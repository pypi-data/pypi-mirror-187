from __future__ import annotations

import datetime
import pickle as pkl
import typing as t

import numpy as np

from sarus_data_spec.base import Referrable
import sarus_data_spec.dataset as sd
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st


class Transform(Referrable[sp.Transform]):
    """A python class to describe transforms"""

    def prototype(self) -> t.Type[sp.Transform]:
        """Return the type of the underlying protobuf."""
        return sp.Transform

    def name(self) -> str:
        return self._protobuf.name

    def doc(self) -> str:
        return self._protobuf.doc

    def is_composed(self) -> bool:
        """Is the transform composed."""
        return self._protobuf.spec.HasField('composed')

    def is_variable(self) -> bool:
        """Is the transform a variable."""
        return self._protobuf.spec.HasField('variable')

    def spec(self) -> str:
        return t.cast(str, self.protobuf().spec.WhichOneof('spec'))

    def is_external(self) -> bool:
        """Is the transform an external operation."""
        return self._protobuf.spec.HasField("external")

    def infer_output_type(
        self, *arguments: st.DataSpec, **named_arguments: st.DataSpec
    ) -> t.Tuple[str, t.Callable[[st.DataSpec], None]]:
        """Guess if the external transform output is a Dataset or a Scalar.

        Registers schema if it is a Dataset and returns the value type.
        """
        return self.manager().infer_output_type(
            self, *arguments, **named_arguments
        )

    def transforms(self) -> t.Set[st.Transform]:
        """return all transforms (and avoid infinite recursions/loops)"""

        class Transforms(st.TransformVisitor):
            visited: t.Set[st.Transform] = set()

            def all(self, visited: st.Transform) -> None:
                self.visited.add(visited)

            def composed(
                self,
                visited: st.Transform,
                transform: st.Transform,
                *arguments: st.Transform,
                **named_arguments: st.Transform,
            ) -> None:
                self.visited.add(transform)
                if transform not in self.visited:
                    transform.accept(self)
                for arg in arguments:
                    if arg not in self.visited:
                        arg.accept(self)
                for name, arg in named_arguments.items():
                    if arg not in self.visited:
                        arg.accept(self)

        visitor = Transforms()
        self.accept(visitor)
        return visitor.visited

    def variables(self) -> t.Set[st.Transform]:
        """Return all the variables from a composed transform"""
        return {
            transform
            for transform in self.transforms()
            if transform.is_variable()
        }

    def compose(
        self,
        *compose_arguments: st.Transform,
        **compose_named_arguments: st.Transform,
    ) -> st.Transform:
        class Compose(st.TransformVisitor):
            visited: t.Set[st.Transform] = set()
            result: st.Transform

            def variable(
                self,
                visited: st.Transform,
                position_name: t.Union[int, str] = 0,
            ) -> None:
                self.result = visited
                if isinstance(position_name, int):
                    if position_name < len(compose_arguments):
                        self.result = compose_arguments[position_name]
                else:
                    if position_name in compose_named_arguments:
                        self.result = compose_named_arguments[position_name]

            def composed(
                self,
                visited: st.Transform,
                transform: st.Transform,
                *arguments: st.Transform,
                **named_arguments: st.Transform,
            ) -> None:
                if visited not in self.visited:
                    self.result = composed(
                        transform,
                        *(
                            arg.compose(
                                *compose_arguments, **compose_named_arguments
                            )
                            for arg in arguments
                        ),
                        **{
                            name: arg.compose(
                                *compose_arguments, **compose_named_arguments
                            )
                            for name, arg in named_arguments.items()
                        },
                    )
                    self.visited.add(visited)
                else:
                    self.result = visited

            def other(self, visited: st.Transform) -> None:
                self.result = composed(
                    visited, *compose_arguments, **compose_named_arguments
                )

        visitor = Compose()
        self.accept(visitor)
        return visitor.result

    def apply(
        self,
        *apply_arguments: st.DataSpec,
        **apply_named_arguments: st.DataSpec,
    ) -> st.DataSpec:
        class Apply(st.TransformVisitor):
            visited: t.Dict[st.Transform, st.DataSpec] = {}
            result: st.DataSpec

            def variable(
                self,
                visited: st.Transform,
                position_name: t.Union[int, str] = 0,
            ) -> None:
                if isinstance(position_name, int):
                    if position_name < len(apply_arguments):
                        self.result = apply_arguments[position_name]
                else:
                    if position_name in apply_named_arguments:
                        self.result = apply_named_arguments[position_name]
                if self.result is None:
                    raise ValueError("Cannot substitute all variables")

            def composed(
                self,
                visited: st.Transform,
                transform: st.Transform,
                *arguments: st.Transform,
                **named_arguments: st.Transform,
            ) -> None:
                if visited not in self.visited:
                    self.result = t.cast(
                        sd.Dataset,
                        sd.transformed(
                            transform,
                            *(
                                arg.apply(
                                    *apply_arguments, **apply_named_arguments
                                )
                                for arg in arguments
                            ),
                            dataspec_type=None,
                            dataspec_name=None,
                            **{
                                name: arg.apply(
                                    *apply_arguments, **apply_named_arguments
                                )
                                for name, arg in named_arguments.items()
                            },
                        ),
                    )
                    self.visited[visited] = self.result

            def other(self, visited: st.Transform) -> None:
                self.result = sd.transformed(
                    visited,
                    *apply_arguments,
                    dataspec_type=None,
                    dataspec_name=None,
                    **apply_named_arguments,
                )

        visitor = Apply()
        self.accept(visitor)
        return visitor.result

    def abstract(
        self,
        *arguments: t.Union[int, str],
        **named_arguments: t.Union[int, str],
    ) -> st.Transform:
        return composed(
            self,
            *(variable(position_name=arg) for arg in arguments),
            **{
                name: variable(position_name=arg)
                for name, arg in named_arguments.items()
            },
        )

    def __call__(
        self,
        *arguments: t.Union[st.Transform, st.DataSpec, int, str],
        **named_arguments: t.Union[st.Transform, st.DataSpec, int, str],
    ) -> t.Union[st.Transform, st.DataSpec]:
        """Applies the transform to another element"""
        all_transforms = True
        all_datasets = True
        all_variables = True
        for arg in arguments:
            all_transforms = all_transforms and isinstance(arg, Transform)
            all_datasets = all_datasets and (isinstance(arg, st.DataSpec))
            all_variables = all_variables and (
                isinstance(arg, int) or isinstance(arg, str)
            )
        for arg in named_arguments.values():
            all_transforms = all_transforms and isinstance(arg, Transform)
            all_datasets = all_datasets and (isinstance(arg, st.DataSpec))
            all_variables = all_variables and (
                isinstance(arg, int) or isinstance(arg, str)
            )
        if all_datasets:
            return self.apply(
                *t.cast(t.Sequence[st.DataSpec], arguments),
                **t.cast(t.Mapping[str, st.DataSpec], named_arguments),
            )
        if all_transforms:
            return self.compose(
                *t.cast(t.Sequence[Transform], arguments),
                **t.cast(t.Mapping[str, Transform], named_arguments),
            )
        if all_variables:
            return self.abstract(
                *t.cast(t.Sequence[t.Union[int, str]], arguments),
                **t.cast(t.Mapping[str, t.Union[int, str]], named_arguments),
            )
        return self

    def __mul__(self, argument: st.Transform) -> st.Transform:
        return self.compose(argument)

    # A Visitor acceptor
    def accept(self, visitor: st.TransformVisitor) -> None:
        visitor.all(self)
        if self.is_composed():
            visitor.composed(
                self,
                t.cast(
                    Transform,
                    self.storage().referrable(
                        self._protobuf.spec.composed.transform
                    ),
                ),
                *(
                    t.cast(Transform, self.storage().referrable(transform))
                    for transform in self._protobuf.spec.composed.arguments
                ),
                **{
                    name: t.cast(
                        Transform, self.storage().referrable(transform)
                    )
                    for name, transform in self._protobuf.spec.composed.named_arguments.items()  # noqa: E501
                },
            )
        elif self.is_variable():
            var = self._protobuf.spec.variable
            if var.position == np.iinfo(np.int32).min32:
                visitor.variable(self, position_name=var.name)
            else:
                visitor.variable(self, position_name=var.position)
        else:
            visitor.other(self)

    def dot(self) -> str:
        """return a graphviz representation of the transform"""

        class Dot(st.TransformVisitor):
            visited: t.Set[st.Transform] = set()
            nodes: t.Dict[str, str] = {}
            edges: t.Set[t.Tuple[str, str]] = set()

            def variable(
                self,
                visited: st.Transform,
                position_name: t.Union[int, str] = 0,
            ) -> None:
                self.nodes[visited.uuid()] = str(position_name)

            def composed(
                self,
                visited: st.Transform,
                transform: st.Transform,
                *arguments: st.Transform,
                **named_arguments: st.Transform,
            ) -> None:
                if visited not in self.visited:
                    transform.accept(self)
                    for argument in arguments:
                        if argument.is_composed():
                            self.edges.add(
                                (
                                    argument.protobuf().spec.composed.transform,  # noqa: E501
                                    transform.uuid(),
                                )
                            )
                        else:
                            self.edges.add((argument.uuid(), transform.uuid()))
                        argument.accept(self)
                    for _, argument in named_arguments.items():
                        if argument.is_composed():
                            self.edges.add(
                                (
                                    argument.protobuf().spec.composed.transform,  # noqa: E501
                                    transform.uuid(),
                                )
                            )
                        else:
                            self.edges.add((argument.uuid(), transform.uuid()))
                        argument.accept(self)
                    self.visited.add(visited)

            def other(self, visited: st.Transform) -> None:
                self.nodes[visited.uuid()] = visited.name()

        visitor = Dot()
        self.accept(visitor)
        result = 'digraph {'
        for uuid, label in visitor.nodes.items():
            result += f'\n"{uuid}" [label="{label} ({uuid[:2]})"];'
        for u1, u2 in visitor.edges:
            result += f'\n"{u1}" -> "{u2}";'
        result += '}'
        return result


# Builders
def identity() -> Transform:
    return Transform(
        sp.Transform(
            name='Identity',
            spec=sp.Transform.Spec(identity=sp.Transform.Identity()),
            inversible=True,
            schema_preserving=True,
        )
    )


def variable(position_name: t.Union[int, str] = 0) -> Transform:
    if isinstance(position_name, int):
        return Transform(
            sp.Transform(
                name='Variable',
                spec=sp.Transform.Spec(
                    variable=sp.Transform.Variable(position=position_name)
                ),
                inversible=True,
                schema_preserving=True,
            )
        )
    return Transform(
        sp.Transform(
            name='Variable',
            spec=sp.Transform.Spec(
                variable=sp.Transform.Variable(
                    name=position_name, position=np.iinfo(np.int32).min32
                )
            ),
            inversible=True,
            schema_preserving=True,
        )
    )


def composed(
    transform: st.Transform,
    *arguments: st.Transform,
    **named_arguments: st.Transform,
) -> st.Transform:
    if transform.is_composed():
        # We want to compose simple transforms only
        return transform.compose(*arguments, **named_arguments)
    return Transform(
        sp.Transform(
            name='Composed',
            spec=sp.Transform.Spec(
                composed=sp.Transform.Composed(
                    transform=transform.uuid(),
                    arguments=(a.uuid() for a in arguments),
                    named_arguments={
                        n: a.uuid() for n, a in named_arguments.items()
                    },
                )
            ),
        )
    )


def op_identifier_from_id(id: str) -> sp.Transform.External.OpIdentifier:
    """Build an OpIdentifier protobuf message from a string identifier.

    Args:
        identifier (str): id in the form library.name (e.g. sklearn.PD_MEAN)
    """
    parts = id.split(".")
    if len(parts) != 2:
        raise ValueError(
            f"Transform ID {id} should have the format library.name"
        )
    library, name = parts

    mapping = {
        "std": sp.Transform.External.Std,
        "sklearn": sp.Transform.External.Sklearn,
        "pandas": sp.Transform.External.Pandas,
        "pandas_profiling": sp.Transform.External.PandasProfiling,
        "numpy": sp.Transform.External.Numpy,
        "tensorflow": sp.Transform.External.Tensorflow,
        "xgboost": sp.Transform.External.XGBoost,
        "skopt": sp.Transform.External.Skopt,
        "imblearn": sp.Transform.External.Imblearn,
    }

    if library not in mapping.keys():
        raise ValueError(f"Unsupported library {library}")

    MsgClass = mapping[library]
    msg = sp.Transform.External.OpIdentifier()
    getattr(msg, library).CopyFrom(MsgClass(name=name))
    return msg


def transform_id(transform: st.Transform) -> str:
    """Return the transform id."""
    spec = transform.protobuf().spec
    spec_type = str(spec.WhichOneof("spec"))

    if spec_type != "external":
        return spec_type
    else:
        library = str(spec.external.op_identifier.WhichOneof("op"))
        op_name = getattr(spec.external.op_identifier, library).name
        return f"{library}.{op_name}"


def external(
    id: str,
    py_args: t.Dict[int, t.Any] = {},
    py_kwargs: t.Dict[str, t.Any] = {},
    ds_args_pos: t.List[int] = [],
) -> Transform:
    """Create an external library transform.

    Args:
        id (str): id in the form library.name (e.g. sklearn.PD_MEAN)
        py_args (Dict[int, Any]):
            the Python objects passed as arguments to the transform.
        py_kwargs (Dict[int, Any]):
            the Python objects passed as keyword arguments to the transform.
        ds_args_pos (List[int]):
            the positions of Dataspecs passed in args.
    """
    external = sp.Transform.External(
        arguments=pkl.dumps([]),
        named_arguments=pkl.dumps(
            {
                "py_args": py_args,
                "py_kwargs": py_kwargs,
                "ds_args_pos": ds_args_pos,
            }
        ),
        op_identifier=op_identifier_from_id(id),
    )

    return Transform(
        sp.Transform(
            name=id,
            spec=sp.Transform.Spec(
                external=external,
            ),
        )
    )


def project(projection: st.Type) -> Transform:
    return Transform(
        sp.Transform(
            name='Project',
            spec=sp.Transform.Spec(
                project=sp.Transform.Project(projection=projection.protobuf())
            ),
            inversible=False,
            schema_preserving=False,
        )
    )


def filter(filter: st.Type) -> Transform:
    return Transform(
        sp.Transform(
            name='Filter',
            spec=sp.Transform.Spec(
                filter=sp.Transform.Filter(filter=filter.protobuf())
            ),
            inversible=False,
            schema_preserving=False,
        )
    )


def shuffle() -> Transform:
    return Transform(
        sp.Transform(
            name='Shuffle',
            spec=sp.Transform.Spec(shuffle=sp.Transform.Shuffle()),
            inversible=False,
            schema_preserving=True,
        )
    )


def join(on: st.Type) -> Transform:
    return Transform(
        sp.Transform(
            name='Join',
            spec=sp.Transform.Spec(join=sp.Transform.Join(on=on.protobuf())),
            inversible=False,
            schema_preserving=False,
        )
    )


def cast(type: st.Type) -> Transform:
    return Transform(
        sp.Transform(
            name='Cast',
            spec=sp.Transform.Spec(
                cast=sp.Transform.Cast(type=type.protobuf())
            ),
            inversible=False,
            schema_preserving=False,
        )
    )


def sample(fraction_size: t.Union[float, int]) -> Transform:
    return Transform(
        sp.Transform(
            name='Sample',
            spec=sp.Transform.Spec(
                sample=sp.Transform.Sample(size=fraction_size)
                if isinstance(fraction_size, int)
                else sp.Transform.Sample(fraction=fraction_size)
            ),
            inversible=False,
            schema_preserving=False,
        )
    )


def user_settings() -> Transform:
    """Transform to create a dataspec from
    a protected one with a new schema. It should
    be called on:
    - the dataset that needs to be protected as the first arg
    - a kwarg user_type: scalar output of automatic_user_setttings"""
    return Transform(
        sp.Transform(
            name='User Settings',
            spec=sp.Transform.Spec(user_settings=sp.Transform.UserSettings()),
            inversible=False,
            schema_preserving=False,
        )
    )


def automatic_user_settings() -> Transform:
    """Transform to be called on a protected dataset
    we want to change the schema. It creates a scalar
    whose value explicits the new type of the schema"""
    return Transform(
        sp.Transform(
            name='automatic_user_settings',
            spec=sp.Transform.Spec(
                automatic_user_settings=sp.Transform.AutomaticUserSettings()
            ),
            inversible=False,
            schema_preserving=False,
            properties={'creation_time': str(datetime.datetime.now())},
        )
    )


def synthetic() -> Transform:
    """Synthetic transform"""
    return Transform(
        sp.Transform(
            name="Synthetic data",
            spec=sp.Transform.Spec(
                synthetic=sp.Transform.Synthetic(),
            ),
            inversible=False,
            schema_preserving=True,
        )
    )


def protect() -> Transform:
    """Transform used for protection should be called on:
    - the dataset that needs to be protected as the first arg
    - a kwarg protected_paths: scalar specifying the paths
     to the entities to protect
    - a kwarg public_paths: scalar specifying the paths to
    the public tables"""
    return Transform(
        sp.Transform(
            name='Dataset with Protected Entity',
            spec=sp.Transform.Spec(protect_dataset=sp.Transform.Protect()),
            inversible=True,
            schema_preserving=False,
        )
    )


def transcode() -> st.Transform:
    return Transform(
        sp.Transform(
            name='Transcode',
            spec=sp.Transform.Spec(transcode=sp.Transform.Transcode()),
            inversible=True,
            schema_preserving=False,
        )
    )


def inverse_transcode() -> st.Transform:

    return Transform(
        sp.Transform(
            name='Inverse Transcoding for synthetic data',
            spec=sp.Transform.Spec(
                inverse_transcode=sp.Transform.InverseTranscode()
            ),
            inversible=True,
            schema_preserving=False,
        )
    )


def automatic_protected_paths() -> st.Transform:
    """Transform that should be called on the dataset
    that needs to be protected, it creates a scalar whose
    value will explicit the paths to protect"""
    return Transform(
        sp.Transform(
            name='automatic_protected_paths',
            spec=sp.Transform.Spec(
                protected_paths=sp.Transform.ProtectedPaths()
            ),
            properties={'creation_time': str(datetime.datetime.now())},
        )
    )


def automatic_public_paths() -> st.Transform:
    """Transform that should be called on the dataset
    that needs to be protected, it creates a scalar whose
    value will explicit the paths to public entities"""
    return Transform(
        sp.Transform(
            name='automatic_public_paths',
            spec=sp.Transform.Spec(public_paths=sp.Transform.PublicPaths()),
            properties={'creation_time': str(datetime.datetime.now())},
        )
    )


def get_item(path: st.Path) -> st.Transform:
    return Transform(
        sp.Transform(
            name='get_item',
            spec=sp.Transform.Spec(
                get_item=sp.Transform.GetItem(path=path.protobuf())
            ),
            inversible=False,
            schema_preserving=False,
        )
    )


def assign_budget() -> st.Transform:
    """Transform to assign a given privacy budget to a dataset.
    It is used to specify the budget to compute the attributes
    size, bounds, marginals"""

    return Transform(
        sp.Transform(
            name='budget_assignment',
            spec=sp.Transform.Spec(assign_budget=sp.Transform.AssignBudget()),
        )
    )


def automatic_budget() -> st.Transform:
    """Transform to create a scalar specifying a budget
    automatically from the dataset it is called on.
    The rule to fix the budget is set in the corresponding
    op.
    """

    return Transform(
        sp.Transform(
            name='automatic_budget',
            spec=sp.Transform.Spec(
                automatic_budget=sp.Transform.AutomaticBudget()
            ),
        )
    )


def attributes_budget() -> st.Transform:
    """Transform to create a scalar specifying an
     epsilon,delta budget for the DP attributes of a
    dataset. It is called on a scalar specifying a
    global budget for attributes+sd."""

    return Transform(
        sp.Transform(
            name='attributes_budget',
            spec=sp.Transform.Spec(
                attribute_budget=sp.Transform.AttributesBudget()
            ),
        )
    )


def sd_budget() -> st.Transform:
    """Transform to create a scalar specifying an
     epsilon,delta budget for a synthetic dataset.
    It should be called on another scalar that specifies
    a global budget (SD+DP attributes)"""

    return Transform(
        sp.Transform(
            name='sd_budget',
            spec=sp.Transform.Spec(sd_budget=sp.Transform.SDBudget()),
        )
    )


def sampling_ratios() -> st.Transform:
    """Transform to create a scalar specifying the sampling ratio for
    each table to synthetize from.
    It should be called on the dataset to synthetize from."""
    return Transform(
        sp.Transform(
            name='sampling_ratios',
            spec=sp.Transform.Spec(
                sampling_ratios=sp.Transform.SamplingRatios()
            ),
        )
    )


def derive_seed(random_int: int) -> st.Transform:
    """Transform to derive a seed from a master seed"""
    return Transform(
        sp.Transform(
            name='derive_seed',
            spec=sp.Transform.Spec(
                derive_seed=sp.Transform.DeriveSeed(random_integer=random_int)
            ),
        )
    )


def group_by_pe() -> st.Transform:
    """Transform that allows to group fields
    by protected entity value. This implies that
    the dataset on which the transform is
    applied should be PEP"""
    return Transform(
        sp.Transform(
            name='group_by',
            spec=sp.Transform.Spec(group_by_pe=sp.Transform.GroupByPE()),
        )
    )


def select_sql(query: str) -> st.Transform:
    """Transform that applies a query to a dataset.
    Calling .schema() or .to_arrow() on a select_sql transformed dataset
    the .sql method will be invoked and the query will be executed.
    """
    return Transform(
        sp.Transform(
            name='select_sql',
            spec=sp.Transform.Spec(
                select_sql=sp.Transform.SelectSql(query=query)
            ),
            inversible=False,
            schema_preserving=False,
        )
    )


def extract(
    size: int,
) -> st.Transform:
    """Transform that should be called on a dataset from which we want to
    extract some rows from according to the size parameter and a kwargs
    random_seed, a scalar that is a seed. For now, seed and size are
    ignored and iterating on the extract transfomed dataset will be as
    iterating over the parent dataset.
    """
    return Transform(
        sp.Transform(
            name='extract',
            spec=sp.Transform.Spec(extract=sp.Transform.Extract(size=size)),
            inversible=False,
            schema_preserving=True,
        )
    )


def relationship_spec() -> st.Transform:
    """Transform that allows to redefine the primary and foreign keys
    of a dataset."""
    return Transform(
        sp.Transform(
            name='relationship_spec',
            spec=sp.Transform.Spec(
                relationship_spec=sp.Transform.RelationshipSpec()
            ),
        )
    )


if t.TYPE_CHECKING:
    test_transform: st.Transform = Transform(sp.Transform())

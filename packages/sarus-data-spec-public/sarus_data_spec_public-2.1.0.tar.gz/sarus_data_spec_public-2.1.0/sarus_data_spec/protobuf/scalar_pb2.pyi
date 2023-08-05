"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class Scalar(google.protobuf.message.Message):
    """A Scalar represents data that does not fulfill the promise of a Dataset.
    A Dataset promises to have a schema and the possibility to iterate on
    pyarrow.RecordBatches
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    class PropertiesEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text = ...
        value: typing.Text = ...
        def __init__(self,
            *,
            key : typing.Text = ...,
            value : typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"key",b"key",u"value",b"value"]) -> None: ...

    class Spec(google.protobuf.message.Message):
        """Definitions
        How to obtain the dataset
        """
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        TRANSFORMED_FIELD_NUMBER: builtins.int
        MODEL_FIELD_NUMBER: builtins.int
        PRIVACY_PARAMS_FIELD_NUMBER: builtins.int
        RANDOM_SEED_FIELD_NUMBER: builtins.int
        @property
        def transformed(self) -> global___Scalar.Transformed: ...
        @property
        def model(self) -> global___Scalar.Model: ...
        @property
        def privacy_params(self) -> global___Scalar.PrivacyParameters: ...
        @property
        def random_seed(self) -> global___Scalar.RandomSeed: ...
        def __init__(self,
            *,
            transformed : typing.Optional[global___Scalar.Transformed] = ...,
            model : typing.Optional[global___Scalar.Model] = ...,
            privacy_params : typing.Optional[global___Scalar.PrivacyParameters] = ...,
            random_seed : typing.Optional[global___Scalar.RandomSeed] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal[u"model",b"model",u"privacy_params",b"privacy_params",u"random_seed",b"random_seed",u"spec",b"spec",u"transformed",b"transformed"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"model",b"model",u"privacy_params",b"privacy_params",u"random_seed",b"random_seed",u"spec",b"spec",u"transformed",b"transformed"]) -> None: ...
        def WhichOneof(self, oneof_group: typing_extensions.Literal[u"spec",b"spec"]) -> typing.Optional[typing_extensions.Literal["transformed","model","privacy_params","random_seed"]]: ...

    class Transformed(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        class NamedArgumentsEntry(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
            KEY_FIELD_NUMBER: builtins.int
            VALUE_FIELD_NUMBER: builtins.int
            key: typing.Text = ...
            value: typing.Text = ...
            def __init__(self,
                *,
                key : typing.Text = ...,
                value : typing.Text = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal[u"key",b"key",u"value",b"value"]) -> None: ...

        TRANSFORM_FIELD_NUMBER: builtins.int
        ARGUMENTS_FIELD_NUMBER: builtins.int
        NAMED_ARGUMENTS_FIELD_NUMBER: builtins.int
        transform: typing.Text = ...
        """Transform id"""

        @property
        def arguments(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
            """Dataset or other object ids"""
            pass
        @property
        def named_arguments(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, typing.Text]: ...
        def __init__(self,
            *,
            transform : typing.Text = ...,
            arguments : typing.Optional[typing.Iterable[typing.Text]] = ...,
            named_arguments : typing.Optional[typing.Mapping[typing.Text, typing.Text]] = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"arguments",b"arguments",u"named_arguments",b"named_arguments",u"transform",b"transform"]) -> None: ...

    class Model(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        class ModelClass(_ModelClass, metaclass=_ModelClassEnumTypeWrapper):
            pass
        class _ModelClass:
            V = typing.NewType('V', builtins.int)
        class _ModelClassEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ModelClass.V], builtins.type):
            DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor = ...
            TF_KERAS = Scalar.Model.ModelClass.V(0)
            SK_SVC = Scalar.Model.ModelClass.V(1)
            SK_ONEHOT = Scalar.Model.ModelClass.V(2)
            SK_PCA = Scalar.Model.ModelClass.V(3)
            SK_AFFINITY_PROPAGATION = Scalar.Model.ModelClass.V(4)
            """Cluster"""

            SK_AGGLOMERATIVE_CLUSTERING = Scalar.Model.ModelClass.V(5)
            SK_BIRCH = Scalar.Model.ModelClass.V(6)
            SK_DBSCAN = Scalar.Model.ModelClass.V(7)
            SK_FEATURE_AGGLOMERATION = Scalar.Model.ModelClass.V(8)
            SK_KMEANS = Scalar.Model.ModelClass.V(9)
            SK_MINIBATCH_KMEANS = Scalar.Model.ModelClass.V(10)
            SK_MEAN_SHIFT = Scalar.Model.ModelClass.V(11)
            SK_OPTICS = Scalar.Model.ModelClass.V(12)
            SK_SPECTRAL_CLUSTERING = Scalar.Model.ModelClass.V(13)
            SK_SPECTRAL_BICLUSTERING = Scalar.Model.ModelClass.V(14)
            SK_SPECTRAL_COCLUSTERING = Scalar.Model.ModelClass.V(15)
            SK_ADABOOST_CLASSIFIER = Scalar.Model.ModelClass.V(60)
            """ensemble"""

            SK_ADABOOST_REGRESSOR = Scalar.Model.ModelClass.V(61)
            SK_BAGGING_CLASSIFIER = Scalar.Model.ModelClass.V(62)
            SK_BAGGING_REGRESSOR = Scalar.Model.ModelClass.V(63)
            SK_EXTRA_TREES_REGRESSOR = Scalar.Model.ModelClass.V(64)
            SK_EXTRA_TREES_CLASSIFIER = Scalar.Model.ModelClass.V(65)
            SK_GRADIENT_BOOSTING_CLASSIFIER = Scalar.Model.ModelClass.V(66)
            SK_GRADIENT_BOOSTING_REGRESSOR = Scalar.Model.ModelClass.V(67)
            SK_ISOLATION_FOREST = Scalar.Model.ModelClass.V(68)
            SK_RANDOM_FOREST_CLASSIFIER = Scalar.Model.ModelClass.V(69)
            SK_RANDOM_FOREST_REGRESSOR = Scalar.Model.ModelClass.V(70)
            SK_RANDOM_TREES_EMBEDDING = Scalar.Model.ModelClass.V(71)
            SK_STACKING_CLASSIFIER = Scalar.Model.ModelClass.V(72)
            SK_STACKING_REGRESSOR = Scalar.Model.ModelClass.V(73)
            SK_VOTING_CLASSIFIER = Scalar.Model.ModelClass.V(74)
            SK_VOTING_REGRESSOR = Scalar.Model.ModelClass.V(75)
            SK_HIST_GRADIENT_BOOSTING_REGRESSOR = Scalar.Model.ModelClass.V(76)
            SK_HIST_GRADIENT_BOOSTING_CLASSIFIER = Scalar.Model.ModelClass.V(77)
            SK_REPEATED_STRATIFIED_KFOLD = Scalar.Model.ModelClass.V(80)
            """Model selection"""

            XGB_CLASSIFIER = Scalar.Model.ModelClass.V(92)
            """XGB"""

            SK_LABEL_ENCODER = Scalar.Model.ModelClass.V(98)
            SK_KFOLD = Scalar.Model.ModelClass.V(99)

        TF_KERAS = Scalar.Model.ModelClass.V(0)
        SK_SVC = Scalar.Model.ModelClass.V(1)
        SK_ONEHOT = Scalar.Model.ModelClass.V(2)
        SK_PCA = Scalar.Model.ModelClass.V(3)
        SK_AFFINITY_PROPAGATION = Scalar.Model.ModelClass.V(4)
        """Cluster"""

        SK_AGGLOMERATIVE_CLUSTERING = Scalar.Model.ModelClass.V(5)
        SK_BIRCH = Scalar.Model.ModelClass.V(6)
        SK_DBSCAN = Scalar.Model.ModelClass.V(7)
        SK_FEATURE_AGGLOMERATION = Scalar.Model.ModelClass.V(8)
        SK_KMEANS = Scalar.Model.ModelClass.V(9)
        SK_MINIBATCH_KMEANS = Scalar.Model.ModelClass.V(10)
        SK_MEAN_SHIFT = Scalar.Model.ModelClass.V(11)
        SK_OPTICS = Scalar.Model.ModelClass.V(12)
        SK_SPECTRAL_CLUSTERING = Scalar.Model.ModelClass.V(13)
        SK_SPECTRAL_BICLUSTERING = Scalar.Model.ModelClass.V(14)
        SK_SPECTRAL_COCLUSTERING = Scalar.Model.ModelClass.V(15)
        SK_ADABOOST_CLASSIFIER = Scalar.Model.ModelClass.V(60)
        """ensemble"""

        SK_ADABOOST_REGRESSOR = Scalar.Model.ModelClass.V(61)
        SK_BAGGING_CLASSIFIER = Scalar.Model.ModelClass.V(62)
        SK_BAGGING_REGRESSOR = Scalar.Model.ModelClass.V(63)
        SK_EXTRA_TREES_REGRESSOR = Scalar.Model.ModelClass.V(64)
        SK_EXTRA_TREES_CLASSIFIER = Scalar.Model.ModelClass.V(65)
        SK_GRADIENT_BOOSTING_CLASSIFIER = Scalar.Model.ModelClass.V(66)
        SK_GRADIENT_BOOSTING_REGRESSOR = Scalar.Model.ModelClass.V(67)
        SK_ISOLATION_FOREST = Scalar.Model.ModelClass.V(68)
        SK_RANDOM_FOREST_CLASSIFIER = Scalar.Model.ModelClass.V(69)
        SK_RANDOM_FOREST_REGRESSOR = Scalar.Model.ModelClass.V(70)
        SK_RANDOM_TREES_EMBEDDING = Scalar.Model.ModelClass.V(71)
        SK_STACKING_CLASSIFIER = Scalar.Model.ModelClass.V(72)
        SK_STACKING_REGRESSOR = Scalar.Model.ModelClass.V(73)
        SK_VOTING_CLASSIFIER = Scalar.Model.ModelClass.V(74)
        SK_VOTING_REGRESSOR = Scalar.Model.ModelClass.V(75)
        SK_HIST_GRADIENT_BOOSTING_REGRESSOR = Scalar.Model.ModelClass.V(76)
        SK_HIST_GRADIENT_BOOSTING_CLASSIFIER = Scalar.Model.ModelClass.V(77)
        SK_REPEATED_STRATIFIED_KFOLD = Scalar.Model.ModelClass.V(80)
        """Model selection"""

        XGB_CLASSIFIER = Scalar.Model.ModelClass.V(92)
        """XGB"""

        SK_LABEL_ENCODER = Scalar.Model.ModelClass.V(98)
        SK_KFOLD = Scalar.Model.ModelClass.V(99)

        ARGUMENTS_FIELD_NUMBER: builtins.int
        NAMED_ARGUMENTS_FIELD_NUMBER: builtins.int
        MODEL_CLASS_FIELD_NUMBER: builtins.int
        arguments: builtins.bytes = ...
        named_arguments: builtins.bytes = ...
        model_class: global___Scalar.Model.ModelClass.V = ...
        def __init__(self,
            *,
            arguments : builtins.bytes = ...,
            named_arguments : builtins.bytes = ...,
            model_class : global___Scalar.Model.ModelClass.V = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"arguments",b"arguments",u"model_class",b"model_class",u"named_arguments",b"named_arguments"]) -> None: ...

    class PrivacyParameters(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        class Point(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
            EPSILON_FIELD_NUMBER: builtins.int
            DELTA_FIELD_NUMBER: builtins.int
            epsilon: builtins.float = ...
            delta: builtins.float = ...
            def __init__(self,
                *,
                epsilon : builtins.float = ...,
                delta : builtins.float = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal[u"delta",b"delta",u"epsilon",b"epsilon"]) -> None: ...

        POINTS_FIELD_NUMBER: builtins.int
        @property
        def points(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Scalar.PrivacyParameters.Point]: ...
        def __init__(self,
            *,
            points : typing.Optional[typing.Iterable[global___Scalar.PrivacyParameters.Point]] = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"points",b"points"]) -> None: ...

    class RandomSeed(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        VALUE_FIELD_NUMBER: builtins.int
        value: builtins.int = ...
        def __init__(self,
            *,
            value : builtins.int = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"value",b"value"]) -> None: ...

    UUID_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    DOC_FIELD_NUMBER: builtins.int
    SPEC_FIELD_NUMBER: builtins.int
    PROPERTIES_FIELD_NUMBER: builtins.int
    uuid: typing.Text = ...
    """A Scalar does not ensure this possibility. As a consequence, oprations
    from standard libraries are allowed (pandas.mean, numpy.std,...) but
    operations implemented for Datasets by Sarus like computing marginals or
    fitting a Keras model cannot be performed on a Scalar.

    Scalars are generated by transforms that explicitly require a specific
    format (e.g. as_pandas, as_numpy,...) or as byproducts of transforms
    (model weights, training history,...).

    e.g. RFC 4122 id used to refer to the dataset (content linked?)
    """

    name: typing.Text = ...
    doc: typing.Text = ...
    @property
    def spec(self) -> global___Scalar.Spec: ...
    @property
    def properties(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, typing.Text]:
        """Other properties"""
        pass
    def __init__(self,
        *,
        uuid : typing.Text = ...,
        name : typing.Text = ...,
        doc : typing.Text = ...,
        spec : typing.Optional[global___Scalar.Spec] = ...,
        properties : typing.Optional[typing.Mapping[typing.Text, typing.Text]] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal[u"spec",b"spec"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"doc",b"doc",u"name",b"name",u"properties",b"properties",u"spec",b"spec",u"uuid",b"uuid"]) -> None: ...
global___Scalar = Scalar

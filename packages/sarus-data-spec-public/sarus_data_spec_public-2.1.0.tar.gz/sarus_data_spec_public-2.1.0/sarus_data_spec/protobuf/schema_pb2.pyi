"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import sarus_data_spec.protobuf.path_pb2
import sarus_data_spec.protobuf.type_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class Schema(google.protobuf.message.Message):
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

    class Hypothesis(google.protobuf.message.Message):
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

        UUID_FIELD_NUMBER: builtins.int
        DATASET_FIELD_NUMBER: builtins.int
        NAME_FIELD_NUMBER: builtins.int
        TYPE_FIELD_NUMBER: builtins.int
        PROPERTIES_FIELD_NUMBER: builtins.int
        uuid: typing.Text = ...
        """Schema.Hypothesis attribute, the type contains Hypothesis elements with scores"""

        dataset: typing.Text = ...
        """uuid"""

        name: typing.Text = ...
        @property
        def type(self) -> sarus_data_spec.protobuf.type_pb2.Type: ...
        @property
        def properties(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, typing.Text]:
            """Other properties"""
            pass
        def __init__(self,
            *,
            uuid : typing.Text = ...,
            dataset : typing.Text = ...,
            name : typing.Text = ...,
            type : typing.Optional[sarus_data_spec.protobuf.type_pb2.Type] = ...,
            properties : typing.Optional[typing.Mapping[typing.Text, typing.Text]] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal[u"type",b"type"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"dataset",b"dataset",u"name",b"name",u"properties",b"properties",u"type",b"type",u"uuid",b"uuid"]) -> None: ...

    UUID_FIELD_NUMBER: builtins.int
    DATASET_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    PROTECTED_FIELD_NUMBER: builtins.int
    PROPERTIES_FIELD_NUMBER: builtins.int
    uuid: typing.Text = ...
    """Schema definition attribute"""

    dataset: typing.Text = ...
    """uuid"""

    name: typing.Text = ...
    @property
    def type(self) -> sarus_data_spec.protobuf.type_pb2.Type: ...
    @property
    def protected(self) -> sarus_data_spec.protobuf.path_pb2.Path:
        """Protected entity (may be empty for non-Sarus datasets)"""
        pass
    @property
    def properties(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, typing.Text]:
        """Other properties"""
        pass
    def __init__(self,
        *,
        uuid : typing.Text = ...,
        dataset : typing.Text = ...,
        name : typing.Text = ...,
        type : typing.Optional[sarus_data_spec.protobuf.type_pb2.Type] = ...,
        protected : typing.Optional[sarus_data_spec.protobuf.path_pb2.Path] = ...,
        properties : typing.Optional[typing.Mapping[typing.Text, typing.Text]] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal[u"protected",b"protected",u"type",b"type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"dataset",b"dataset",u"name",b"name",u"properties",b"properties",u"protected",b"protected",u"type",b"type",u"uuid",b"uuid"]) -> None: ...
global___Schema = Schema

"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.internal.well_known_types
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _NullValue:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _NullValueEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_NullValue.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    NULL_VALUE: _NullValue.ValueType  # 0
    """Null value."""

class NullValue(_NullValue, metaclass=_NullValueEnumTypeWrapper):
    """`NullValue` is a singleton enumeration to represent the null value for the
    `Value` type union.

     The JSON representation for `NullValue` is JSON `null`.
    """
    pass

NULL_VALUE: NullValue.ValueType  # 0
"""Null value."""

global___NullValue = NullValue


class Struct(google.protobuf.message.Message, google.protobuf.internal.well_known_types.Struct):
    """`Struct` represents a structured data value, consisting of fields
    which map to dynamically typed values. In some languages, `Struct`
    might be supported by a native representation. For example, in
    scripting languages like JS a struct is represented as an
    object. The details of that representation are described together
    with the proto support for the language.

    The JSON representation for `Struct` is JSON object.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class FieldsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        @property
        def value(self) -> global___Value: ...
        def __init__(self,
            *,
            key: typing.Optional[typing.Text] = ...,
            value: typing.Optional[global___Value] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value",b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    FIELDS_FIELD_NUMBER: builtins.int
    @property
    def fields(self) -> google.protobuf.internal.containers.MessageMap[typing.Text, global___Value]:
        """Unordered map of dynamically typed values."""
        pass
    def __init__(self,
        *,
        fields: typing.Optional[typing.Mapping[typing.Text, global___Value]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["fields",b"fields"]) -> None: ...
global___Struct = Struct

class Value(google.protobuf.message.Message):
    """`Value` represents a dynamically typed value which can be either
    null, a number, a string, a boolean, a recursive struct value, or a
    list of values. A producer of value is expected to set one of these
    variants. Absence of any variant indicates an error.

    The JSON representation for `Value` is JSON value.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NULL_VALUE_FIELD_NUMBER: builtins.int
    NUMBER_VALUE_FIELD_NUMBER: builtins.int
    STRING_VALUE_FIELD_NUMBER: builtins.int
    BOOL_VALUE_FIELD_NUMBER: builtins.int
    STRUCT_VALUE_FIELD_NUMBER: builtins.int
    LIST_VALUE_FIELD_NUMBER: builtins.int
    null_value: global___NullValue.ValueType
    """Represents a null value."""

    number_value: builtins.float
    """Represents a double value."""

    string_value: typing.Text
    """Represents a string value."""

    bool_value: builtins.bool
    """Represents a boolean value."""

    @property
    def struct_value(self) -> global___Struct:
        """Represents a structured value."""
        pass
    @property
    def list_value(self) -> global___ListValue:
        """Represents a repeated `Value`."""
        pass
    def __init__(self,
        *,
        null_value: typing.Optional[global___NullValue.ValueType] = ...,
        number_value: typing.Optional[builtins.float] = ...,
        string_value: typing.Optional[typing.Text] = ...,
        bool_value: typing.Optional[builtins.bool] = ...,
        struct_value: typing.Optional[global___Struct] = ...,
        list_value: typing.Optional[global___ListValue] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["bool_value",b"bool_value","kind",b"kind","list_value",b"list_value","null_value",b"null_value","number_value",b"number_value","string_value",b"string_value","struct_value",b"struct_value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["bool_value",b"bool_value","kind",b"kind","list_value",b"list_value","null_value",b"null_value","number_value",b"number_value","string_value",b"string_value","struct_value",b"struct_value"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["kind",b"kind"]) -> typing.Optional[typing_extensions.Literal["null_value","number_value","string_value","bool_value","struct_value","list_value"]]: ...
global___Value = Value

class ListValue(google.protobuf.message.Message, google.protobuf.internal.well_known_types.ListValue):
    """`ListValue` is a wrapper around a repeated field of values.

    The JSON representation for `ListValue` is JSON array.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Value]:
        """Repeated field of dynamically typed values."""
        pass
    def __init__(self,
        *,
        values: typing.Optional[typing.Iterable[global___Value]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["values",b"values"]) -> None: ...
global___ListValue = ListValue

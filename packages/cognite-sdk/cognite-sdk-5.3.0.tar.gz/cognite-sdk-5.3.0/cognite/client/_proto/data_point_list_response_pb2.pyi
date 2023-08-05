"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import data_points_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class DataPointListItem(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    EXTERNALID_FIELD_NUMBER: builtins.int
    ISSTRING_FIELD_NUMBER: builtins.int
    ISSTEP_FIELD_NUMBER: builtins.int
    UNIT_FIELD_NUMBER: builtins.int
    NEXTCURSOR_FIELD_NUMBER: builtins.int
    NUMERICDATAPOINTS_FIELD_NUMBER: builtins.int
    STRINGDATAPOINTS_FIELD_NUMBER: builtins.int
    AGGREGATEDATAPOINTS_FIELD_NUMBER: builtins.int
    id: builtins.int
    externalId: builtins.str
    isString: builtins.bool
    isStep: builtins.bool
    unit: builtins.str
    nextCursor: builtins.str
    @property
    def numericDatapoints(self) -> data_points_pb2.NumericDatapoints: ...
    @property
    def stringDatapoints(self) -> data_points_pb2.StringDatapoints: ...
    @property
    def aggregateDatapoints(self) -> data_points_pb2.AggregateDatapoints: ...
    def __init__(
        self,
        *,
        id: builtins.int = ...,
        externalId: builtins.str = ...,
        isString: builtins.bool = ...,
        isStep: builtins.bool = ...,
        unit: builtins.str = ...,
        nextCursor: builtins.str = ...,
        numericDatapoints: data_points_pb2.NumericDatapoints | None = ...,
        stringDatapoints: data_points_pb2.StringDatapoints | None = ...,
        aggregateDatapoints: data_points_pb2.AggregateDatapoints | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["aggregateDatapoints", b"aggregateDatapoints", "datapointType", b"datapointType", "numericDatapoints", b"numericDatapoints", "stringDatapoints", b"stringDatapoints"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["aggregateDatapoints", b"aggregateDatapoints", "datapointType", b"datapointType", "externalId", b"externalId", "id", b"id", "isStep", b"isStep", "isString", b"isString", "nextCursor", b"nextCursor", "numericDatapoints", b"numericDatapoints", "stringDatapoints", b"stringDatapoints", "unit", b"unit"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["datapointType", b"datapointType"]) -> typing_extensions.Literal["numericDatapoints", "stringDatapoints", "aggregateDatapoints"] | None: ...

global___DataPointListItem = DataPointListItem

@typing_extensions.final
class DataPointListResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ITEMS_FIELD_NUMBER: builtins.int
    @property
    def items(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DataPointListItem]: ...
    def __init__(
        self,
        *,
        items: collections.abc.Iterable[global___DataPointListItem] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["items", b"items"]) -> None: ...

global___DataPointListResponse = DataPointListResponse

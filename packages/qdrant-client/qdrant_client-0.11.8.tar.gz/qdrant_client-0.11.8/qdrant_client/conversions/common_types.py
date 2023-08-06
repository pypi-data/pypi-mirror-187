import sys

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

from typing import Union, List

from qdrant_client import grpc as grpc
from qdrant_client.http import models as rest

Filter = Union[rest.Filter, grpc.Filter]
SearchParams = Union[rest.SearchParams, grpc.SearchParams]
PayloadSelector = Union[rest.PayloadSelector, grpc.WithPayloadSelector]
Distance = Union[rest.Distance, int]  # type(grpc.Distance) == int
HnswConfigDiff = Union[rest.HnswConfigDiff, grpc.HnswConfigDiff]
OptimizersConfigDiff = Union[rest.OptimizersConfigDiff, grpc.OptimizersConfigDiff]
CollectionParamsDiff = Union[rest.CollectionParamsDiff, grpc.CollectionParamsDiff]
WalConfigDiff = Union[rest.WalConfigDiff, grpc.WalConfigDiff]
PointId = Union[int, str, grpc.PointId]
PayloadSchemaType = Union[rest.PayloadSchemaType, rest.PayloadSchemaParams, int]  # type(grpc.PayloadSchemaType) == int
Points = Union[rest.Batch, List[Union[rest.PointStruct, grpc.PointStruct]]]
PointsSelector = Union[List[PointId], rest.Filter, grpc.Filter, rest.PointsSelector, grpc.PointsSelector]
LookupLocation = Union[rest.LookupLocation, grpc.LookupLocation]

AliasOperations = Union[
    rest.CreateAliasOperation,
    rest.RenameAliasOperation,
    rest.DeleteAliasOperation,
    grpc.AliasOperations
]
Payload: TypeAlias = rest.Payload

ScoredPoint: TypeAlias = rest.ScoredPoint
UpdateResult: TypeAlias = rest.UpdateResult
Record: TypeAlias = rest.Record
CollectionsResponse: TypeAlias = rest.CollectionsResponse
CollectionInfo: TypeAlias = rest.CollectionInfo
CountResult: TypeAlias = rest.CountResult
SnapshotDescription: TypeAlias = rest.SnapshotDescription
NamedVector: TypeAlias = rest.NamedVector
VectorParams: TypeAlias = rest.VectorParams
LocksOption: TypeAlias = rest.LocksOption
SnapshotPriority: TypeAlias = rest.SnapshotPriority

SearchRequest = Union[rest.SearchRequest, grpc.SearchPoints]
RecommendRequest = Union[rest.RecommendRequest, grpc.RecommendPoints]

from pandas import DataFrame

from app.service.build_relationships.graph_config import RelationshipGraph, EDGE_THRESHOLD


def filter_weights(edges: DataFrame, threshold: float = EDGE_THRESHOLD) -> DataFrame:
    return edges[edges[RelationshipGraph.WEIGHT] > threshold]

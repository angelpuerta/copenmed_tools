from networkx import nx
from pandas import DataFrame

from app.service.build_relationships.graph_config import RelationshipGraph, DEFAULT_DEPTH
from app.service.build_relationships.reasons import Reasons
from app.service.build_relationships.relationship_graph import filter_weights
from app.service.load.load_relationships.weights import Weights


def _to_tuple_edge(record):
    return (record[RelationshipGraph.ID_FIRST_ENTITY],
            record[RelationshipGraph.ID_SECOND_ENTITY],
            {'weight': record[RelationshipGraph.WEIGHT],
             'type': record[RelationshipGraph.ID_RELATIONSHIP_TYPE]})

class Edges:
    _edges: nx.DiGraph
    _weights: Weights

    def __init__(self, edges: DataFrame, weights: Weights):
        filtered_edges = filter_weights(edges)
        tuple_edges = filtered_edges.apply(_to_tuple_edge, axis=1)
        self._edges = nx.DiGraph(tuple_edges)
        self._weights = weights

    def get_succesors(self, node: int, depth: int = DEFAULT_DEPTH):
        return nx.dfs_successors(self._edges, source=node, depth_limit=depth)

    def get_predecessors(self, node: int, depth: int = DEFAULT_DEPTH):
        return nx.dfs_predecessors(self._edges, source=node, depth_limit=depth)

    def evaluate_succesors(self, node:int):
        return Reasons(self._edges, self._weights, node)
from networkx import nx
from pandas import DataFrame

from app.service.build_relationships.graph_config import RelationshipGraph, DEFAULT_DEPTH
from app.service.build_relationships.reasons import Reasons
from app.service.build_relationships.relationship_graph import filter_weights
from app.service.load.load_weights.weights import Weights


def _to_tuple_edge(record):
    return (record[RelationshipGraph.ID_FIRST_ENTITY],
            record[RelationshipGraph.ID_SECOND_ENTITY],
            {'weight': record[RelationshipGraph.WEIGHT],
             'type': record[RelationshipGraph.ID_RELATIONSHIP_TYPE]})


class Relations:
    _graph: nx.DiGraph
    _weights: Weights
    depth: int

    def __init__(self, edges: DataFrame, weights: Weights, depth: int = DEFAULT_DEPTH):
        filtered_edges = filter_weights(edges)
        tuple_edges = filtered_edges.apply(_to_tuple_edge, axis=1)
        self._graph = nx.DiGraph(tuple_edges)
        self._weights = weights
        self.depth = depth

    def evaluate_node(self, node: int):
        predecessors = self._graph.edge_subgraph(
            nx.bfs_tree(self._graph, node, reverse=True, depth_limit=self.depth).reverse().edges)
        successors = self._graph.edge_subgraph(nx.bfs_tree(self._graph, node, depth_limit=self.depth).edges)
        return Reasons(nx.compose(predecessors, successors), self._weights, node)

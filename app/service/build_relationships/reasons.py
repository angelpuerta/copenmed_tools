from operator import itemgetter

import networkx as nx

from app.service.build_relationships.graph_config import WeightsColumns, WEIGHTS_THRESHOLD, DEFAULT_DEPTH, \
    EDGE_THRESHOLD
from app.service.build_relationships.reason import Reason
from app.service.load.load_relationships.weights import Weights


class Reasons:
    source_node: int
    depth: int
    weights_threshold: float
    edges_threshold: float
    _weights: Weights
    successor_by_type: dict
    predecessor_by_type: dict

    def __init__(self, edges, weights: Weights, source_node: int, depth: int = DEFAULT_DEPTH,
                 weights_threshold: float = WEIGHTS_THRESHOLD, edges_threshold: float = EDGE_THRESHOLD):
        self._edges = edges
        self._weights = weights
        self.source_node = source_node
        self.weights_threshold = weights_threshold
        self.edges_threshold = edges_threshold
        self.depth = depth

    def build_successors(self):
        self.successor_by_type = {}
        successors: list = nx.dfs_successors(self._edges, source=self.source_node, depth_limit=1)[self.source_node]
        ##Do we need parallel graph in case of source ? -> (8, w:.7) -> (7, w:.3) -> (10, w:.5) <- (7, w:.6) <- source ?
        for weight_type in self._weights.get_weight_types():
            edges = []
            for nodeTo in successors:
                edges.extend(self._build_graph(self.source_node, nodeTo, weight_type, self.depth))
            if (len(edges)) != 0:
                self.successor_by_type[weight_type] = Reason(edges, self.source_node, weight_type)

    def _build_graph(self, fromNode: int, toNode: int, weight_type, depth: int, ponderated_weight: float = 1.0) -> list:
        if depth == 0:
            return []
        edge_weight, type = itemgetter("weight", "type")(self._edges.get_edge_data(fromNode, toNode))
        if ponderated_weight * edge_weight < self.edges_threshold:
            return []
        additional_weight = self._weights.get_weight(weight_type, type, WeightsColumns.WDOWN_1)
        weight = ponderated_weight * edge_weight * additional_weight
        edges = []
        if weight > self.weights_threshold:
            edges.append((fromNode, toNode, {'weight': weight, 'type': type}))
            successors = nx.dfs_successors(self._edges, source=toNode, depth_limit=1)[toNode]
            for successor in successors:
                edges.extend(self._build_graph(toNode, successor, weight_type, depth - 1, weight))
        return edges

    def get_reason_by_type(self, type) -> Reason:
        if self.successor_by_type is None:
            raise ValueError("You have not yet employed the build succesors")
        return self.successor_by_type[type]

    def __repr__(self):
        if self.successor_by_type is not None:
            return self.successor_by_type.values().__repr__()

    def to_json(self) -> dict:
        json = {}
        json["graphs"] = [value.to_json() for value in self.successor_by_type.values()]
        return json
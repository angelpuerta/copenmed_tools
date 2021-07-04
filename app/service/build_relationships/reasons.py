from collections import deque
from operator import itemgetter

import networkx as nx

from app.service.build_relationships.graph_config import WEIGHTS_THRESHOLD, EDGE_THRESHOLD, EdgeType
from app.service.build_relationships.reason import Reason
from app.service.load.load_weights.weights import Weights


class Reasons:
    source_node: int
    depth: int
    weights_threshold: float
    edges_threshold: float
    _weights: Weights
    reasons: dict
    predecessor_by_type: dict
    _graph: nx.DiGraph

    def __init__(self, edges, weights: Weights, source_node: int,
                 weights_threshold: float = WEIGHTS_THRESHOLD, edges_threshold: float = EDGE_THRESHOLD):
        self._graph = edges
        self._weights = weights
        self.source_node = source_node
        self.weights_threshold = weights_threshold
        self.edges_threshold = edges_threshold
        self.reasons = {}

    def make_explanation(self):
        successors_func = self._graph.successors
        predecessors_func = self._graph.predecessors
        for weight_type in self._weights.get_weight_types():
            explanations = []
            explanations.extend(self.build_graph(weight_type, predecessors_func, EdgeType.OUTCOMING))
            explanations.extend(self.build_graph(weight_type, successors_func, EdgeType.INCOMING))
            if len(explanations) != 0:
                subgraph = self._graph.edge_subgraph(
                    [edge['edge'] for explanation in explanations for edge in explanation['path']])
                self.reasons[weight_type] = Reason(subgraph, self.source_node, weight_type, explanations)

    def build_graph(self, weight_type, function, edge_type: EdgeType) -> dict:
        next_nodes = function(self.source_node)
        paths = []
        accumulated_paths = deque()
        for node in next_nodes:
            paths.extend(self.build_paths(weight_type, function, edge_type)(self.source_node, node, accumulated_paths))
        return paths

    def build_paths(self, weight_type, function, edge_type):

        def _build_paths(from_node, to_node, paths: deque,
                         ponderated_weight: float = 1.0) -> dict:
            to_node_path = []
            edge_weight, type = self._get_weights(edge_type, from_node, to_node)
            if ponderated_weight * edge_weight < self.edges_threshold:
                return to_node_path
            additional_weight = self._weights.get_weight(weight_type, type, edge_type)
            weight = ponderated_weight * edge_weight * additional_weight
            if weight > self.weights_threshold:
                paths.append(self._build_path(additional_weight, edge_type, from_node, to_node, weight))
                to_node_path.append(self._build_to_node_path(edge_type, paths, to_node, weight))
                next_nodes = function(to_node)
                for node in next_nodes:
                    to_node_path.extend(
                        _build_paths(to_node, node, paths, weight))
                paths.pop()
            return to_node_path

        return _build_paths

    @staticmethod
    def _build_to_node_path(edge_type, paths, to_node, weight):
        if edge_type == EdgeType.INCOMING:
            return {"path": list((paths)), "target": to_node, "weight": weight, "type": edge_type}
        else:
            if len(paths) < 2:
                outcoming_path = list(paths)
            else:
                outcoming_path = list([paths[-1]] + list(paths)[1:-1] + [paths[0]])
            return {"path": outcoming_path, "target": to_node, "weight": weight, "type": edge_type}

    @staticmethod
    def _build_path(additional_weight, edge_type, from_node, to_node, weight):
        if edge_type == EdgeType.INCOMING:
            return {"edge": (from_node, to_node), "weight_rule": additional_weight, "weight": weight}
        else:
            return {"edge": (to_node, from_node), "weight_rule": additional_weight, "weight": weight}

    def _get_weights(self, edge_type, from_node, to_node):
        if edge_type == EdgeType.INCOMING:
            edge_weight, type = itemgetter("weight", "type")(self._graph.get_edge_data(from_node, to_node))
        else:
            edge_weight, type = itemgetter("weight", "type")(self._graph.get_edge_data(to_node, from_node))
        return edge_weight, type

    def __repr__(self):
        if self.reasons is not None:
            return self.reasons.values().__repr__()

    def to_json(self) -> dict:
        json = {}
        json["graphs"] = [value.to_json() for value in self.reasons.values()]
        return json

import networkx as nx
from networkx.readwrite import json_graph;

from app.service.build_relationships.graph_config import EdgeType
from app.service.translation.translation_service import TranslationService


class Reason:
    _graph: nx.DiGraph
    translation_service: TranslationService
    source_node: int
    reason_label: str
    _paths: list

    def __init__(self, graph: nx.DiGraph,
                 source_node: int,
                 reason: str,
                 paths: list):
        self.reason = reason
        self._graph = graph
        paths.sort(key=lambda path: path['weight'], reverse=True)
        self._paths = paths
        self.source_node = source_node
        self.translation_service = TranslationService()
        nx.set_node_attributes(self._graph, {self.source_node: {type: "source"}})
        self._translate()

    def _get_terminal_nodes(self):
        return [node for node in self._graph.nodes if self._graph.out_degree(node) == 0]

    def get_terminal_paths(self) -> dict:
        terminal = self._get_terminal_nodes()
        return {key: nx.all_simple_edge_paths(self._graph, self.source_node, key) for key in terminal}

    def get_paths_to(self, nodeTo):
        return nx.all_simple_edge_paths(self._graph, self.source_node, nodeTo)

    def _translate(self):
        for node in self._graph.nodes:
            nx.set_node_attributes(self._graph, {node: {'label': self.translation_service.translate_entity(node)}})

        for node_from, node_to, dict in self._graph.edges(data=True):
            label_type = self.translation_service.translate_relationship_type(dict['type'])
            nx.set_edge_attributes(self._graph, {(node_from, node_to): {'label': label_type}})

        self.reason_label = self.translation_service.translate_relationship_supertype(self.reason)

    def to_json(self) -> dict:
        auxiliar_graph = json_graph.node_link_data(self._graph)
        graph = {}
        graph['label'] = self.reason_label
        graph['nodes'] = {value["id"]: {"label": value["label"]} for value in auxiliar_graph['nodes']}
        graph['edges'] = [
            {"source": value["source"], "label": value["label"], "target": value["target"], "directed": True,
             "weight": value["weight"]} for value in auxiliar_graph['links']]
        graph['paths'] = [{'target': path['target'], 'weight': path['weight'],
                          'type': 'incoming' if path['type'] == EdgeType.INCOMING else 'outcoming',
                          'path': self.repr_path(path)
                          } for path in self._paths]
        return {"graph": graph}

    def repr_path(self, path):
        return [{'from': edge['edge'][0], 'to': edge['edge'][1], 'weight': edge['weight'],
          'weight_rule': edge['weight_rule']} for edge in path['path']]

    def __repr__(self):
        chain = "For " + self.reason_label + "\n"
        for path in self._paths:
            chain += "For " + self._print_node(path['target']) + " :" + "\n"
            chain += "\t"
            for edge in path['path']:
                node_from = edge['edge'][0]
                node_to = edge['edge'][1]
                chain += self._print_node(node_from)
                chain += " --> "
                chain += self._print_path(node_from, node_to)
                chain += " --> "
            if path['type'] == EdgeType.INCOMING:
                chain += self._print_node(path['target'])+"\n"
            else:
                chain += self._print_node(self.source_node)+"\n"
        return chain + "\n"

    def _print_node(self, node):
        return "( " + str(node) + " : " + self._graph.nodes[node]['label'] + " )"

    def _print_path(self, nodeTo, nodeFrom):
        return "[ " + str((nodeTo, nodeFrom)) + " : " + self._graph[nodeTo][nodeFrom]['label'] + " ]"

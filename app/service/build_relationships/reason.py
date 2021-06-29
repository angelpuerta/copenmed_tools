import networkx as nx
from networkx.readwrite import json_graph;

from app.service.translation.translation_service import TranslationService


class Reason:
    _graph: nx.DiGraph
    translation_service: TranslationService
    source_node: int
    reason_label: str

    def __init__(self, edges: dict,
                 source_node: int,
                 reason: str):
        self.reason = reason
        self._graph = nx.DiGraph(edges)
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
        graph['nodes'] = {value["id"] : {"label": value["label"]} for value in auxiliar_graph['nodes']}
        graph['edges'] = [{"source": value["source"], "label": value["label"],  "target": value["target"], "directed": True, "weight": value["weight"] } for value in auxiliar_graph['links']]
        return {"graph" : graph}

    def __repr__(self):
        chain = "For " + self.reason_label + "\n"
        successors = nx.bfs_successors(self._graph, self.source_node)
        for init_node, nodes in successors:
            for node in nodes:
                chain += "\t For " + self._print_node(node) + " :" + "\n"
                for path in self.get_paths_to(node):
                    chain += "\t"
                    for nodeTo, nodeFrom in path:
                        chain += self._print_node(nodeTo)
                        chain += " --> "
                        chain += self._print_path(nodeTo, nodeFrom)
                    chain += " --> "
                    chain += self._print_node(node)
                chain += "\n"
        return chain

    def _print_node(self, node):
        return "( " + str(node) + " : " + self._graph.nodes[node]['label'] + " )"

    def _print_path(self, nodeTo, nodeFrom):
        return "[ " + str((nodeTo, nodeFrom)) + " : " + self._graph[nodeTo][nodeFrom]['label'] + " ]"

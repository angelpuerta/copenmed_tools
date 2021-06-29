import matplotlib.pyplot as plt
import networkx as nx


def draw_graph(graph:nx.Graph):
    pos = nx.spring_layout(graph)
    plt.figure()
    nx.draw(graph,pos,arrows=True, edge_color='black',width=1,linewidths=1,\
    node_size=500,node_color='pink',alpha=0.9,\
    labels={node:node for node in graph.nodes()})
    nx.draw_networkx_edge_labels(graph,pos,font_color='red')
    plt.axis('off')
    plt.show()

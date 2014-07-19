import graph
import networkx as nx
import matplotlib.pyplot as plt
from sets import Set

def calc_values(in_clique_nctbc, gr):
    values = []
    for node in gr.nodes():
        if node//10000000 == 9:
            values.append('blue')
        else:
            if node in in_clique_nctbc:
                values.append('green')
            else:
                values.append('red')
    return values

def calc_values_edges(gr):
    values = []
    for edge in gr.edges():
        if edge[0]//10000000 != 9 or edge[1]//10000000 != 9:
            values.append('red')
        else:
            values.append('blue')
    return values

def main(cdr_filename, with_graph=False):
    cdr = graph.load_cdr(cdr_filename)
    cliques = list(nx.find_cliques(cdr))
    print(cliques)
    if with_graph:
        graph1 = nx.Graph(cdr)
        nonCtbcInClique = {}
        clique_set = Set()
        for clique in cliques:
            if (len(clique) >= 3):
                for n in clique:
                    if n//10000000 != 9:
                        clique_set.add(n)
        nx.draw(graph1, node_color = calc_values(clique_set, graph1), edge_color = calc_values_edges(graph1), node_size=100, with_labels=False)
        plt.show()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Error: missing parameter CDR file')
    else:
        wg = False
        if len(sys.argv) == 3:
            wg=True
        main(sys.argv[1], with_graph=wg)

import graph
import networkx as nx

def main(cdr_filename):
    cdr = graph.load_cdr(cdr_filename)
    print(list(nx.find_cliques(cdr)))i

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('Error: missing parameter CDR file')
    else:
        main(sys.argv[1])

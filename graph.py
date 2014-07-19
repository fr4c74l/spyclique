#!/usr/bin/env python3
import networkx as nx
import re
import itertools

DUR_FACTOR = 1/300.0

SAME_PRICE = 0.10
DIFF_PRICE = 0.30

class Edge:
    __slots__ = ['orig', 'dest', 'w']
    def __init__(self, orig, dest):
        self.orig = orig
        self.dest = dest
        self.w = 0

    def is_same_op(self):
        return str(self.orig)[0] == str(self.dest)[0]

edges = {}

def load_cdr(cdr_filename):
    cdr_file = open(cdr_filename, 'r')
    parser = re.compile('(\d*) +(\d*) +(\d*)')

    for line in cdr_file:
        match = parser.match(line)
        string_row = [match.group(i) for i in [1,2,3]]
        row = [int(r) for r in string_row]

        key = tuple(row[:2])
        dur = row[2]

        try:
            e = edges[key]
        except KeyError:
            e = Edge(*key)
            edges[key] = e
        e.w += 1 + DUR_FACTOR * dur

    graph = nx.Graph()
    for key in edges.keys():
        #TODO: filter low w edges
        graph.add_edge(*key)
    return graph

def main(cdr_filename):
    cdr = load_cdr(cdr_filename)
    for clique in nx.find_cliques(cdr):
        if len(clique) < 4:
            continue
        costs = {}
        for a, b in itertools.combinations(clique, 2):
            for key in [(a, b), (b, a)]:
                try:
                    edge = edges[key]
                except KeyError:
                    if key[0] not in costs:
                        costs[key[0]] = [0.0, 0.0]
                    continue

                sameopcost = SAME_PRICE * edge.w
                if edge.is_same_op():
                    # Same operator
                    callcost = sameopcost
                else:
                    # Different operator
                    callcost = DIFF_PRICE * edge.w
                try:
                    totcost = costs[edge.orig]
                    totcost[0] += callcost # Current price
                    totcost[1] += sameopcost # Future price
                except KeyError:
                    costs[edge.orig] = [callcost, sameopcost]
        print('\n\nGrupo:', clique)
        savings = 0
        for k in costs:
            c = costs[k]
            dif = c[0] - c[1]
            print(' * %d: %.2f - %.2f = %.2f' % (k, c[0], c[1], dif))
            savings += dif
        print(' * Economia total: %.2f' % savings)
        c = input('C:\>')

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('Error: missing parameter CDR file')
    else:
        main(sys.argv[1])

#!/usr/bin/env python3
import networkx as nx
import re

DUR_FACTOR = 1/300.0

class Edge:
    __slots__ = ['a', 'b', 'w']
    def __init__(self, a, b):
        if(b < a):
            (a,b) = (b,a)
        self.a = a
        self.b = b
        self.w = 0

    def other(self, me):
        if me == self.a:
            return self.b
        return self.a

def load_cdr(cdr_filename):
    cdr_file = open(cdr_filename, 'r')
    parser = re.compile('(\d*) +(\d*) +(\d*)')

    edges = {}

    for line in cdr_file:
        match = parser.match(line)
        row = [int(match.group(i)) for i in [1,2,3]]

        key = tuple(row[:2])
        dur = row[2]

        try:
            e = edges[key]
        except KeyError:
            e = Edge(*key)
            edges[key] = e
        e.w += 1 + DUR_FACTOR * dur

    graph = nx.Graph()
    for (key, e) in edges.items():
        graph.add_edge(*key, attr_dict={'w': e.w})
    return graph

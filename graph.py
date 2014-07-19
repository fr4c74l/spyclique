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
        print(match.group(0))
        row = [int(match.group(i)) for i in [1,2,3]]

        key = tuple(row[:2])
        dur = row[2]

        try:
            e = edges[key]
        except KeyError:
            e = Edge(*key)
            edges[key] = e
        e.w += 1 + DUR_FACTOR * dur

    graph = {}
    for (key, e) in edges.items():
        for vert in key:
            try:
                graph[vert].append(e)
            except KeyError:
                graph[vert] = [e]
    return graph

def main(cdr_filename):
    cdr = load_cdr(cdr_filename)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('Error: missing parameter CDR file')
    else:
        main(sys.argv[1])

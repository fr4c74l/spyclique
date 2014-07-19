#!/usr/bin/env python3
from random import randrange as rr
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
n = 20
f = open('input.txt', 'w')

ctbcOrigN = 100
nonCtbcN = 100
ncont = 10
callsPerN = 50
ctbcNumbers = []
nonCtbcNumbers = []

for i in range(nonCtbcN):
    nonCtbcNumbers.append(rr(10000000, 90000000))

for i in range(ctbcOrigN):
    ctbcNumbers.append(rr(90000000,100000000))

for i in range(n):
    print(i)
    ctbcNumber = ctbcNumbers[rr(0, ctbcOrigN)]
    G.add_node(ctbcNumber)
    ncontacts = rr(1,ncont)
    contacts = []
    
    for j in range(ncontacts):
        contacts.append(nonCtbcNumbers[rr(0, nonCtbcN)])
    contN = rr(1, ncont)

    for j in range(ncontacts):
        c = nonCtbcNumbers[rr(0, ctbcOrigN)]
        contacts.append(c)
    
    ncalls = rr(1,callsPerN)
    for j in range(ncalls):
        dur = rr(1, 3600)
        dst = rr(0, len(contacts))
        data = '{} {} {} \n'.format(ctbcNumber, contacts[dst], dur)
        G.add_node(contacts[dst])
        G.add_edge(ctbcNumber, contacts[dst])
        f.write(data)

nx.draw(G, nx.spring_layout(G,iterations=100), node_color='b', node_size=20, with_labels=False)
plt.show()

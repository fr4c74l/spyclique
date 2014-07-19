#!/usr/bin/env python
from random import randrange as rr
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
ctbcClientsN = 100
nonCtbcClientsN = 50
f = open('input.txt', 'w')

ctbcN = 1000
nonCtbcN = 100
ncont = 10
callsPerN = 50
callCtbcPercentage = 80
ctbcNumbers = []
nonCtbcNumbers = []

val_map = {}

for i in range(nonCtbcN):
    nonCtbcNumbers.append(rr(10000000, 90000000))

for i in range(ctbcN):
    ctbcNumbers.append(rr(90000000,100000000))

for i in range(ctbcClientsN):
    ctbcNumber = ctbcNumbers[rr(0, ctbcN)]
    G.add_node(ctbcNumber, color='blue')
    val_map[ctbcNumber] = 'blue'
    ncontacts = rr(1,ncont)
    contacts = []
    
    for j in range(ncontacts):
        if (rr(0, 101) < callCtbcPercentage):
            contacts.append(ctbcNumbers[rr(0, ctbcN)])
        else:
            contacts.append(nonCtbcNumbers[rr(0, nonCtbcN)])

    ncalls = rr(1,callsPerN)
    for j in range(ncalls):
        dur = rr(1, 3600)
        dst = rr(0, ncontacts)
        data = '{} {} {}\n'.format(ctbcNumber, contacts[dst], dur)
        if (contacts[dst]//10000000 == 9):
            G.add_node(contacts[dst])
            val_map[contacts[dst]] = 'red'
        else:
            G.add_node(contacts[dst])
            val_map[contacts[dst]] = 'blue'
        G.add_edge(ctbcNumber, contacts[dst])
        f.write(data)

for i in range(nonCtbcClientsN):
    nonCtbcNumber = nonCtbcNumbers[rr(0, nonCtbcN)]
    G.add_node(nonCtbcNumber)
    val_map[nonCtbcNumber] = 'red'
    ctbcContact = ctbcNumbers[rr(0, ctbcN)]
    for j in range(ncalls):
        data = '{} {} {}\n'.format(nonCtbcNumber, ctbcContact, rr(1, 300))
        G.add_node(ctbcContact)
        val_map[ctbcContact] = 'blue'
        G.add_edge(nonCtbcNumber, ctbcContact)
        f.write(data)

values = [val_map.get(node) for node in G.nodes()]

values_edges = []
for edge in G.edges():
    if val_map[edge[0]] == 'red' or val_map[edge[1]] == 'red':
        values_edges.append('red')
    else:
        values_edges.append('blue')

nx.draw(G, nx.spring_layout(G,iterations=100), node_color = values, edge_color = values_edges, node_size=100, with_labels=False)
plt.show()

import re

from Automata import Automata
from Graph import Graph
from Link import Link, get_links
from Node import Node


def main():
    # Open stream
    stream = open("Resources/NFA.txt", "r")

    # Read from file
    AF = (re.search('\((.*)\)', (stream.readline()))).group(1).replace(' ', '').split(',')
    Q = (re.search('\{(.*)\}', (stream.readline()))).group(1).replace(' ', '').split(',')
    Sigma = (re.search('\{(.*)\}', (stream.readline()))).group(1).replace(' ', '').split(',')
    F = (re.search('\{(.*)\}', (stream.readline()))).group(1).replace(' ', '').split(',')

    # Create links
    links = []
    for line in stream:
        if line == '\n' or line == '\r\n':
            continue
        param = (re.search('\((.*)\)', line)).group(1).replace(' ', '').split(',')
        src = param[0]
        condition = param[1]
        dst = (re.search('= (.*)((,)|(\.))', line)).group(1)
        links.append(Link(src, dst, condition))
    stream.close()

    # Create the nodes
    nodes = []
    for node_id in Q:
        node_links = get_links(node_id, links)
        nodes.append(Node(node_id, node_links))
    starting_node = AF[3]

    # Create the graph
    graph = Graph(nodes, links)

    # Create the automata
    automata = Automata(graph, starting_node, F, Sigma)

    # Morari Gheorghe FAF-192
    print(automata.run('bbbbab'))
    automata.show("Resources/nfa.dot")
    automata.make_dfa()
    automata.show("Resources/dfa.dot")
    print(automata.run('bbbbab'))


main()

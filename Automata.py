from networkx.drawing.nx_pydot import write_dot

from Graph import Graph
from Link import get_links, Link
from Node import get_node, Node
import networkx as nx
import matplotlib.pyplot as plt


class Automata(Graph):
    def __init__(self, graph, starting_id, terminal_ids, conditions):
        super(Automata, self).__init__(graph.nodes, graph.links)
        self.starting_id = starting_id
        self.terminal_ids = terminal_ids
        self.conditions = conditions
        self.current_id = starting_id

    def run(self, string):
        self.current_id = self.starting_id
        for c in string:
            paths = get_links(self.current_id, self.links)
            available_paths = []
            for path in paths:
                if path.condition == c:
                    available_paths.append(path)

            if len(available_paths) == 1:
                self.current_id = available_paths[0].dst_id

            elif len(available_paths) > 1:
                print("Ambiguous transition, available paths:")
                for path in available_paths:
                    print(path.src_id, ' --', path.condition, '--> ', path.dst_id, sep='')
                return False
            else:
                print("No available paths for: ", self.current_id, ' --', c, '--> ', sep='')
                return False

        if self.current_id in self.terminal_ids:
            return True
        else:
            print("Current node", self.current_id, "is not terminal")
            return False

    def make_dfa(self):
        self.current_id = self.starting_id
        current_node = get_node(self.current_id, self.nodes)
        transition_table = {}
        self.fill_table(transition_table, self.current_id)

        new_states = []
        for key in transition_table:
            new_states.append(key)

        new_nodes = []
        new_links = []
        new_terminal_ids = []
        for state in new_states:
            state_dict = transition_table[state]
            local_links = []
            for condition in self.conditions:
                dst = state_dict[condition]
                if dst != '':
                    link = Link(state, dst, condition)
                    local_links.append(link)
                    new_links.append(link)
            new_nodes.append(Node(state, local_links))

            if state not in new_terminal_ids:
                for old_terminal_id in self.terminal_ids:
                    if old_terminal_id in state:
                        new_terminal_ids.append(state)
                        break

        new_graph = Graph(new_nodes, new_links)
        new_starting_id = self.starting_id
        new_conditions = self.conditions

        self.__init__(new_graph, new_starting_id, new_terminal_ids, new_conditions)

    def fill_table(self, table, current_id):
        if current_id not in table and current_id != "":
            current_dict = {}
            table[current_id] = current_dict
            for condition in self.conditions:
                links = get_states(current_id, self.links, condition)
                new_state = ""
                for link in links:
                    if link.dst_id not in new_state:
                        new_state += link.dst_id
                current_dict[condition] = new_state
                self.fill_table(table, new_state)

    def show(self, filename, usegraphwiz=True):
        # Morari Gheorghe FAF-192
        stream = open(filename, "w")
        print("digraph  {", file=stream)
        for node in self.nodes:
            if node.id in self.terminal_ids:
                print(node.id + " [peripheries=2];", file=stream)
            else:
                print(node.id + ";", file=stream)
        print("start -> " + self.starting_id + ";", file=stream)
        for node in self.nodes:
            for link in node.links:
                print(link.src_id + " -> " + link.dst_id + "[label=" + link.condition + "];", file=stream)
        print("}", file=stream)
        stream.close()

        if usegraphwiz:
            from graphviz import Source
            s = Source.from_file(filename)
            s.view()


def get_states(node_id, links, condition):
    ret = []
    for link in links:
        if link.src_id in node_id and link.condition in condition:
            ret.append(link)
    return ret

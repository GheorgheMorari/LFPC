# Morari Gheorghe FAF-192

class Node:
    def __init__(self, id, links):
        self.id = id
        self.links = links


def get_node(id, nodes):
    for node in nodes:
        if node.id == id:
            return node
    return None

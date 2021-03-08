# Morari Gheorghe FAF-192

class Link:
    def __init__(self, src_id, dst_id, condition):
        self.src_id = src_id
        self.dst_id = dst_id
        self.condition = condition


def get_links(node_id, links):
    ret = []
    for link in links:
        if link.src_id == node_id:
            ret.append(link)
    return ret

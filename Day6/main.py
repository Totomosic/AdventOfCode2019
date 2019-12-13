def read_map_file(file):
    with open(file, "r") as f:
        result = []
        for line in f.readlines():
            line = line.replace('\n', '').replace('\r', '')
            result.append(tuple(line.split(')')))
        return result

def find_children(data, name):
    result = []
    for pair in data:
        if pair[0] == name:
            result.append(pair)
    return result

def build_tree(data, root, parent=None):
    node = { "node" : root, "children" : [], "parent" : parent }
    children = find_children(data, root)
    for child in children:
        node["children"].append(build_tree(data, child[1], node))
    return node

def count_connections(tree, level):
    connections = 0
    for child in tree["children"]:
        connections += count_connections(child, level + 1) + level
    return connections

def find_path(tree, node):
    path = [tree["node"]]
    if tree["node"] == node:
        return path
    for child in tree["children"]:
        child_path = find_path(child, node)
        if child_path is not None:
            return path + child_path
    return None

def find_lca_path(path0, path1):
    path = []
    index = 0
    while index < len(path0) and index < len(path1):
        v0 = path0[index]
        v1 = path1[index]
        if v0 != v1:
            break
        path.append(v0)
        index += 1
    return path

def count_from_to(tree, from_node, to_node):
    start_path = find_path(tree, from_node)
    end_path = find_path(tree, to_node)
    lca_path = find_lca_path(start_path, end_path)
    return len(start_path) + len(end_path) - 2 * len(lca_path)

data = read_map_file("map.txt")
tree = build_tree(data, "COM")
#print(tree)
print(count_connections(tree, 1))
print(count_from_to(tree, "YOU", "SAN") - 2)
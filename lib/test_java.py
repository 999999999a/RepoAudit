import tree_sitter
from typing import List

JAVA_LANGUAGE = tree_sitter.Language("build/my-languages.so", "java")

parser = tree_sitter.Parser()
parser.set_language(JAVA_LANGUAGE)


def find_nodes(root_node: tree_sitter.Node, node_type: str) -> List[tree_sitter.Node]:
    """
    Find all the nodes with node_type type underlying the root node.
    :param root_node: root node
    :return the list of the nodes with node_type type
    """
    nodes = []
    if root_node.type == node_type:
        nodes.append(root_node)

    for child_node in root_node.children:
        nodes.extend(find_nodes(child_node, node_type))
    return nodes

# Read the Java file
with open("../benchmark/Java/toy/toy_NPD_single/NullPointerExceptionDemo.java", "r") as file:
    source_code = file.read()

# Parse the Java code
tree = parser.parse(bytes(source_code, "utf8"))

root = tree.root_node
all_function_nodes = []

nodes = find_nodes(root, "method_invocation")
nodes.extend(find_nodes(root, "field_access"))

for node in nodes:
    print(source_code[node.start_byte: node.end_byte])
    child_node_strs = [(child.type, source_code[child.start_byte: child.end_byte]) for child in node.children]
    print(child_node_strs)
    print("\n")

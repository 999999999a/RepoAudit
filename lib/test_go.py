import tree_sitter
from typing import List

GO_LANGUAGE = tree_sitter.Language("build/my-languages.so", "go")

parser = tree_sitter.Parser()
parser.set_language(GO_LANGUAGE)


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

# Read the  python file
with open("../benchmark/Go/toy/bof_case01.go", "r") as file:
    source_code = file.read()

# Parse the   code
tree = parser.parse(bytes(source_code, "utf8"))

root = tree.root_node
all_function_nodes = []

nodes = find_nodes(tree.root_node, "return_statement")

for retnode in nodes:
    line_number = source_code[:retnode.start_byte].count("\n") + 1
    sub_node_types = [sub_node.type for sub_node in retnode.children]
    index = 0
    if "expression_list" in sub_node_types:
        expression_list_index = sub_node_types.index("expression_list")
        for expression_node in retnode.children[expression_list_index].children:
            if expression_node.type != ",":
                print(source_code[expression_node.start_byte:expression_node.end_byte], index)
                index += 1
    else:
        print("nil", 0)
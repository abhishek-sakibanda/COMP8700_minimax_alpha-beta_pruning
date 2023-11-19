import json


class Node:
    def __init__(self, value=None, children=None):
        self.value = value
        self.children = children if children else []

    def __str__(self, level=0):
        ret = "\t" * level + f"Value: {self.value}\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret


def minimax(node, depth, maximizing_player):
    # If depth is 0 or the node has no children (Terminal Node), return the node's value
    if depth == 0 or not node.children:
        return node.value

    if maximizing_player:
        # Maximize the value for the maximizing player
        max_eval = float('-inf')
        for child in node.children:
            # Recursively call minimax for each child node with depth reduced and player switched
            eval = minimax(child, depth - 1, False)
            max_eval = max(max_eval, eval)
        node.value = max_eval
        return max_eval
    else:
        # Minimize the value for the minimizing player
        min_eval = float('inf')
        for child in node.children:
            # Recursively call minimax for each child node with depth reduced and player switched
            eval = minimax(child, depth - 1, True)
            min_eval = min(min_eval, eval)
        node.value = min_eval
        return min_eval


def alpha_beta_pruning(node, depth, alpha, beta, maximizing_player):
    # If depth is 0 or the node has no children (Terminal Node), return the node's value
    if depth == 0 or not node.children:
        return node.value

    if maximizing_player:
        # Maximize the value for the maximizing player with alpha-beta pruning
        max_eval = float('-inf')
        for child in node.children:
            # Recursively call alpha_beta_pruning for each child node with depth reduced, and player switched
            eval = alpha_beta_pruning(child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            # Prune the tree if beta is less than or equal to alpha
            if beta <= alpha:
                break
        node.value = max_eval
        return max_eval
    else:
        # Minimize the value for the minimizing player with alpha-beta pruning
        min_eval = float('inf')
        for child in node.children:
            # Recursively call alpha_beta_pruning for each child node with depth reduced, and player switched
            eval = alpha_beta_pruning(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            # Prune the tree if beta is less than or equal to alpha
            if beta <= alpha:
                break
        node.value = min_eval
        return min_eval


def load_tree_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    if isinstance(data, list):
        # For multiple trees
        return [build_tree_from_dict(tree_data) for tree_data in data]
    elif isinstance(data, dict):
        # For single trees
        return build_tree_from_dict(data)
    else:
        # Handle other cases as needed
        raise ValueError("Invalid JSON format")


def build_tree_from_dict(data: dict):
    node = Node(value=data.get('value'))
    node.children = [build_tree_from_dict(child_data) for child_data in data.get('children', [])]
    return node


# Testing with a two-ply tree
print("Two-ply tree structure:")
# Using minimax
example_tree = load_tree_from_json('two_ply_tree_structure.json')
result_minimax = minimax(example_tree, depth=2, maximizing_player=True)
print("Minimax result:", result_minimax)

# Using alpha-beta pruning
result_alpha_beta = alpha_beta_pruning(load_tree_from_json('two_ply_tree_structure.json'), depth=2, alpha=float('-inf'),
                                       beta=float('inf'),
                                       maximizing_player=True)
print("Alpha-beta pruning result:", result_alpha_beta)

# Testing with a four-ply tree
print("\nFour-ply tree structure:")
# Using minimax
for loaded_tree in load_tree_from_json('four_ply_tree_structures.json'):
    # Using minimax
    print("\nMinimax result:", minimax(loaded_tree, depth=4, maximizing_player=True))

    # Using alpha-beta pruning
    print("Alpha-beta pruning result:", alpha_beta_pruning(loaded_tree, depth=4, alpha=float('-inf'), beta=float('inf'),
                                                           maximizing_player=True))

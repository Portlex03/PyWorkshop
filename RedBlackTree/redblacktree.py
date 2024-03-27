import networkx as nx
import matplotlib.pyplot as plt
from node import Node

def root_x_pos(max_height: int) -> int:
    return sum([2**n for n in range(1, max_height)])

def root_y_pos(max_height: int) -> int:
    return 2 * (max_height - 1)

class RedBlackTree:
    def __init__(self) -> None:
        self.edges: list[tuple[Node]] = []
        self.nodes: list[Node] = []
        self.max_height = 1
        self.root = Node(
            height=self.max_height,
            position=(
                root_x_pos(self.max_height), 
                root_y_pos(self.max_height)
            )
        )
        self.nodes.append(self.root)

    @staticmethod
    def __black_root_check(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            args[0].root.color = 'Black'
        return wrapper
    
    @staticmethod
    def __tree_balance_check(func):
        def wrapper(*args, **kwargs):
            node: Node = func(*args, **kwargs)
            self: RedBlackTree = args[0]
            if self.max_height - node.height < 2 or node.father.color == 'Black':
                return node
            if node.uncle.color == 'Red':
                return self.__red_uncle_case(node)
            elif node < node.father:
                if node.father < node.grandpa:
                    return self.__right_turning(node)
                return self.__right_left_turning(node)
            elif node > node.father:
                if node.father < node.grandpa:
                    return self.__left_right_turning(node)
                return self.__left_turning(node)
        return wrapper
    
    @__tree_balance_check
    def __red_uncle_case(self, node: Node) -> Node:
        node.father.color = 'Black'
        node.uncle.color = 'Black'
        node.grandpa.color = 'Red'
        return node.grandpa

    def __add_node_and_edge(self, node: Node, edge: tuple[Node]) -> None:
        self.nodes.append(node)
        self.edges.append(edge)
    
    def __replace_edges(self, edge2replace: tuple[Node], need_edge: tuple[Node]):
        self.edges.remove(edge2replace)
        self.edges.append(need_edge)
    
    def __left_right_turning(self, node: Node) -> None:
        father = node.father
        grandpa = node.grandpa
        node_left_child = node.left_child
        self.__replace_edges((grandpa, father),(grandpa, node))
        self.__replace_edges((father, node), (node, father))
        self.__replace_edges((node, node_left_child), (father, node_left_child))
        grandpa.left_child = node
        node.father = grandpa
        father.right_child = node_left_child
        father.father = node
        node_left_child.father = father
        node.left_child = father
        self.__right_turning(father)

    def __left_turning(self, node: Node) -> None:
        head = node.grandpa.father
        grandpa = node.grandpa
        father = node.father
        father_left_child = node.father.left_child
        if not head:
            father.father = None 
            father._height = grandpa.height
            father._position = grandpa.position
            self.root = father
        else:
            head.replace_child(grandpa, father)
            father.father = head
            self.__replace_edges((head, grandpa), (head, father))
        father.color, grandpa.color = (grandpa.color, father.color)
        grandpa.right_child = father_left_child
        father_left_child.father = grandpa
        father.left_child = grandpa
        grandpa.father = father
        self.__replace_edges((grandpa, father), (father, grandpa))
        self.__replace_edges((father, father_left_child), (grandpa, father_left_child))

    def __right_left_turning(self, node: Node) ->None:
        father = node.father
        grandpa = node.grandpa
        node_right_child = node.right_child
        self.__replace_edges((grandpa, father),(grandpa, node))
        self.__replace_edges((father, node), (node, father))
        self.__replace_edges((node, node_right_child), (father, node_right_child))
        grandpa.right_child = node
        node.father = grandpa
        father.left_child = node_right_child
        father.father = node
        node_right_child.father = father
        node.right_child = father
        self.__left_turning(father)

    def __right_turning(self, node: Node) -> None:
        head = node.grandpa.father
        grandpa = node.grandpa
        father = node.father
        father_right_child = node.father.right_child
        if not head:
            father.father = None
            father._height = grandpa.height
            father._position = grandpa.position
            self.root = father
        else:
            head.replace_child(grandpa, father)
            father.father = head
            self.__replace_edges((head, grandpa), (head, father))
        father.color, grandpa.color = (grandpa.color, father.color)
        grandpa.left_child = father_right_child
        father_right_child.father=grandpa
        father.right_child = grandpa
        grandpa.father = father
        self.__replace_edges((grandpa, father), (father, grandpa))
        self.__replace_edges((father, father_right_child), (grandpa, father_right_child))
    
    @property
    def node_colors(self) -> list[str]:
        return [node.color for node in self.nodes]
    
    @property
    def node_positions(self) -> dict[int, tuple]:
        node_positions = {}
        for node in self.nodes:
            node_positions[node] = node.position
        return node_positions

    @__black_root_check
    @__tree_balance_check
    def add_node(self, value: int) -> Node:
        node, height = self.root, 1
        while node:
            node = node.left_child if value < node else node.right_child
            height += 1
        node.color, node.value = 'Red', value
        self.__add_node_and_edge(node.left_child, (node, node.left_child))
        self.__add_node_and_edge(node.right_child, (node, node.right_child))
        if height > self.max_height:
            self.max_height = height
            self.root.height = self.max_height
            self.root.position = (
                root_x_pos(self.max_height), 
                root_y_pos(self.max_height)
            )
        return node

    def add_nodes_from(self, values_list: list) -> None:
        for value in values_list:
            self.add_node(value)

    def image(self,
        font_size: int = 14, 
        node_size: int = 2000, 
        figsize=(6, 6), 
        margins: float = 0.4
    ) -> plt.Figure:
        g = nx.DiGraph()
        g.add_nodes_from(self.nodes)
        g.add_edges_from(self.edges)
        options = {
            "edgecolors": "black",
            "font_color": "white",
            "font_size": font_size,
            "node_color": self.node_colors,
            "node_size": node_size,
            "width": 4,
        }
        figure = plt.figure(figsize=figsize)
        plt.margins(margins)
        nx.draw_networkx(g, pos=self.node_positions, **options)
        return figure

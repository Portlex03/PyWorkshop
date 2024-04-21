import networkx as nx
from node import Node
from color import Color

class RedBlackTree:
    def __init__(self):
        self.root: Node = Node()
        self.nodes: dict[int, Node] = {hash(self.root): self.root}

    def __balance(self, node: Node):
        if node.grandpa and node.father.is_red:
            if node.uncle.is_red:
                node.father.color = Color.Black
                node.uncle.color = Color.Black
                node.grandpa.color = Color.Red
                self.__balance(node.grandpa)
            elif node.father < node.grandpa:
                self.__LLturn(node)
            elif node.father > node.grandpa:
                self.__RRturn(node)
        self.root.color = Color.Black
        self.root.set_position(len(self.nodes))

    def __black_list_case(self, node: Node):
        brother = node.brother
        if not brother:
            return
        if brother.is_black:
            if brother.left.is_black and brother.right.is_black:
                brother.color = Color.Red
                if brother.father.is_red:
                    brother.father.color = Color.Black
                else:
                    self.__black_list_case(node.father)
            elif brother.is_left:
                if brother.right.is_red:
                    self.__RRturn(brother.right.right)
                brother.left.color = Color.Black
                self.__LLturn(brother.left)
            else:
                if brother.left.is_red:
                    self.__LLturn(brother.left.left)
                brother.right.color = Color.Black
                self.__RRturn(brother.right)
        else:
            if brother.is_left:
                self.__LLturn(brother.left)
            else:
                self.__RRturn(brother.right)
            self.__black_list_case(node)

    def __LLturn(self, node: Node):
        if node and node > node.father:
            self.__RRturn(node.right)
        father = node.father
        grandpa = node.grandpa
        uncle = node.uncle
        father_right = father.right
        father.value, grandpa.value = grandpa.value, father.value
        grandpa.right = grandpa.left
        grandpa.left = node
        father.right = uncle
        father.left = father_right
        uncle.father = father
        node.father = grandpa

    def __RRturn(self, node: Node):
        if node and node < node.father:
            self.__LLturn(node.left)
        father = node.father
        grandpa = node.grandpa
        uncle = node.uncle
        father_left = father.left
        father.value, grandpa.value = grandpa.value, father.value
        grandpa.left = grandpa.right
        grandpa.right = node
        father.left = uncle
        father.right = father_left
        uncle.father = father
        node.father = grandpa

    def insert(self, value: int):
        node = self.search(value)
        if node: 
            raise ValueError(f'Value {value} already exists in the tree')
        node.value = value
        node.color = Color.Red
        self.nodes[hash(node.right)] = node.right
        self.nodes[hash(node.left)] = node.left
        self.__balance(node)

    def insert_from(self, values: list[int]):
        for value in values:
            self.insert(value)

    def delete(self, obj: int | Node):
        node = obj if isinstance(obj, Node) else self.search(obj)
        if not node:
            raise ValueError(f'Value {obj} not exists in tree')
        elif node.children_count == 0:
            if node.is_black:
                self.__black_list_case(node)
            self.nodes.pop(hash(node.left))
            self.nodes.pop(hash(node.right))
            node.value = None
        elif node.children_count == 1:
            node_child = node.left or node.right
            node.value, node_child.value = node_child.value, node.value
            self.delete(node_child)
        elif node.children_count == 2:
            max_right_child = node.left
            while max_right_child.right:
                max_right_child = max_right_child.right
            node.value = max_right_child.value
            self.delete(max_right_child)
        self.root.set_position(len(self.nodes))

    def delete_from(self, values: list[int]):
        for value in values:
            self.delete(value)

    def search(self, value: int) -> Node:
        node = self.root
        while node and node != value:
            node = node.child(value)
        return node

    def realize(self):
        g = nx.DiGraph()
        g.add_nodes_from(self.nodes.values())
        g.add_edges_from(self.edges)
        options = {
            "edgecolors": "black",
            "font_color": "white",
            "font_size": 7,
            "node_color": self.colors,
            "node_size": 350,
            "width": 4,
        }
        return g, self.positions, options

    @property
    def colors(self) -> list[str]:
        return [node.color.value for node in self.nodes.values()]

    @property
    def edges(self) -> list[tuple[Node]]:
        return [(node, child) for node in self.nodes.values() for child in [node.right, node.left] if node]

    @property
    def positions(self) -> dict[Node, tuple[int]]:
        return {node: node.position.value for node in self.nodes.values()}

from position import Position
from color import Color
import math

class Node:
    def __init__(self, father=None) -> None:
        self.color = Color.Black
        self.father: Node | None = father
        self.left: Node | None = None
        self._position: Position | None = None
        self.right: Node | None = None
        self._value: int | None = None

    def __bool__(self) -> bool:
        return bool(self.value) or self.value == 0

    def __eq__(self, obj) -> bool:
        if isinstance(obj, Node):
            return self.value == obj.value if self or obj else self is obj
        elif isinstance(obj, int):
            return self.value == obj
        return False

    def __gt__(self, obj) -> bool:
        if not isinstance(obj, (Node, int)):
            raise ValueError('Object {} not in [Node, int] type'.format(obj))
        return self.value > obj.value if isinstance(obj, Node) else self.value > obj

    def __hash__(self) -> int:
        return object.__hash__(self)

    def __lt__(self, obj) -> bool:
        if not isinstance(obj, (Node, int)):
            raise ValueError('Object {} not in [Node, int] type'.format(obj))
        return self.value < obj.value if isinstance(obj, Node) else self.value < obj

    def __repr__(self) -> str:
        if self:
            return f'<{self.color.name}.Node: {self.value}>'
        elif self.father:
            side = 'Left' if self.is_left else 'Right'
            return f'<{side}.List(father={self.father.value})>'
        return '<Empty root>'

    def __str__(self) -> str:
        return str(self.value) if self else 'n'

    def child(self, value: int):
        return self.left if value < self else self.right

    @property
    def brother(self):
        if not self.father:
            return None
        return self.father.right if self.is_left else self.father.left

    @property
    def children_count(self) -> int:
        return bool(self.right) + bool(self.left)

    @property
    def grandpa(self):
        return self.father.father if self.father else None

    @property
    def is_black(self) -> bool:
        return self.color == Color.Black

    @property
    def is_left(self) -> bool:
        return bool(self.father) and self is self.father.left

    @property
    def is_red(self) -> bool:
        return self.color == Color.Red

    @property
    def position(self) -> Position:
        if not self.father:
            return self._position
        left = (-1)**self.is_left
        pos = self.father.position.value
        return pos + Position(left * 2**(pos[1] - 1), -1)
    
    def set_position(self, count: int):
        height = int(2 * math.log2(count + 1))
        self._position = Position(2**height - 1, height)

    @property
    def uncle(self):
        return self.father.brother if self.father else None

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        self._value = value if isinstance(value, int) else None
        if self:
            self.left = self.left if self.left != None else Node(father=self)
            self.right = self.right if self.right != None else Node(
                father=self)
        else:
            self.color = Color.Black
            self.left = None
            self.right = None

from position import Position
from color import Color

class Node:
    Height = 1
    Pos = Position(0, 0)

    def __init__(self, father=None) -> None:
        self.color = Color.Black
        self.father: Node | None = father
        self.left: Node | None = None
        self.right: Node | None = None
        self._value: int | None = None

    def __bool__(self) -> bool:
        return bool(self.value)

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
    def height(self):
        return Node.Height if not self.father else self.father.height - 1

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
        return Node.Pos if not self.father else self.father.position + ((-1)**self.is_left * 2**(self.father.height - 1), -2)

    @property
    def uncle(self):
        return self.father.brother if self.father else None

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        self._value = value if isinstance(value, int) else None
        if self._value:
            self.left = self.left if self.left != None else Node(father=self)
            self.right = self.right if self.right != None else Node(
                father=self)
        else:
            self.color = Color.Black
            self.left = None
            self.right = None

class Node:
    def __init__(self, 
        father = None, 
        height: int | None = None, 
        position: tuple[int] | None = None,
        value: int | None = None
    ) -> None:
        self.color = 'Black'
        self.father: Node | None = father
        self._height: int | None = height
        self.left_child: Node | None = None
        self._position: tuple[int] | None = position
        self.right_child: Node | None = None
        self._value: int | None = value

    def __bool__(self) -> bool:
        return bool(self.value)
    
    def __gt__(self, obj) -> bool:
        value = obj.value if isinstance(obj, Node) else obj
        return self.value > value
    
    def __lt__(self, obj) -> bool:
        value = obj.value if isinstance(obj, Node) else obj
        return self.value < value
    
    def __repr__(self) -> str:
        return f'<{self.color}.Node: {self.value}>'

    def __str__(self) -> str:
        return str(self.value) if self else 'n'
    
    @property
    def grandpa(self):
        return self.father.father if self.father else None

    @property
    def height(self):
        if self.father:
            self._height = self.father.height - 1
        return self._height
    
    @property
    def is_left_child(self) -> bool:
        if not self.father:
            return False
        return self is self.father.left_child

    @property 
    def position(self):
        if self.father:
            pos_x, pos_y  = self.father.position
            self._position = (
                pos_x + (-1)**self.is_left_child * 2**(self.father.height - 1),
                pos_y - 2
            )
        return self._position
    
    @property
    def uncle(self):
        if not self.grandpa:
            return None
        elif self.father.is_left_child:
            return self.grandpa.right_child
        return self.grandpa.left_child

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value) -> None:
        if not value: 
            raise ValueError('Нет значения value')
        self.left_child = Node(father=self)
        self.right_child = Node(father=self)
        self._value = value

    def replace_child(self, child2replace, need_child) -> None:
        if child2replace.is_left_child:
            self.left_child = need_child
        else:
            self.right_child = need_child

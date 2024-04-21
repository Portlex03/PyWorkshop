class Position:
	def __init__(self, x: int, y: int) -> None:
		self.x = x
		self.y = y

	def __radd__(self, obj):
		if isinstance(obj, Position):
			return Position(self.x + obj.x, self.y + obj.y)
		elif isinstance(obj, tuple):
			return Position(self.x + obj[0], self.y + obj[1])
		raise TypeError(f'unsupported operand type(s) for +: Position and {type(obj)}')
		
	def __repr__(self) -> str:
		return f'<Position{self.value}>'

	@property
	def value(self) -> tuple:
		return (self.x, self.y)
	
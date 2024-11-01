class Piece:
	def __init__(self, pos, color, board):
		self.notation = None
		self.pos = pos
		self.x = pos[0]
		self.y = pos[1]
		self.board = board
		self.color = color
		self.has_moved = False

	def move(self, board, square, force=False):
		for i in board.squares:
			i.highlight = False

		from data.classes.pieces.Dragon import Dragon
		from data.classes.pieces.Nuclear import Nuclear
		attacked_piece = square.occupying_piece
		print(attacked_piece)

		if attacked_piece is not None and attacked_piece.color == self.color:
			print("Cannot attack an allied piece")
			board.selected_piece = None
			return False

		prev_square = board.get_square_from_pos(self.pos)

		if isinstance(attacked_piece, Nuclear):
			if attacked_piece.eat_nuclear():
				print("It's a draw!")
				board.game_result = "draw"
				return True
		else:
			square.occupying_piece = attacked_piece

		if isinstance(attacked_piece, Dragon):
			if attacked_piece.take_damage():
				print(f'Dragon defeated: {attacked_piece}')
				board.remove_piece(attacked_piece)
				square.occupying_piece = self
				board.switch(square)
				prev_square.occupying_piece = None
			else:
				print(f'Dragon injured: {attacked_piece}')
				self.pos, self.x, self.y = prev_square.pos, prev_square.x, prev_square.y
				self.has_moved = True
				board.switch(square)
				return False

		else:
			square.occupying_piece = attacked_piece

		if square in self.get_valid_moves(board) or force:
			self.pos, self.x, self.y = square.pos, square.x, square.y
			prev_square.occupying_piece = None
			square.occupying_piece = self
			board.selected_piece = None
			self.has_moved = True
			if self.notation == ' ':
				if self.y == 0 or self.y == 7:
					from data.classes.pieces.Queen import Queen
					square.occupying_piece = Queen(
						(self.x, self.y),
						self.color,
						board
					)

			# Логика рокировки
			if self.notation == 'K':
				if prev_square.x - self.x == 2:
					rook = board.get_piece_from_pos((0, self.y))
					rook.move(board, board.get_square_from_pos((3, self.y)), force=True)
				elif prev_square.x - self.x == -2:
					rook = board.get_piece_from_pos((7, self.y))
					rook.move(board, board.get_square_from_pos((5, self.y)), force=True)

			return True
		else:
			board.selected_piece = None
			return False

	def get_moves(self, board):
		output = []
		for direction in self.get_possible_moves(board):
			for square in direction:
				if square.occupying_piece is not None:
					if square.occupying_piece.color == self.color:
						break
					else:
						output.append(square)
						break
				else:
					output.append(square)

		return output

	def get_valid_moves(self, board):
		output = []
		for square in self.get_moves(board):
			if not board.is_in_check(self.color, board_change=[self.pos, square.pos]):
				output.append(square)

		return output

	def attacking_squares(self, board):
		return self.get_moves(board)

	"""
		Чтобы не было ошибки Unresolved attribute reference 'get_possible_moves' for class 'Piece',
		а то некрасиво (Нужно, чтобы было красиво)
	"""
	def get_possible_moves(self, board):
		pass

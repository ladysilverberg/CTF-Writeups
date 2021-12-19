from pwn import *
import copy

class NKQueenSolver:
	def __init__(self, N, board=None):
		self.N = N
		if board:
			self.board = board
		else:
			self.board = self.generate_board()
		self.solutions = []
		self.solution_idx = 0
		self.top_layers = []
	
	def add_top_layer(self, layer):
		self.top_layers.append(layer)
	
	def get_next_solution(self):
		if len(self.solutions) > self.solution_idx:
			idx = self.solution_idx
			self.solution_idx += 1
			return self.solutions[idx]
		return None
	
	def solve(self):
		return self.solve_nk_queens(self.board, 0)
			
	def print_board(self, board=None):
		if not board:
			board = self.board
		for row in board:
			print(row)
	
	def generate_board(self):
		board = []
		for i in range(self.N):
			board.append([0 for i in range(self.N)])
		return board
		
	def is_safe(self, board, row, col):
		# Check top layers for opposing queens
		for layer in self.top_layers:
			if layer[row][col] >= 1:
				return False
	
		# Check entire row for queens
		for i in range(self.N):
			if board[row][i] >= 1:
				return False
	 
		# Upper Diagonal (Left Side)
		for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
			if board[i][j] >= 1:
				return False
				
		# Upper Diagonal (Right Side)
		for i, j in zip(range(row, -1, -1), range(col, self.N, 1)):
			if board[i][j] >= 1:
				return False
	 
		# Lower Diagonal (Left Side)
		for i, j in zip(range(row, self.N, 1), range(col, -1, -1)):
			if board[i][j] >= 1:
				return False
	 
		# Lower Diagonal (Right Side)
		for i, j in zip(range(row, self.N, 1), range(col, self.N, 1)):
			if board[i][j] >= 1:
				return False
	 
		return True
		
	def solve_nk_queens(self, board, col):
		# Base Case: all queens placed
		if col >= self.N:
			sol = copy.deepcopy(board)
			self.solutions.append(sol)
			return True
	 
		# Check if column has preplaced queen
		preplaced = False
		for i in range(self.N):
			if board[i][col] == 2:
				preplaced = True
				break
	 
		# Try placing queen in all rows one by one
		res = False
		for i in range(self.N):
			if preplaced:
				if self.solve_nk_queens(board, col+1):
					return True
			elif self.is_safe(board, i, col):
				board[i][col] = 1
				res = self.solve_nk_queens(board, col+1) or res
				board[i][col] = 0
		return res


 
def print_layers(layers):
	for layer in layers:
		for row in layer:
			print(row)
		print("---")
 
def assemble_layers(board, N):
    layers = []
    for b in board:
        layer = []
 
        for i in range(N):
            layer.append([0 for i in range(N)])
 
        for row in range(N):
            col = b[row]
            if col > 0:
                layer[row][col-1] = 2
        layers.append(layer)
    return layers

def assemble_solution(layers):
	solution_str = ""
	for layer in layers:
		for row in layer:
			cnt = 0
			for num in row:
				cnt+=1
				if num > 0:
					solution_str += str(cnt)
					solution_str += ","
		solution_str = solution_str[0:len(solution_str)-1] + " "
	solution_str = solution_str[0:len(solution_str)-1]
	return solution_str

def solve(board):
	N = len(board[0])
	layers = assemble_layers(board, N)

	# Start by top layer, work downwards
	has_solution = solve_next_layer(N, layers, 0)
	print("DONE! Result:", has_solution)
	print_layers(layers)
	
	# Translate Layer format to what remote expects
	sol = assemble_solution(layers)
	return sol

def solve_next_layer(N, layers, layer_id):
	# Base Case - no more layers
	if layer_id >= len(layers):
		return True

	solver = NKQueenSolver(N, layers[layer_id])
	
	# Add Top Layers
	tl_id = 0
	while tl_id != layer_id:
		solver.add_top_layer(layers[tl_id])
		tl_id+=1
	
	# No Solutions - Top layers must be wrong
	if not solver.solve():
		return False
	
	# Recursively try all solutions
	layers[layer_id] = solver.get_next_solution()
	while not solve_next_layer(N, layers, layer_id+1):
		next = solver.get_next_solution()
		if next is None:
			return False
		layers[layer_id] = next
	return True


 
r = remote("io.ept.gg", 30042)
 
while True:
	out = r.recvuntil(b"Your 3d board is:\n", timeout=.5)
	if len(out) == 0:
		print(out)
		break
	board = r.recvline().decode().strip()
	board = eval(board)
	solution = solve(board)
	print(solution)
	r.readrepeat(.2)
	r.sendline(solution)
out = r.readrepeat(.2)
print(out)
class Points:
	def __init__(self, xcord, ycord):
		self.x = xcord;
		self.y = ycord;

class Board:
	def _init_(self, num_agents = 3, xr = Points(0, 0), yr = Points(2, 2)):
		self.startRange = xr
		self.endRange = xy
		self.agents = []
		self.actions = []
		self.collision = []
		self.step = 0

		for x in range(0, num_agents):	
			self.agents.append(self.generate_agent());

	def generate_agent(self, board):
		we_good = False
		newAgent = Agent(board, Points(random.randint(self.startRange.x, self.endRange.x),random.randint(self.startRange.y, self.endRange.y)), Points(random.randint(self.startRange.x, self.endRange.x),random.randint(self.startRange.y, self.endRange.y)))
		
		while not we_good:
			count = -1
			for agent in self.agents:
				if (agent.pos.x == newAgent.pos.x) and (agent.pos.y == newAgent.pos.y):
					newAgent.pos = Points(random.randint(self.startRange.x, self.endRange.x),random.randint(self.startRange.y, self.endRange.y))
					count = count + 1
				elif (agent.goal.x == newAgent.goal.x) and (agent.goal.y == newAgent.goal.y):
					newAgent.goal = Points(random.randint(self.startRange.x, self.endRange.x),random.randint(self.startRange.y, self.endRange.y))
					count = count + 1
				else:
					if count == -1:
						we_good = True

	def step_path():
		self.step = self.step + 0
		
		#self.collision.append

class Agent:
	def _init_(self, board, posShow, goalShow):
		self.pos = posShow
		self.goal = goalShow
		self.board = board
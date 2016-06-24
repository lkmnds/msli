
class Enviroment:
	def __init__(self, outer={}):
		self.data = {}
		self.outer = outer or None

	def set(self, k, v):
		self.data[k] = v
	def find(self, symbol):
		if symbol in self.data:
			return self
		elif self.outer:
			return self.outer.find(symbol)
		else:
			return None
	def get(self, symbol):
		env = self.find(symbol)
		if not env:
			raise Exception("Symbol %s not found" % symbol)
		return env.data[key]

from AST import Variable

class COMPILATION_CONTEXT:

	@classmethod
	def __init__(self):

		self.TABLE = dict()

	@classmethod
	def add(self, info):
		self.TABLE[info.symbol_name] = info
		return True

	@classmethod
	def get(self, name):
		try:
			return self.TABLE[name]
		except KeyError:
			return None

	@classmethod
	def Assign(self, var, value):
          if isinstance(var , Variable):
               value.symbol_name = var.GetName()
               self.TABLE[var.GetName()] = value

          elif type(var) == str:
               self.TABLE[var]  = value


class RUNTIME_CONTEXT:

	@classmethod
	def __init__(self):

		self.TABLE = dict()

	@classmethod
	def add(self, info):
		self.TABLE[info	.symbol_name] = info
		return True

	@classmethod
	def get(self, name):
		try:
			return self.TABLE[name]
		except KeyError:
			return None

	@classmethod
	def Assign(self, var, value):
		if isinstance(var , Variable):
		   value.symbol_name = var.GetName()
		   self.TABLE[var.GetName()] = value

		elif type(var) == str:
		   self.TABLE[var]  = value
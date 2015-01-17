from AST import *

class COMPILATION_CONTEXT:

	def __init__(self):

		self.TABLE = dict()

	def add(self, info):
		self.TABLE[info.symbol_name] = info
		return True

	def get(self, name):
		try:
			return self.TABLE[name]
		except KeyError:
			return None

	def GetSymbolTable(self):
		return self.TABLE

	def Assign(self, var, value):

          if isinstance(var , Variable):
               value.symbol_name = var.GetName()
               self.TABLE[var.GetName()] = value

          elif type(var) == str:
               self.TABLE[var]  = value


class RUNTIME_CONTEXT:

	def __init__(self, program=None):

		self.TABLE = dict()
		self._prog = program

	def add(self, info):
		self.TABLE[info	.symbol_name] = info
		return True

	def get(self, name):
		try:
			return self.TABLE[name]
		except KeyError:
			return None

	def Assign(self, var, value):
		from AST import Variable
		if isinstance(var , Variable):
		   value.symbol_name = var.GetName()
		   self.TABLE[var.GetName()] = value

		elif type(var) == str:
		   self.TABLE[var]  = value

	def GetProgram(self):
		return self._prog
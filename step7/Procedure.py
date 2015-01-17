from AST import TYPE_INFO

class  Procedure:

	def __init__(self, name, formals, statements, locs, t):
		self.name = name
		self.formals = formals
		self.statements = statements
		self.locals = locs
		self._type = t

	def GetName(self):
		return self.name

	def GetFormals(self):
		return self.formals

	def GetType(self):
		self._type

	def ReturnValue(self):
		return self.return_value

	def TypeCheck(self, com_cntxt):
		return TYPE_INFO.TYPE_NUMERIC

	def Execute(self, run_cntxt, actuals):
		variables = []
		i = 0
		if self.formals and actuals:
			for o in self.formals:
				inf = actuals[i]
				inf.symbol_name = o.symbol_name
				run_cntxt.add(inf)
				i += 1
		for s in self.statements:
			return_value = s.Execute(run_cntxt)
			if return_value:
				return return_value
		return None

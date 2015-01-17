from abc import ABCMeta, abstractmethod

class CompilationUnit:
	__metaclass__ = ABCMeta

	@classmethod
	def Excecute(run_cntxt, actuals):
		pass

class TModule(CompilationUnit):

	def __init__(self, procs):
		self.procs = procs

	def Execute(self, run_cntxt, actuals):

		p = self.Find("Main")

		if p:
			return p.Execute(run_cntxt, actuals)

		return None

	def Find(self, name):

		for p in self.procs:
			pname = p.GetName()
			if pname.upper() == name.upper():
				return p
		return None
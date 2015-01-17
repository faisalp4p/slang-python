from abc import ABCMeta, abstractmethod
from CompilationUnit import TModule
from AST import TYPE_INFO
from Procedure import Procedure

class FunctionInfo:

	def __init__(self, name, ret_val, formals):

		self._ret_value = ret_val
		self._type_info = formals
		self._name = name



class Builder:
	__metaclass__ = ABCMeta


class ProcedureBuilder(Builder):

	def __init__(self, name, com_cntxt):
		self.ctx = com_cntxt
		self.proc_name = name
		self.type_info = TYPE_INFO.TYPE_ILLEGAL
		self.statements = []
		self.formals = []

	def AddLocal(self, info):
		self.ctx.add(info)
		return True

	def add(self, info):
		self.ctx.add(info)
		return True

	def get(self, name):
		return self.ctx.get(name)

	def AddFormals(self, info):
		self.formals.append(info)

	def TypeCheck(self, exp):
		return exp.TypeCheck(self.ctx)

	def AddStatement(self, statement):
		self.statements.append(statement)

	def GetSymbol(self, name):
		return self.ctx.get(name)

	def CheckProto(name):
		return True

	def GetTypeInfo(self):
		return self.type_info

	def SetTypeInfo(self, info):
		self.type_info = info

	def GetSymbolTable(self):
		return self.ctx.TABLE

	def GetContext(self):
		return self.ctx

	def SetProcedureName(self, name):
		self.proc_name = name

	def GetProcedureName(self):
		return self.proc_name

	def GetProcedure(self):
		proc = Procedure(self.proc_name, self.formals, self.statements, self.ctx, self.type_info)
		return proc


class TModuleBuilder(Builder):

	def __init__(self):

		self.protos = []
		self.procs = []

	def IsFunction(self, name):

		for p in self.protos:
			if p._name == name:
				return True
		return False

	def AddFunctionProtoType(self, name, ret_type, type_infos):
		info = FunctionInfo(name, ret_type, type_infos)
		self.protos.append(info)

	def CheckFunctionProtoType(name, ret_type, type_infos):

		for p in self.protos:
			if p._name == name:
				if p._ret_type == ret_type:
					if type_info.size() == p._type_info.size():
						for i in xrange(type_infos.size()):
							a = type_infos[i]
							b = type_infos[i]
							if a != b:
								return False
						return True
		return False

	def Add(self, p):
		self.procs.append(p)

	def GetProgram(self):
		return TModule(self.procs)

	def GetProc(self, name):
		for p in self.procs:
			if p.GetName() == name:
				return p
		return None

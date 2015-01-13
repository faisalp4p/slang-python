from abc import ABCMeta, abstractmethod

from AST import Variable

class Statement:
     __metaclass__ = ABCMeta

     @abstractmethod
     def Execute(self): pass

class PrintStatement(Statement):

    def __init__(self, ex):
        self._ex = ex

    def Execute(self, run_cntxt):
        a = self._ex.Evaluate(run_cntxt)
        print a.val,
        return True

class PrintLineStatement(Statement):

    def __init__(self, ex):
        self._ex = ex


    def Execute(self, run_cntxt):
        a = self._ex.Evaluate(run_cntxt)
        print a.val
        return True



class VariableDeclStatement(Statement):

     def __init__(self, info):
          self.sym_info =  info
          

     def Execute(self, run_cntxt):
          run_cntxt.add(self.sym_info)
          self.var = Variable(self.sym_info)


class AssignmentStatement(Statement):

     def __init__(self, var, ex):
          self.variable = Variable(info=var)
          self.ex = ex


     def Execute(self, run_cntxt):
          
          val = self.ex.Evaluate(run_cntxt)
          run_cntxt.Assign(self.variable, val)
          return None

# class SymbolTable:

#      def __init__(self):
#           self.dt = dict()


#      def add(self, info):
#           self.dt[info.symbol_name] = info
#           return True

#      def get(self, name):
#           return self.dt[name]

#      def Assign(self, var, value):
#           if isinstance(var , Variable):
#                value.symbol_name = var.GetName()
#                self.dt[var.GetName()] = value

#           elif type(var) == str:
#                self.dt[var]  = value


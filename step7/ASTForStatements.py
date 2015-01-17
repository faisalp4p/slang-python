from abc import ABCMeta, abstractmethod
from AST import TYPE_INFO

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
        return None

class PrintLineStatement(Statement):

    def __init__(self, ex):
        self._ex = ex


    def Execute(self, run_cntxt):
        a = self._ex.Evaluate(run_cntxt)
        print a.val
        return None



class VariableDeclStatement(Statement):

     def __init__(self, info):
          self.sym_info =  info
          

     def Execute(self, run_cntxt):
          run_cntxt.add(self.sym_info)
          self.var = Variable(self.sym_info)
          return None


class AssignmentStatement(Statement):

     def __init__(self, var, ex):
          self.variable = Variable(info=var)
          self.ex = ex

     def Execute(self, run_cntxt):
          
          val = self.ex.Evaluate(run_cntxt)
          run_cntxt.Assign(self.variable, val)
          return None


class IfStatement(Statement):

    def __init__(self, cond, then_list, else_list):

        self.cond = cond
        self.then_statement_list = then_list
        self.else_statement_list = else_list

    def Execute(self, run_cntxt):

        m_cond = self.cond.Evaluate(run_cntxt)

        if m_cond == None or m_cond.type != TYPE_INFO.TYPE_BOOL:
            return None

        if m_cond.val == True:
            for statement in self.then_statement_list:
                ret = statement.Execute(run_cntxt)
                if ret:
                	return ret
        else:
            for statement in self.else_statement_list:
                ret = statement.Execute(run_cntxt)
                if ret:
                	return ret
        return None


class WhileStatement(Statement):

    def __init__(self, cond, statement_list):
        self.cond = cond
        self.statement_list = statement_list

    def Execute(self, run_cntxt):

        m_cond = self.cond.Evaluate(run_cntxt)
        if m_cond == None or m_cond.type != TYPE_INFO.TYPE_BOOL:
            return None

        while m_cond.val:
          for statement in self.statement_list:
              ret = statement.Execute(run_cntxt)
              if ret:
              	return ret
          m_cond = self.cond.Evaluate(run_cntxt)

        return None

class ReturnStatement(Statement):

    def __init__(self, exp):
        self._exp = exp

    def Execute(self, run_cntxt):

        inf = None if not self._exp else self._exp.Evaluate(run_cntxt)
        return inf
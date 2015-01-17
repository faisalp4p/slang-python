from abc import ABCMeta, abstractmethod

from Lexer import RELATIONAL_OPERATOR

from contexts import *

class OPERATOR:
     PLUS = "+"
     MINUS = "-"
     DIV = "/"
     MUL = "*"


class TYPE_INFO:
    TYPE_ILLEGAL = -1
    TYPE_NUMERIC = 0
    TYPE_BOOL = 1
    TYPE_STRING = 2


class SYMBOL_INFO:

    def __init__(self, symbol_name=None, type=None, val=None):

        self.symbol_name = symbol_name
        self.type = type
        self.val = val




class Exp:
     __metaclass__ = ABCMeta
     
     @abstractmethod
     def Evaluate(self): pass

     @abstractmethod
     def TypeCheck(self): pass

     @abstractmethod
     def GetType(self): pass


class BooleanConstant(Exp):

     def __init__(self, pvalue):
          self.info = SYMBOL_INFO(symbol_name=None,
                                  val=pvalue,
                                  type=TYPE_INFO.TYPE_BOOL)


     def Evaluate(self, run_cntxt):
          return self.info


     def TypeCheck(self, run_cntxt):
          return self.info.type

     def GetType(self):
          return self.info.type


class NumericConstant(Exp):
     
     def __init__(self, value):
          self.info = SYMBOL_INFO(symbol_name=None,
                                  val=value,
                                  type=TYPE_INFO.TYPE_NUMERIC)



     def Evaluate(self, run_cntxt):
          return self.info

     def TypeCheck(self, run_cntxt):
          return self.info.type

     def GetType(self):
          return self.info.type

     def __str__(self):
          return u'NumericConstant(%d)' % self.info.val


class StringLiteral(Exp):
     
     def __init__(self, pvalue):

          self.info = SYMBOL_INFO(symbol_name=None,
                                  val=pvalue,
                                  type=TYPE_INFO.TYPE_STRING)

     def Evaluate(self, run_cntxt):
          return self.info


     def TypeCheck(self, run_cntxt):
          return self.info.type

     def GetType(self):
          return self.info.type


class Variable(Exp):
     
     def __init__(self, info=None, com_cntxt=None, name=None, _val=None):
          
          if info:
               self.var_name = info.symbol_name
               return
          if type(_val) in [int, long]:
               t = TYPE_INFO.TYPE_NUMERIC
          elif type(_val) == bool:
               t = TYPE_INFO.TYPE_BOOL
          elif type(_val) == str:
               t = TYPE_INFO.TYPE_STRING
          else:
               raise Exception("Fuck")
          s = SYMBOL_INFO(symbol_name=name,
                          type=t,
                          val=_val)
          com_cntxt.add(s)
          self.var_name = name

     def GetName(self):
          return self.var_name

     def Evaluate(self, run_cntxt):
          if not run_cntxt.TABLE:
              return None

          else:
              return run_cntxt.get(self.var_name)


     def TypeCheck(self, com_cntxt):
          if not com_cntxt.GetSymbolTable():
               return TYPE_INFO.TYPE_ILLEGAL

          else:
               a = com_cntxt.get(self.var_name)
               if a:
                    self._type = a.type
                    return a.type
               return TYPE_INFO.TYPE_ILLEGAL

     def GetType(self):
          return self._type


class BinaryPlus(Exp):
     
     def __init__(self, ex1, ex2):
          self.ex1 = ex1
          self.ex2 = ex2


     def Evaluate(self, run_cntxt):
          eval_left = self.ex1.Evaluate(run_cntxt)
          eval_right = self.ex2.Evaluate(run_cntxt)
          
          if (eval_left.type == TYPE_INFO.TYPE_STRING and eval_right.type == TYPE_INFO.TYPE_STRING) or (eval_left.type == TYPE_INFO.TYPE_NUMERIC and eval_right.type == TYPE_INFO.TYPE_NUMERIC):
               retval = SYMBOL_INFO(type=eval_left.type,
                                    val=eval_left.val + eval_right.val,
                                    symbol_name="")
               return retval

          else:
               raise Exception("Type mismatch")


     def TypeCheck(self, com_cntxt):
          eval_left = self.ex1.TypeCheck(com_cntxt)
          eval_right = self.ex2.TypeCheck(com_cntxt)
          if eval_left == eval_right and eval_left != TYPE_INFO.TYPE_BOOL:
               self._type = eval_left
               return self._type
          else:
               raise Exception("Type mismatch")

     def GetType(self):
          return self._type


class BinaryMinus(Exp):
     
     def __init__(self, ex1, ex2):
          self.ex1 = ex1
          self.ex2 = ex2

     def Evaluate(self, run_cntxt):
          eval_left = self.ex1.Evaluate(run_cntxt)
          eval_right = self.ex2.Evaluate(run_cntxt)
          
          if eval_left.type == TYPE_INFO.TYPE_NUMERIC and eval_right.type == TYPE_INFO.TYPE_NUMERIC:
               retval = SYMBOL_INFO(type=eval_left.type,
                                    val=eval_left.val - eval_right.val,
                                    symbol_name="")
               return retval

          else:
               raise Exception("Type mismatch")


     def TypeCheck(self, com_cntxt):
          eval_left = self.ex1.TypeCheck(com_cntxt)
          eval_right = self.ex2.TypeCheck(com_cntxt)
          if eval_left == eval_right and eval_left == TYPE_INFO.TYPE_NUMERIC:
               self._type = eval_left
               return self._type
          else:
               raise Exception("Type mismatch")

     def GetType(self):
          return self._type


class Mul(Exp):
     
     def __init__(self, ex1, ex2):
          self.ex1 = ex1
          self.ex2 = ex2

     def Evaluate(self, run_cntxt):
          eval_left = self.ex1.Evaluate(run_cntxt)
          eval_right = self.ex2.Evaluate(run_cntxt)
          
          if eval_left.type == TYPE_INFO.TYPE_NUMERIC and eval_right.type == TYPE_INFO.TYPE_NUMERIC:
               retval = SYMBOL_INFO(type=eval_left.type,
                                    val=eval_left.val * eval_right.val,
                                    symbol_name="")
               return retval

          else:
               raise Exception("Type mismatch")


     def TypeCheck(self, com_cntxt):
          eval_left = self.ex1.TypeCheck(com_cntxt)
          eval_right = self.ex2.TypeCheck(com_cntxt)
          if eval_left == eval_right and eval_left == TYPE_INFO.TYPE_NUMERIC:
               self._type = eval_left
               return self._type
          else:
               raise Exception("Type mismatch")

     def GetType(self):
          return self._type


class Div(Exp):
     
     def __init__(self, ex1, ex2):
          self.ex1 = ex1
          self.ex2 = ex2

     def Evaluate(self, run_cntxt):
          eval_left = self.ex1.Evaluate(run_cntxt)
          eval_right = self.ex2.Evaluate(run_cntxt)
          
          if eval_left.type == TYPE_INFO.TYPE_NUMERIC and eval_right.type == TYPE_INFO.TYPE_NUMERIC:
               retval = SYMBOL_INFO(type=eval_left.type,
                                    val=eval_left.val / eval_right.val,
                                    symbol_name="")
               return retval

          else:
               raise Exception("Type mismatch")


     def TypeCheck(self, com_cntxt):
          eval_left = self.ex1.TypeCheck(com_cntxt)
          eval_right = self.ex2.TypeCheck(com_cntxt)
          if eval_left == eval_right and eval_left == TYPE_INFO.TYPE_NUMERIC:
               self._type = eval_left
               return self._type
          else:
               raise Exception("Type mismatch")

     def GetType(self):
          return self._type



class UnaryPlus(Exp):
     
     def __init__(self, ex1):
          self.ex1 = ex1

     def Evaluate(self, run_cntxt):
          eval_left = self.ex1.Evaluate(run_cntxt)
          
          if eval_left.type == TYPE_INFO.TYPE_NUMERIC:
               retval = SYMBOL_INFO(type=eval_left.type,
                                    val=eval_left.val,
                                    symbol_name="")
               return retval

          else:
               raise Exception("Type mismatch")


     def TypeCheck(self, com_cntxt):
          eval_left = self.ex1.TypeCheck(com_cntxt)
          if eval_left == TYPE_INFO.TYPE_NUMERIC:
               self._type = eval_left
               return self._type
          else:
               raise Exception("Type mismatch")

     def GetType(self):
          return self._type

class UnaryMinus(Exp):
     
     def __init__(self, ex1):
          self.ex1 = ex1

     def Evaluate(self, run_cntxt):
          eval_left = self.ex1.Evaluate(run_cntxt)
          if eval_left.type == TYPE_INFO.TYPE_NUMERIC:
               retval = SYMBOL_INFO(type=eval_left.type,
                                    val=-eval_left.val,
                                    symbol_name="")
               return retval

          else:
               raise Exception("Type mismatch")


     def TypeCheck(self, com_cntxt):
          eval_left = self.ex1.TypeCheck(com_cntxt)
          if eval_left == TYPE_INFO.TYPE_NUMERIC:
               self._type = eval_left
               return self._type
          else:
               raise Exception("Type mismatch")

     def GetType(self):
          return self._type



class RelationExp(Exp):

    def __init__(self, op, ex1, ex2):
        self.m_op = op
        self._ex1 = ex1
        self._ex2 = ex2

    def Evaluate(self, run_cntxt):

        eval_left = self._ex1.Evaluate(run_cntxt)
        eval_right = self._ex2.Evaluate(run_cntxt)

        retval = SYMBOL_INFO()
        if eval_left.type == TYPE_INFO.TYPE_NUMERIC and eval_right.type == TYPE_INFO.TYPE_NUMERIC:
            retval.type = TYPE_INFO.TYPE_BOOL
            retval.symbol_name = ""

            if self.m_op == RELATIONAL_OPERATOR.TOK_EQ:
                retval.val = eval_left.val == eval_right.val
            elif self.m_op == RELATIONAL_OPERATOR.TOK_NEQ:
                retval.val = eval_left.val != eval_right.val
            elif self.m_op == RELATIONAL_OPERATOR.TOK_GT:
                retval.val = eval_left.val > eval_right.val 
            elif self.m_op == RELATIONAL_OPERATOR.TOK_GTE:
                retval.val = eval_left.val >= eval_right.val
            elif self.m_op == RELATIONAL_OPERATOR.TOK_LT:
                retval.val = eval_left.val < eval_right.val
            elif self.m_op == RELATIONAL_OPERATOR.TOK_LTE:
                retval.val = eval_left.val <= eval_right.val
            return retval

        elif eval_left.type == TYPE_INFO.TYPE_STRING and eval_right.type == TYPE_INFO.TYPE_STRING:

            retval.type = TYPE_INFO.TYPE_BOOL
            retval.symbol_name = ""
            if self.m_op == RELATIONAL_OPERATOR.TOK_EQ:
                retval.val = eval_left.val == eval_right.val
            elif self.m_op == RELATIONAL_OPERATOR.TOK_NEQ:
                retval.val = eval_left.val != eval_right.val
            else:
                retval = False

            return retval

        elif eval_left.type == TYPE_INFO.TYPE_BOOL and eval_right.type == TYPE_INFO.TYPE_BOOL:

            retval.type = TYPE_INFO.TYPE_BOOL
            retval.symbol_name = ""
            if self.m_op == RELATIONAL_OPERATOR.TOK_EQ:
                retval.val = eval_left.val == eval_right.val
            elif self.m_op == RELATIONAL_OPERATOR.TOK_NEQ:
                retval.val = eval_left.val != eval_right.val
            else:
                retval = False

            return retval

        return None

    def TypeCheck(self, com_cntxt):
        
        eval_left = self._ex1.TypeCheck(com_cntxt)
        eval_right = self._ex2.TypeCheck(com_cntxt)

        if eval_right != eval_left:
            raise Exception("Wrong Type in Expression")

        if eval_left == TYPE_INFO.TYPE_STRING and not (self.m_op == RELATIONAL_OPERATOR.TOK_EQ or self.m_op == RELATIONAL_OPERATOR.TOK_NEQ):
            raise Exception("Only == and != supported for string type")
        if eval_left == TYPE_INFO.TYPE_BOOL and not (self.m_op == RELATIONAL_OPERATOR.TOK_EQ or self.m_op == RELATIONAL_OPERATOR.TOK_NEQ):
            raise Exception("Only == and != supported for boolean type")

        self._optype  = eval_left
        self._type = TYPE_INFO.TYPE_BOOL
        return self._type

    def GetType(self):
        return self._type


class LogicalExp(Exp):

    def __init__(self, op, ex1, ex2):
        self.m_op = op
        self._ex1 = ex1
        self._ex2 = ex2

    def TypeCheck(self, com_cntxt):

        eval_left = self._ex1.TypeCheck(com_cntxt)
        eval_right = self._ex2.TypeCheck(com_cntxt)

        if eval_left == eval_right and eval_left == TYPE_INFO.TYPE_BOOL:
            self._type = TYPE_BOOL.TYPE_BOOL
            return self._type
        else:
            raise "Wrong Type in Expression"


    def Evaluate(self, run_cntxt):

        eval_left = self._ex1.Evaluate(run_cntxt)
        eval_right = self._ex2.Evaluate(run_cntxt)

        if eval_left.type == TYPE_INFO.TYPE_BOOL and eval_right == TYPE_INFO.TYPE_BOOL:
            retval = SYMBOL_INFO()
            retval.type = TYPE_INFO.TYPE_BOOL
            retval.symbol_name = ""

            if self.m_op == TOKEN.TOK_AND:
                retval.val = eval_left.val and  eval_right.val
            elif self.m_op == TOKEN.TOK_OR:
                retval.val = eval_left.val or eval_right.val
            else:
                return None

            return retval

        return None

    def GetType(self):
        return self._type


class LogicalNot(Exp):

    def __init__(self, ex):
        self._ex = ex

    def Evaluate(self, run_cntxt):
        eval_left = self._ex.Evaluate(run_cntxt)
        if eval_left.type == TYPE_INFO.TYPE_BOOL:
            retval = SYMBOL_INFO(type=TYPE_INFO.TYPE_BOOL, symbol_name="", val=not eval_left.val)
            return retval
        else:
            return None

    def TypeCheck(self, com_cntxt):
        eval_left = self._ex.TypeCheck(com_cntxt)

        if eval_left == TYPE_INFO.TYPE_BOOL:
            self._type = TYPE_INFO.TYPE_BOOL
            return self._type
        else:
            raise Exception("Wrong Type in Expression")

    def GetType(self):
        return self._type


class CallExpr(Exp):

  def __init__(self, name=None, recurse=False, actuals=None, t=None, proc=None):
    self.name = name
    self.recurse = recurse
    self.actuals = actuals
    self._type = t
    self.proc = proc

  def Execute(self, run_cntxt):
    self.Evaluate(run_cntxt)

  def Evaluate(self, run_cntxt):

    if self.proc:
      ctx = RUNTIME_CONTEXT(run_cntxt.GetProgram())
      lst = []
      for o in self.actuals:
        lst.append(o.Evaluate(run_cntxt))
      return self.proc.Execute(ctx, lst)
    else:
      self.proc = run_cntxt.GetProgram().Find(self.name)
      ctx = RUNTIME_CONTEXT(run_cntxt.GetProgram())
      lst = []
      for o in self.actuals:
        lst.append(o.Evaluate(run_cntxt))
      return self.proc.Execute(ctx, lst)

  def TypeCheck(self, com_cntxt):
    if self.proc:
      self._type = self.proc.TypeCheck(com_cntxt)
    return self._type

  def GetType(self):
    return self._type



if __name__ == "__main__":
     
     # Abstract Syntax Tree(AST) for 5*10
     exp1 = BinaryExp(NumericConstant(5), NumericConstant(10), OPERATOR.MUL)
     print (exp1.Evaluate())

     # AST for - (10 + (30 + 50))
     exp2 = UnaryExp(
          BinaryExp(NumericConstant(10),
                    BinaryExp(NumericConstant(30),
                              NumericConstant(50),
                              OPERATOR.PLUS
                              ),
                    OPERATOR.PLUS
                    ),
          OPERATOR.PLUS
          )
     print (exp2.Evaluate())

     # AST for (400 + exp2)
     exp3  = BinaryExp(NumericConstant(400), exp2, OPERATOR.PLUS)
     print (exp3.Evaluate())

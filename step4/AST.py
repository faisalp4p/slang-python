from abc import ABCMeta, abstractmethod

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
          if not com_cntxt.TABLE:
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



###########
# class BinaryExp(Exp):

#      def __init__(self, a, b, op):
#           self._ex1 = a;
#           self._ex2 = b;
#           self._op = op

#      def Evaluate(self):

#           if self._op == OPERATOR.PLUS:
#                return self._ex1.Evaluate() + self._ex2.Evaluate()

#           elif self._op == OPERATOR.MINUS:
#                return self._ex1.Evaluate() - self._ex2.Evaluate()

#           elif self._op == OPERATOR.DIV:
#                return self._ex1.Evaluate() / self._ex2.Evaluate()

#           elif self._op == OPERATOR.MUL:
#                return self._ex1.Evaluate() * self._ex2.Evaluate()
#           else:
#                None

#      def __str__(self):
#           return u" BinaryExp(%s %s %s) " % (self._ex1, self._op, self._ex2)


# class UnaryExp(Exp):

#      def __init__(self, a, op):
#           self._ex1 = a
#           self._op = op

#      def Evaluate(self):
          
#           if self._op == OPERATOR.PLUS:
#                return self._ex1.Evaluate()
#           elif self._op == OPERATOR.MINUS:
#                return -self._ex1.Evaluate()
#           else:
#                None

#      def __str__(self):
#           return u" UnaryExp(%s %s) " % (self._op, self._ex1)


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

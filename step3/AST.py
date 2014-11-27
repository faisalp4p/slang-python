from abc import ABCMeta, abstractmethod

class OPERATOR:
     PLUS = "+"
     MINUS = "-"
     DIV = "/"
     MUL = "*"

class Exp:
     __metaclass__ = ABCMeta
     
     @abstractmethod
     def Evaluate(self): pass


class NumericConstant(Exp):
     
     def __init__(self, value):
          if type(value) not in [int, long]:
               raise TypeError("Illegal type found: %s " % type(value))
          self._value = value

     def Evaluate(self):
          return self._value

     def __str__(self):
          return u'NumericConstant(%d)' % self._value


class BinaryExp(Exp):

     def __init__(self, a, b, op):
          self._ex1 = a;
          self._ex2 = b;
          self._op = op

     def Evaluate(self):

          if self._op == OPERATOR.PLUS:
               return self._ex1.Evaluate() + self._ex2.Evaluate()

          elif self._op == OPERATOR.MINUS:
               return self._ex1.Evaluate() - self._ex2.Evaluate()

          elif self._op == OPERATOR.DIV:
               return self._ex1.Evaluate() / self._ex2.Evaluate()

          elif self._op == OPERATOR.MUL:
               return self._ex1.Evaluate() * self._ex2.Evaluate()
          else:
               None

     def __str__(self):
          return u" BinaryExp(%s %s %s) " % (self._ex1, self._op, self._ex2)


class UnaryExp(Exp):

     def __init__(self, a, op):
          self._ex1 = a
          self._op = op

     def Evaluate(self):
          
          if self._op == OPERATOR.PLUS:
               return self._ex1.Evaluate()
          elif self._op == OPERATOR.MINUS:
               return -self._ex1.Evaluate()
          else:
               None

     def __str__(self):
          return u" UnaryExp(%s %s) " % (self._op, self._ex1)


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

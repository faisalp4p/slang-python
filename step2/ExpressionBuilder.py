
from RDParser import RDParser

class ExpressionBuilder:
    
    @classmethod
    def __init__(self, expr):
       self. _expr_string = expr

    @classmethod
    def GetExpression(self):
        
        p = RDParser(self._expr_string)
        return p.CallExpr()

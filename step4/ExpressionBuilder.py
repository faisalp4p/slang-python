
from RDParser import RDParser

class ExpressionBuilder:
    
    @classmethod
    def __init__(self, expr):
       self. _expr_string = expr

    @classmethod
    def GetExpression(self):
        
        p = RDParser(self._expr_string)
        return p.CallExpr()


if __name__ == "__main__":
	
	exp_string = "2+4"
	exp = ExpressionBuilder(exp_string).GetExpression()
	print exp
	print exp.Evaluate()


from ExpressionBuilder import ExpressionBuilder

def main():
    expr_str = "-2*(3+(4/2))"
    b  = ExpressionBuilder(expr_str)
    e = b.GetExpression()
    print ("Expression in String: %s " % expr_str)
    print ("AST: %s" % e)
    print ("Result: %d" % e.Evaluate())
    


if __name__ == "__main__":
    main()

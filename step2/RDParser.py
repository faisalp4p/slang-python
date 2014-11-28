
from AST import OPERATOR
from AST import Exp
from AST import NumericConstant
from AST import BinaryExp
from AST import UnaryExp


from Lexer import TOKEN
from Lexer import Lexer


class RDParser(Lexer):

    @classmethod
    def __init__(self, string):
        self.current_token = None
        Lexer.__init__(string)

    @classmethod
    def CallExpr(self):
        self.current_token = self.GetToken()
        e = self.Expr()
        if self.current_token != TOKEN.TOK_NULL:
            raise Exception("Illegal Syntax")
        return e

    @classmethod
    def Expr(self):
        retval = self.Term()
        while (self.current_token == TOKEN.TOK_PLUS or self.current_token == TOKEN.TOK_SUB):
            l_token = self.current_token
            self.current_token = self.GetToken()
            e1 = self.Expr()
            retval = BinaryExp(retval, e1, OPERATOR.PLUS if l_token == TOKEN.TOK_PLUS else OPERATOR.MINUS)
        return retval

    @classmethod
    def Term(self):
        retval = self.Factor()
        while self.current_token == TOKEN.TOK_MUL or self.current_token == TOKEN.TOK_DIV:
            l_token = self.current_token
            self.current_token = self.GetToken() 
            e1 = self.Term()
            retval = BinaryExp(retval, e1, OPERATOR.MUL if l_token == TOKEN.TOK_MUL else OPERATOR.DIV)
        return retval

    @classmethod
    def Factor(self):
        retval = None
        if self.current_token == TOKEN.TOK_DOUBLE:
            retval = NumericConstant(self.GetNumber())
            self.current_token = self.GetToken()

        elif self.current_token == TOKEN.TOK_OPAREN:
            self.current_token = self.GetToken()
            retval = self.Expr()
            if self.current_token != TOKEN.TOK_CPAREN:
                raise Exception("Missing Closing Paranthesis")
            self.current_token = self.GetToken()

        elif self.current_token == TOKEN.TOK_PLUS or self.current_token == TOKEN.TOK_SUB:
            l_token = self.current_token
            self.current_token = self.GetToken()
            retval = self.Factor()
            retval = UnaryExp(retval, OPERATOR.PLUS if l_token == TOKEN.TOK_PLUS else OPERATOR.MINUS)
        
        else:
            raise Exception("Illegal Token")

        return retval


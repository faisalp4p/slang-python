
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
        self.CurrentToken = None
        Lexer.__init__(string)

    @classmethod
    def CallExpr(self):
        self.CurrentToken = self.GetToken()
        e = self.Expr()
        if self.CurrentToken != TOKEN.TOK_NULL:
            raise Exception("Illegal Syntax")
        return e

    @classmethod
    def Expr(self):
        RetValue = self.Term()
        while (self.CurrentToken == TOKEN.TOK_PLUS or self.CurrentToken == TOKEN.TOK_SUB):
            l_token = self.CurrentToken
            self.CurrentToken = self.GetToken()
            e1 = self.Expr()
            RetValue = BinaryExp(RetValue, e1, OPERATOR.PLUS if l_token == TOKEN.TOK_PLUS else OPERATOR.MINUS)
        return RetValue

    @classmethod
    def Term(self):
        RetValue = self.Factor()
        while self.CurrentToken == TOKEN.TOK_MUL or self.CurrentToken == TOKEN.TOK_DIV:
            l_token = self.CurrentToken
            self.CurrentToken = self.GetToken() 
            e1 = self.Term()
            RetValue = BinaryExp(RetValue, e1, OPERATOR.MUL if l_token == TOKEN.TOK_MUL else OPERATOR.DIV)
        return RetValue

    @classmethod
    def Factor(self):
        RetValue = None
        if self.CurrentToken == TOKEN.TOK_DOUBLE:
            RetValue = NumericConstant(self.GetNumber())
            self.CurrentToken = self.GetToken()

        elif self.CurrentToken == TOKEN.TOK_OPAREN:
            self.CurrentToken = self.GetToken()
            RetValue = self.Expr()
            if self.CurrentToken != TOKEN.TOK_CPAREN:
                raise Exception("Missing Closing Paranthesis")
            self.CurrentToken = self.GetToken()

        elif self.CurrentToken == TOKEN.TOK_PLUS or self.CurrentToken == TOKEN.TOK_SUB:
            l_token = self.CurrentToken
            self.CurrentToken = self.GetToken()
            RetValue = self.Factor()
            RetValue = UnaryExp(RetValue, OPERATOR.PLUS if l_token == TOKEN.TOK_PLUS else OPERATOR.MINUS)
        
        else:
            raise Exception("Illegal Token")

        return RetValue


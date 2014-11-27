

class TOKEN:
    ILLEGAL_TOKEN = -1
    TOK_PLUS = 1
    TOK_MUL = 2
    TOK_DIV = 3
    TOK_SUB = 4
    TOK_OPAREN = 5
    TOK_CPAREN = 6
    TOK_DOUBLE = 7
    TOK_NULL = 8


class Lexer:

    @classmethod
    def __init__(self, Expr):
        
        self.IExpr = Expr
        self.length = len(Expr)
        self.index = 0
        self.number = None

    @classmethod
    def GetToken(self):

        tok = TOKEN.ILLEGAL_TOKEN
        while self.index < self.length and (self.IExpr[self.index] == ' ' or self.IExpr[self.index] == '\t'):
            self.index += 1

        if self.index == self.length:
            return TOKEN.TOK_NULL

        t = self.IExpr[self.index]
        if t == '+':
            tok = TOKEN.TOK_PLUS
            self.index += 1
        elif t == '-':
            tok = TOKEN.TOK_SUB
            self.index += 1
        elif t == '*':
            tok = TOKEN.TOK_MUL
            self.index += 1
        elif t == '/':
            tok = TOKEN.TOK_DIV
            self.index += 1
        elif t == '(':
            tok = TOKEN.TOK_OPAREN
            self.index += 1
        elif t == ')':
            tok = TOKEN.TOK_CPAREN
            self.index += 1
        elif t.isdigit():
            string = ""
            while self.index < self.length and self.IExpr[self.index].isdigit():
                string += self.IExpr[self.index]
                self.index += 1
            self.number = int(string)
            tok = TOKEN.TOK_DOUBLE
        else:
            raise Exception("Error While Analyzing Token")
        return tok
 
    @classmethod
    def GetNumber(self):
        return self.number

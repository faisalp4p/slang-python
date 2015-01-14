
class TOKEN:
    ILLEGAL_TOKEN = -1
    TOK_PLUS = 1
    TOK_MUL = 2
    TOK_DIV = 3
    TOK_SUB = 4
    TOK_OPAREN = 5
    TOK_CPAREN = 6
    TOK_NUMERIC = 7
    TOK_NULL = 8
    TOK_PRINT = 9
    TOK_PRINTLN = 10
    TOK_UNQUOTED_STRING = 11
    TOK_SEMI = 12

    TOK_VAR_NUMERIC= 13
    TOK_VAR_STRING = 14
    TOK_VAR_BOOL = 15
    TOK_COMMENT = 16
    TOK_BOOL_TRUE = 17
    TOK_BOOL_FALSE = 18
    TOK_STRING = 19
    TOK_ASSIGN = 20

# new in step 6

    TOK_EQ = 21
    TOK_NEQ = 22
    TOK_GT = 23
    TOK_GTE = 24
    TOK_LT = 25
    TOK_LTE = 26
    TOK_AND = 27
    TOK_OR = 28
    TOK_NOT = 29

    TOK_IF = 30
    TOK_THEN = 31
    TOK_ELSE = 32
    TOK_ENDIF = 33
    TOK_WHILE = 34
    TOK_WEND = 35


class RELATIONAL_OPERATOR:

    TOK_EQ = "=="
    TOK_NEQ = "<>"
    TOK_GT = ">"
    TOK_GTE = ">="
    TOK_LT = "<"
    TOK_LTE = "<="



ValueTable = dict(
    PRINT=TOKEN.TOK_PRINT,
    PRINTLINE=TOKEN.TOK_PRINTLN,
    FALSE=TOKEN.TOK_BOOL_FALSE,
    TRUE=TOKEN.TOK_BOOL_TRUE,
    STRING=TOKEN.TOK_VAR_STRING,
    BOOLEAN=TOKEN.TOK_VAR_BOOL,
    NUMERIC=TOKEN.TOK_VAR_NUMERIC,

    IF=TOKEN.TOK_IF,
    WHILE=TOKEN.TOK_WHILE,
    WEND=TOKEN.TOK_WEND,
    ELSE=TOKEN.TOK_ELSE,
    ENDIF=TOKEN.TOK_ENDIF,
    THEN=TOKEN.TOK_THEN
)



class Lexer:

    @classmethod
    def __init__(self, Expr):
        
        self.IExpr = Expr
        self.length = len(Expr)
        self.index = 0
        self.number = None

        self.CurrentToken = None
        self.LastToken = None
        self.last_str = None

    @classmethod
    def GetNext(self):
        self.LastToken = self.CurrentToken
        self.CurrentToken = self.GetToken()
        return self.CurrentToken

    @classmethod
    def SaveIndex(self):
        return self.index

    @classmethod
    def GetCurrentLine(self, pindex):
        tindex = pindex
        if pindex >= self.length:
            tindex = length - 1
        while tindex > 0 and self.IExpr[tindex] != '\n':
            tindex += 1
        if self.IExpr[tindex] == '\n':
            tindex += 1
        current_line = ""
        while tindex < length and self.IExpr[tindex] != '\n':
            current_line += self.IExpr[tindex]
            tindex += 1

        return current_line + "\n"

    @classmethod
    def GetPreviousLine(self, pindex):
        tindex = pindex
        while tindex > 0 and self.IExpr[tindex] != '\n':
            tindex -= 1
        if self.IExpr[tindex] == '\n':
            tindex -= 1
        else:
            return ""
        while tindex > 0 and self.IExpr[tindex] != '\n':
            tindex -= 1

        current_line = ""

        while tindex < length and self.IExpr[tindex] != '\n':
            current_line += self.IExpr[tindex]
            tindex += 1
        return current_line + "\n"


    @classmethod
    def RestoreIndex(self, m_index):
        self.index = m_index

    @classmethod
    def ExtractString(self):
        retval = ""
        while self.index <  self.length and (self.IExpr[self.index].isalnum() or self.IExpr[self.index] == '_'):
            retval += self.IExpr[self.index]
            self.index += 1
        return retval

    @classmethod
    def SkipToEOL(self):
        while self.index < self.length and self.IExpr[self.index] != "\n":
            self.index += 1

        if self.index == self.length:
            return

        # if self.IExpr[self.index+1] == "\n":
        #     self.index += 2
        #     return

        self.index += 1
        return

    @classmethod
    def GetToken(self):

        tok = TOKEN.ILLEGAL_TOKEN
        while self.index < self.length and (self.IExpr[self.index] in [' ', '\t', '\r', '\n']):
            self.index += 1

        if self.index == self.length:
            return TOKEN.TOK_NULL

        t = self.IExpr[self.index]
        if t in ['\n', '\r']:
            self.index += 1
            return self.GetToken()
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
            if self.IExpr[self.index + 1] == '/':
                self.SkipToEOL()
                return self.GetToken()
            else:
                tok = TOKEN.TOK_DIV
                self.index += 1
        elif t == '(':
            tok = TOKEN.TOK_OPAREN
            self.index += 1
        elif t == ')':
            tok = TOKEN.TOK_CPAREN
            self.index += 1
        elif t == ';':
            tok = TOKEN.TOK_SEMI
            self.index += 1
        elif t == '=':
            if self.IExpr[self.index + 1] == '=':
                tok = TOKEN.TOK_EQ
                self.index += 2
            else:
                tok = TOKEN.TOK_ASSIGN
                self.index += 1
        elif t == '"':
            temp = ""
            self.index += 1
            while self.index < self.length and self.IExpr[self.index] != '"':
                temp += self.IExpr[self.index]
                self.index += 1
            if self.index == self.length:
                tok = TOKEN.ILLEGAL_TOKEN
                return tok
            else:
                self.index += 1
                self.last_str = temp
                tok = TOKEN.TOK_STRING
                return tok

        elif t == '!':
            tok = TOKEN.TOK_NOT
            self.index += 1
        elif t == '>':
            if self.IExpr[self.index + 1] == '=':
                tok = TOKEN.TOK_GTE
                self.index += 2
            else:
                tok = TOKEN.TOK_GT
                self.index += 1
        elif t == '<':
            if self.IExpr[self.index + 1] == '=':
                tok = TOKEN.TOK_LTE
                self.index += 2
            elif self.IExpr[self.index + 1] == '>':
                tok = TOKEN.TOK_NEQ
                self.index += 2
            else:
                tok = TOKEN.TOK_LT
                self.index += 1
        elif t == '&':
            if self.IExpr[self.index + 1] == '&':
                tok = TOKEN.TOK_AND
                self.index += 2
            else:
                tok = TOKE.ILLEGAL_TOKEN
                self.index += 1
        elif t == '|':
            if self.IExpr[self.index + 1] == '|':
                tok = TOKEN.TOK_OR
                self.index += 2
            else:
                tok = TOKE.ILLEGAL_TOKEN
                self.index += 1
        elif t.isdigit():
            string = ""
            while self.index < self.length and self.IExpr[self.index].isdigit():
                string += self.IExpr[self.index]
                self.index += 1
            if self.IExpr[self.index] == '.':
                string += "."
                self.index += 1
                while self.index < self.length and self.IExpr[self.index].isdigit():
                    string += self.IExpr[self.index]
                    self.index += 1
            self.number = float(string)
            tok = TOKEN.TOK_NUMERIC
        elif t.isalpha():
            string = ""
            while self.index < self.length and (self.IExpr[self.index].isalnum()or self.IExpr[self.index] == '_'):
                string += self.IExpr[self.index]
                self.index += 1
            string = string.upper() # now keywords and variables are incase sensitive
            if string in ValueTable:
                tok = ValueTable[string]
                return tok
            self.last_str = string
            return TOKEN.TOK_UNQUOTED_STRING
        else:
            raise Exception("Error While Analyzing Token")
        return tok
 
    @classmethod
    def GetNumber(self):
        return self.number


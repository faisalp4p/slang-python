

from AST import OPERATOR
from AST import Exp
from AST import NumericConstant
from Lexer import RELATIONAL_OPERATOR

from AST import UnaryPlus
from AST import UnaryMinus
from AST import BooleanConstant
from AST import StringLiteral
from AST import Variable
from AST import BinaryPlus
from AST import BinaryMinus
from AST import Mul
from AST import Div
from AST import RelationExp
from AST import LogicalExp
from AST import LogicalNot
# from AST import BinaryExp
# from AST import UnaryExp

from AST import TYPE_INFO
from AST import SYMBOL_INFO

from Lexer import TOKEN
from Lexer import Lexer

from ASTForStatements import PrintStatement
from ASTForStatements import PrintLineStatement
from ASTForStatements import VariableDeclStatement
from ASTForStatements import AssignmentStatement
from ASTForStatements import IfStatement
from ASTForStatements import WhileStatement


class RDParser(Lexer):

    @classmethod
    def __init__(self, string):
        #self.CurrentToken = None
        Lexer.__init__(string)

    @classmethod
    def Parse(self, com_cntxt):
        self.GetNext()
        return self.StatementList(com_cntxt)

    @classmethod
    def StatementList(self, com_cntxt):
        arr = []
        while self.CurrentToken not in [TOKEN.TOK_NULL, TOKEN.TOK_ENDIF, TOKEN.TOK_WEND, TOKEN.TOK_ELSE]:
            temp = self.Statement(com_cntxt)
            if temp:
                arr.append(temp)
        return arr

    @classmethod
    def Statement(self, com_cntxt):
        if self.CurrentToken in [TOKEN.TOK_VAR_STRING, TOKEN.TOK_VAR_NUMERIC, TOKEN.TOK_VAR_BOOL]:
            retval = self.ParseVariableDeclStatement(com_cntxt)
            self.GetNext()
        elif self.CurrentToken == TOKEN.TOK_PRINT:
            retval = self.ParsePrintStatement(com_cntxt)
            self.GetNext()
        elif self.CurrentToken == TOKEN.TOK_PRINTLN:
            retval = self.ParsePrintLNStatement(com_cntxt)
            self.GetNext()
        elif self.CurrentToken == TOKEN.TOK_UNQUOTED_STRING:
            retval = self.ParseAssignmentStatement(com_cntxt)
            self.GetNext()
        elif self.CurrentToken == TOKEN.TOK_IF:
            retval = self.ParseIfStatement(com_cntxt)
            self.GetNext()
        elif self.CurrentToken == TOKEN.TOK_WHILE:
            retval = self.ParseWhileStatement(com_cntxt)
            self.GetNext()
        else:
            raise Exception("Invalid statement")
        return retval

    @classmethod
    def ParseIfStatement(self, com_cntxt):
        tok = self.CurrentToken
        self.GetNext()
        exp = self.BExpr(com_cntxt)
        if exp.TypeCheck(com_cntxt) != TYPE_INFO.TYPE_BOOL:
            raise Exception("Expects a boolean expression")
        if self.CurrentToken != TOKEN.TOK_THEN:
            raise Exception("Then, Expected")
        self.GetNext()
        true_part = self.StatementList(com_cntxt)
        if self.CurrentToken == TOKEN.TOK_ENDIF:
            return IfStatement(exp, true_part, [])
        if self.CurrentToken != TOKEN.TOK_ELSE:
            raise Exception("ELSE expected")
        self.GetNext()
        false_part = self.StatementList(com_cntxt)
        if self.CurrentToken != TOKEN.TOK_ENDIF:
            raise Exception("ENDIF Expected")
        return IfStatement(exp, true_part, false_part)

    @classmethod
    def ParseWhileStatement(self, com_cntxt):
        self.GetNext()
        exp = self.BExpr(com_cntxt)
        if exp.TypeCheck(com_cntxt) != TYPE_INFO.TYPE_BOOL:
            raise Exception("Expected boolean expression")

        body = self.StatementList(com_cntxt)
        if self.CurrentToken != TOKEN.TOK_WEND:
            raise Exception("WEND Expected")

        return WhileStatement(exp, body)


    @classmethod
    def ParseVariableDeclStatement(self, com_cntxt):
        tok = self.CurrentToken
        self.GetNext()
        if self.CurrentToken == TOKEN.TOK_UNQUOTED_STRING:
            t = TYPE_INFO.TYPE_BOOL if tok == TOKEN.TOK_VAR_BOOL else TYPE_INFO.TYPE_NUMERIC if tok == TOKEN.TOK_VAR_NUMERIC else TYPE_INFO.TYPE_STRING
            symb = SYMBOL_INFO(symbol_name=self.last_str,
                               type=t)
            self.GetNext()
            if self.CurrentToken == TOKEN.TOK_SEMI:
                com_cntxt.add(symb)
                return VariableDeclStatement(symb)
            else:
                raise Exception(", or ; expected")  ## need to add something else
        else:
            raise Exception(", or ; expected")


    @classmethod
    def ParseAssignmentStatement(self, com_cntxt):
        variable = self.last_str
        s = com_cntxt.get(variable)
        if not s:
            raise Exception("Variable not found")

        self.GetNext()
        if self.CurrentToken != TOKEN.TOK_ASSIGN:
            raise Exception("= expected")

        self.GetNext()
        exp = self.Expr(com_cntxt)
        if exp.TypeCheck(com_cntxt) != s.type:
            raise Exception("Type mismatch in assignment")
        if self.CurrentToken != TOKEN.TOK_SEMI:
            raise Exception("; excpected")
        return AssignmentStatement(s, exp)


    @classmethod
    def ParsePrintStatement(self, com_cntxt):
        self.GetNext()
        a = self.Expr(com_cntxt)
        if self.CurrentToken != TOKEN.TOK_SEMI:
            raise Exception("; is expected")
        return PrintStatement(a)

    @classmethod
    def ParsePrintLNStatement(self, com_cntxt):
        self.GetNext()
        a = self.Expr(com_cntxt)
        if self.CurrentToken != TOKEN.TOK_SEMI:
            raise Exception("; is expected")
        return PrintLineStatement(a)

    @classmethod
    def CallExpr(self):
        self.CurrentToken = self.GetToken()
        return self.Expr()

    @classmethod
    def GetRelOp(self, tok):
        if tok == TOKEN.TOK_EQ:
            return RELATIONAL_OPERATOR.TOK_EQ
        elif tok == TOKEN.TOK_NEQ:
            return RELATIONAL_OPERATOR.TOK_NEQ
        elif tok == TOKEN.TOK_GT:
            return RELATIONAL_OPERATOR.TOK_GT
        elif tok == TOKEN.TOK_GTE:
            return RELATIONAL_OPERATOR.TOK_GTE
        elif tok == TOKEN.TOK_LT:
            return RELATIONAL_OPERATOR.TOK_LT
        else:
            return RELATIONAL_OPERATOR.TOK_LTE


    @classmethod
    def LExpr(self, com_cntxt):
        retval = self.Expr(com_cntxt)
        tok_list = [TOKEN.TOK_GT, TOKEN.TOK_GTE, TOKEN.TOK_LT,
                    TOKEN.TOK_LTE, TOKEN.TOK_EQ, TOKEN.TOK_NEQ]
        while self.CurrentToken  in tok_list:
            l_token = self.CurrentToken
            self.CurrentToken = self.GetToken()
            e2 = self.Expr(com_cntxt)
            rop = self.GetRelOp(l_token)
            retval = RelationExp(rop, retval, e2)
        return retval

    @classmethod
    def BExpr(self, com_cntxt):
        retval = self.LExpr(com_cntxt)
        tok_list = [TOKEN.TOK_AND, TOKEN.TOK_OR]
        while self.CurrentToken  in tok_list:
            l_token = self.CurrentToken
            self.CurrentToken = self.GetToken()
            e2 = Lxpr(com_cntxt)
            retval = LogicalExp(l_token, retval, e2)
        return retval

    @classmethod
    def Expr(self, com_cntxt):
        retval = self.Term(com_cntxt)
        while (self.CurrentToken == TOKEN.TOK_PLUS or self.CurrentToken == TOKEN.TOK_SUB):
            l_token = self.CurrentToken
            self.CurrentToken = self.GetToken()
            e1 = self.Expr(com_cntxt)
            if l_token == TOKEN.TOK_PLUS:
                retval = BinaryPlus(retval, e1)
            else:
                retval = BinaryMinus(retval, e1)
        return retval

    @classmethod
    def Term(self, com_cntxt):
        retval = self.Factor(com_cntxt)
        while self.CurrentToken == TOKEN.TOK_MUL or self.CurrentToken == TOKEN.TOK_DIV:
            l_token = self.CurrentToken
            self.CurrentToken = self.GetToken() 
            e1 = self.Term(com_cntxt)
            if l_token == TOKEN.TOK_MUL:
                retval = Mul(retval, e1)
            else:
                retval = Div(retval, e1)
        return retval

    @classmethod
    def Factor(self, com_cntxt):
        retval = None
        if self.CurrentToken == TOKEN.TOK_NUMERIC:
            retval = NumericConstant(self.GetNumber())
            self.CurrentToken = self.GetToken()
        elif  self.CurrentToken == TOKEN.TOK_STRING:
            retval = StringLiteral(self.last_str)
            self.CurrentToken = self.GetToken()
        elif self.CurrentToken in [TOKEN.TOK_BOOL_FALSE, TOKEN.TOK_BOOL_TRUE]:
            retval = BooleanConstant(True if self.CurrentToken == TOKEN.TOK_BOOL_TRUE else False)
            self.CurrentToken = self.GetToken()
        elif self.CurrentToken == TOKEN.TOK_OPAREN:
            self.CurrentToken = self.GetToken()
            retval = self.BExpr(com_cntxt)
            if self.CurrentToken != TOKEN.TOK_CPAREN:
                raise Exception("Missing Closing Paranthesis")
            self.CurrentToken = self.GetToken()

        elif self.CurrentToken == TOKEN.TOK_PLUS or self.CurrentToken == TOKEN.TOK_SUB:
            l_token = self.CurrentToken
            self.CurrentToken = self.GetToken()
            retval = self.Factor(com_cntxt)
            if l_token == TOKEN.TOK_PLUS:
                retval = UnaryPlus(retval)
            else:
                retval = UnaryMinus(retval)
        elif self.CurrentToken == TOKEN.TOK_NOT:
            l_token = self.CurrentToken
            self.CurrentToken = self.GetToken()
            retval = self.Factor(com_cntxt)
            retval = LogicalNot(retval)
        elif self.CurrentToken == TOKEN.TOK_UNQUOTED_STRING:
            st = self.last_str
            info = com_cntxt.get(st)
            if not info:
                raise Exception("Undefined symbol")
            self.GetNext()
            retval = Variable(info)
        
        else:
            raise Exception("Illegal Token")

        return retval



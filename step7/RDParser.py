

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
from AST import CallExpr
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
from ASTForStatements import ReturnStatement


from Builders import ProcedureBuilder
from Builders import TModuleBuilder

from contexts import COMPILATION_CONTEXT

class RDParser(Lexer):

    @classmethod
    def __init__(self, string):
        #self.CurrentToken = None
        Lexer.__init__(string)
        self.prog = TModuleBuilder()

    @classmethod
    def Parse(self, pb):
        self.GetNext()
        return self.StatementList(pb)

    @classmethod
    def StatementList(self, pb):
        arr = []
        while self.CurrentToken not in [TOKEN.TOK_NULL, TOKEN.TOK_ENDIF, TOKEN.TOK_WEND, TOKEN.TOK_ELSE, TOKEN.TOK_END]:
            temp = self.Statement(pb)
            if temp:
                arr.append(temp)
        return arr

    @classmethod
    def Statement(self, pb):
        if self.CurrentToken in [TOKEN.TOK_VAR_STRING, TOKEN.TOK_VAR_NUMERIC, TOKEN.TOK_VAR_BOOL]:
            retval = self.ParseVariableDeclStatement(pb)
            self.GetNext()
        elif self.CurrentToken == TOKEN.TOK_PRINT:
            retval = self.ParsePrintStatement(pb)
            self.GetNext()
        elif self.CurrentToken == TOKEN.TOK_PRINTLN:
            retval = self.ParsePrintLNStatement(pb)
            self.GetNext()
        elif self.CurrentToken == TOKEN.TOK_UNQUOTED_STRING:
            if self.prog.IsFunction(self.last_str):
                p = self.prog.GetProc(self.last_str)
                retval = self.ParseCallProc(pb, p)
                self.GetNext()
                #retval = ptr
            else:
                retval = self.ParseAssignmentStatement(pb)
            self.GetNext()
        elif self.CurrentToken == TOKEN.TOK_IF:
            retval = self.ParseIfStatement(pb)
            self.GetNext()
        elif self.CurrentToken == TOKEN.TOK_WHILE:
            retval = self.ParseWhileStatement(pb)
            self.GetNext()
        elif self.CurrentToken == TOKEN.TOK_RETURN:
            retval = self.ParseReturnStatement(pb)
            self.GetNext()
        else:
            raise Exception("Invalid statement")
        return retval

    @classmethod
    def ParseIfStatement(self, pb):
        tok = self.CurrentToken
        self.GetNext()
        exp = self.BExpr(pb)
        if exp.TypeCheck(pb) != TYPE_INFO.TYPE_BOOL:
            raise Exception("Expects a boolean expression")
        if self.CurrentToken != TOKEN.TOK_THEN:
            raise Exception("Then, Expected")
        self.GetNext()
        true_part = self.StatementList(pb)
        if self.CurrentToken == TOKEN.TOK_ENDIF:
            return IfStatement(exp, true_part, [])
        if self.CurrentToken != TOKEN.TOK_ELSE:
            raise Exception("ELSE expected")
        self.GetNext()
        false_part = self.StatementList(pb)
        if self.CurrentToken != TOKEN.TOK_ENDIF:
            raise Exception("ENDIF Expected")
        return IfStatement(exp, true_part, false_part)

    @classmethod
    def ParseWhileStatement(self, pb):
        self.GetNext()
        exp = self.BExpr(pb)
        if exp.TypeCheck(pb) != TYPE_INFO.TYPE_BOOL:
            raise Exception("Expected boolean expression")

        body = self.StatementList(pb)
        if self.CurrentToken != TOKEN.TOK_WEND:
            raise Exception("WEND Expected")

        return WhileStatement(exp, body)


    @classmethod
    def ParseVariableDeclStatement(self, pb):
        tok = self.CurrentToken
        self.GetNext()
        if self.CurrentToken == TOKEN.TOK_UNQUOTED_STRING:
            t = TYPE_INFO.TYPE_BOOL if tok == TOKEN.TOK_VAR_BOOL else TYPE_INFO.TYPE_NUMERIC if tok == TOKEN.TOK_VAR_NUMERIC else TYPE_INFO.TYPE_STRING
            symb = SYMBOL_INFO(symbol_name=self.last_str,
                               type=t)
            self.GetNext()
            if self.CurrentToken == TOKEN.TOK_SEMI:
                pb.add(symb)
                return VariableDeclStatement(symb)
            else:
                raise Exception(", or ; expected")  ## need to add something else
        else:
            raise Exception(", or ; expected")


    @classmethod
    def ParseAssignmentStatement(self, pb):
        variable = self.last_str
        s = pb.get(variable)
        if not s:
            raise Exception("Variable not found")

        self.GetNext()
        if self.CurrentToken != TOKEN.TOK_ASSIGN:
            raise Exception("= expected")

        self.GetNext()
        exp = self.Expr(pb)
        if exp.TypeCheck(pb) != s.type:
            raise Exception("Type mismatch in assignment")
        if self.CurrentToken != TOKEN.TOK_SEMI:
            raise Exception("; excpected")
        return AssignmentStatement(s, exp)


    @classmethod
    def ParsePrintStatement(self, pb):
        self.GetNext()
        a = self.Expr(pb)
        if self.CurrentToken != TOKEN.TOK_SEMI:
            raise Exception("; is expected")
        return PrintStatement(a)

    @classmethod
    def ParsePrintLNStatement(self, pb):
        self.GetNext()
        a = self.Expr(pb)
        if self.CurrentToken != TOKEN.TOK_SEMI:
            raise Exception("; is expected")
        return PrintLineStatement(a)

    # @classmethod
    # def CallExpr(self):
    #     self.CurrentToken = self.GetToken()
    #     return self.Expr()

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
    def LExpr(self, pb):
        retval = self.Expr(pb)
        tok_list = [TOKEN.TOK_GT, TOKEN.TOK_GTE, TOKEN.TOK_LT,
                    TOKEN.TOK_LTE, TOKEN.TOK_EQ, TOKEN.TOK_NEQ]
        while self.CurrentToken  in tok_list:
            l_token = self.CurrentToken
            self.CurrentToken = self.GetToken()
            e2 = self.Expr(pb)
            rop = self.GetRelOp(l_token)
            retval = RelationExp(rop, retval, e2)
        return retval

    @classmethod
    def BExpr(self, pb):
        retval = self.LExpr(pb)
        tok_list = [TOKEN.TOK_AND, TOKEN.TOK_OR]
        while self.CurrentToken  in tok_list:
            l_token = self.CurrentToken
            self.CurrentToken = self.GetToken()
            e2 = Lxpr(pb)
            retval = LogicalExp(l_token, retval, e2)
        return retval

    @classmethod
    def Expr(self, pb):
        retval = self.Term(pb)
        while (self.CurrentToken == TOKEN.TOK_PLUS or self.CurrentToken == TOKEN.TOK_SUB):
            l_token = self.CurrentToken
            self.CurrentToken = self.GetToken()
            e1 = self.Expr(pb)
            if l_token == TOKEN.TOK_PLUS:
                retval = BinaryPlus(retval, e1)
            else:
                retval = BinaryMinus(retval, e1)
        return retval

    @classmethod
    def Term(self, pb):
        retval = self.Factor(pb)
        while self.CurrentToken == TOKEN.TOK_MUL or self.CurrentToken == TOKEN.TOK_DIV:
            l_token = self.CurrentToken
            self.CurrentToken = self.GetToken() 
            e1 = self.Term(pb)
            if l_token == TOKEN.TOK_MUL:
                retval = Mul(retval, e1)
            else:
                retval = Div(retval, e1)
        return retval

    @classmethod
    def Factor(self, pb):
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
            retval = self.BExpr(pb)
            if self.CurrentToken != TOKEN.TOK_CPAREN:
                raise Exception("Missing Closing Paranthesis")
            self.CurrentToken = self.GetToken()

        elif self.CurrentToken == TOKEN.TOK_PLUS or self.CurrentToken == TOKEN.TOK_SUB:
            l_token = self.CurrentToken
            self.CurrentToken = self.GetToken()
            retval = self.Factor(pb)
            if l_token == TOKEN.TOK_PLUS:
                retval = UnaryPlus(retval)
            else:
                retval = UnaryMinus(retval)
        elif self.CurrentToken == TOKEN.TOK_NOT:
            l_token = self.CurrentToken
            self.CurrentToken = self.GetToken()
            retval = self.Factor(pb)
            retval = LogicalNot(retval)
        elif self.CurrentToken == TOKEN.TOK_UNQUOTED_STRING:
            st = self.last_str
            if not self.prog.IsFunction(st):
                info = pb.get(st)
                if not info:
                    raise Exception("Undefined symbol")
                self.GetNext()
                retval = Variable(info)
            else:
                if pb.GetProcedureName() == st:
                    p =  pb.GetProcedure()
                else:
                    p = self.prog.GetProc(st)
                ptr = self.ParseCallProc(pb, p)
                self.GetNext()
                retval = ptr
        else:
            raise Exception("Illegal Token")

        return retval

    @classmethod
    def ParseCallProc(self, pb, p):
        self.GetNext()
        if self.CurrentToken != TOKEN.TOK_OPAREN:
            raise Exception("opening Paranthesis expected")
        self.GetNext()
        actual_params = []
        while True:
            exp = self.BExpr(pb)
            exp.TypeCheck(pb.GetContext())
            if self.CurrentToken == TOKEN.TOK_COMMA:
                actual_params.append(exp)
                self.GetNext()
                continue

            if self.CurrentToken != TOKEN.TOK_CPAREN:
                raise Exception("Expected closing paranthesis")
            else:
                actual_params.append(exp)
                break
        #self.GetNext()
        if p:
            return CallExpr(proc=p, actuals=actual_params)
        else:
            #print pb.GetProcedure().GetType()
            return CallExpr(name=pb.GetProcedureName(), recurse=True, actuals=actual_params)

    @classmethod
    def DoParse(self):

        try:
            self.GetNext()
            return self.ParseFunctions()
        except KeyError:
            print "error"
            return None

    @classmethod
    def ParseFunctions(self):

        while self.CurrentToken == TOKEN.TOK_FUNCTION:
            b = self.ParseFunction()
            s = b.GetProcedure()

            if not s:
                print "Error while Parsing Function"
                return None
            self.prog.Add(s)
            self.GetNext()
        return self.prog.GetProgram()

    @classmethod
    def ParseFunction(self):
        p = ProcedureBuilder("", COMPILATION_CONTEXT())
        if self.CurrentToken != TOKEN.TOK_FUNCTION:
            return None
        self.GetNext()
        if self.CurrentToken not in [TOKEN.TOK_VAR_BOOL, TOKEN.TOK_VAR_NUMERIC, TOKEN.TOK_VAR_STRING]:
            return None
        if self.CurrentToken == TOKEN.TOK_VAR_BOOL:
            type_info = TYPE_INFO.TYPE_BOOL
        else:
            if self.CurrentToken == TOKEN.TOK_VAR_NUMERIC:
                type_info = TYPE_INFO.TYPE_NUMERIC
            else:
                type_info = TYPE_INFO.TYPE_STRING
        p.SetTypeInfo(type_info)
        self.GetNext()
        if self.CurrentToken != TOKEN.TOK_UNQUOTED_STRING:
            return None
        p.SetProcedureName(self.last_str)
        self.GetNext()
        if self.CurrentToken != TOKEN.TOK_OPAREN:
            return None
        self.FormalParameters(p)
        if self.CurrentToken != TOKEN.TOK_CPAREN:
            return None
        self.GetNext()
        lst = self.StatementList(p)

        if self.CurrentToken != TOKEN.TOK_END:
            raise Exception("END expected")
        for s in lst:
            p.AddStatement(s)
        return p

    @classmethod
    def FormalParameters(self, pb):
        if self.CurrentToken != TOKEN.TOK_OPAREN:
            raise Exception("Opening Paranthesis expected")
        self.GetNext()
        lst_type = []

        while self.CurrentToken in [TOKEN.TOK_VAR_BOOL, TOKEN.TOK_VAR_NUMERIC, TOKEN.TOK_VAR_STRING]:
            inf = SYMBOL_INFO()
            if self.CurrentToken == TOKEN.TOK_VAR_BOOL:
                inf.type = TYPE_INFO.TYPE_BOOL
            else:
                if self.CurrentToken == TOKEN.TOK_VAR_NUMERIC:
                    inf.type = TYPE_INFO.TYPE_NUMERIC
                else:
                    inf.type = TYPE_INFO.TYPE_STRING
            self.GetNext()
            if self.CurrentToken != TOKEN.TOK_UNQUOTED_STRING:
                raise Exception("Variable name expected")
            inf.symbol_name = self.last_str
            lst_type.append(inf.type)
            pb.AddFormals(inf)
            pb.AddLocal(inf)
            self.GetNext()
            if self.CurrentToken != TOKEN.TOK_COMMA:
                break
            x = self.GetNext()
        self.prog.AddFunctionProtoType(pb.GetProcedureName(), pb.GetTypeInfo(), lst_type)
        return

    @classmethod
    def ParseReturnStatement(self, pb):
        self.GetNext()
        exp = self.BExpr(pb)
        if self.CurrentToken != TOKEN.TOK_SEMI:
            raise Exception("; Expected")
        pb.TypeCheck(exp)
        return ReturnStatement(exp)

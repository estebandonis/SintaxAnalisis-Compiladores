import sys
import pickle
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from .CompiscriptLexer import CompiscriptLexer
from .CompiscriptParser import CompiscriptParser
from .CompiscriptVisitor import CompiscriptVisitor


class MyVisitor(CompiscriptVisitor):
    def visitIfStmt(self, ctx: CompiscriptParser.IfStmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#program.
    def visitProgram(self, ctx: CompiscriptParser.ProgramContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#declaration.
    def visitDeclaration(self, ctx: CompiscriptParser.DeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#classDecl.
    def visitClassDecl(self, ctx: CompiscriptParser.ClassDeclContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#funDecl.
    def visitFunDecl(self, ctx: CompiscriptParser.FunDeclContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#varDecl.
    def visitVarDecl(self, ctx: CompiscriptParser.VarDeclContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#statement.
    def visitStatement(self, ctx: CompiscriptParser.StatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#exprStmt.
    def visitExprStmt(self, ctx: CompiscriptParser.ExprStmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#forStmt.
    def visitForStmt(self, ctx: CompiscriptParser.ForStmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#ifStmt.

    # Visit a parse tree produced by CompiscriptParser#printStmt.
    def visitPrintStmt(self, ctx: CompiscriptParser.PrintStmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#returnStmt.
    def visitReturnStmt(self, ctx: CompiscriptParser.ReturnStmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#whileStmt.
    def visitWhileStmt(self, ctx: CompiscriptParser.WhileStmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#block.
    def visitBlock(self, ctx: CompiscriptParser.BlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#expression.
    def visitExpression(self, ctx: CompiscriptParser.ExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#assignment.
    def visitAssignment(self, ctx: CompiscriptParser.AssignmentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#logic_or.
    def visitLogic_or(self, ctx: CompiscriptParser.Logic_orContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#logic_and.
    def visitLogic_and(self, ctx: CompiscriptParser.Logic_andContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#equality.
    def visitEquality(self, ctx: CompiscriptParser.EqualityContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#comparison.
    def visitComparison(self, ctx: CompiscriptParser.ComparisonContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#term.
    def visitTerm(self, ctx: CompiscriptParser.TermContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#factor.
    def visitFactor(self, ctx: CompiscriptParser.FactorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#unary.
    def visitUnary(self, ctx: CompiscriptParser.UnaryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#call.
    def visitCall(self, ctx: CompiscriptParser.CallContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#primary.
    def visitPrimary(self, ctx: CompiscriptParser.PrimaryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#function.
    def visitFunction(self, ctx: CompiscriptParser.FunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#parameters.
    def visitParameters(self, ctx: CompiscriptParser.ParametersContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CompiscriptParser#arguments.
    def visitArguments(self, ctx: CompiscriptParser.ArgumentsContext):
        return self.visitChildren(ctx)


def compilador(input_stream):
    try:
        print("Entro al compilador")
        lexer = CompiscriptLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = CompiscriptParser(stream)
        tree = parser.program()  # Analizar la entrada utilizando la regla 'prog'

        visitor = MyVisitor()
        visitor.visit(tree)

        print("Compilación exitosa")

        return 0
    except Exception as e:
        print(f"Error de compilación: {e}")
        return 1

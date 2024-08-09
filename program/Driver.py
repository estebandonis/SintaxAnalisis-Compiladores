import sys
import os
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from graphviz import Digraph
from .CompiscriptLexer import CompiscriptLexer
from .CompiscriptParser import CompiscriptParser
from .CompiscriptVisitor import CompiscriptVisitor

# Custom visitor class inheriting from CompiscriptVisitor
class MyVisitor(CompiscriptVisitor):
    # Visit a parse tree produced by CompiscriptParser#ifStmt.
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
    
    # Constructor for MyVisitor
    def __init__(self, parser):
        self.graph = Digraph(comment='AST')  # Initialize a Digraph for the AST
        self.counter = 1  # Initialize a counter for node IDs
        self.parser = parser  # Store the parser

    # Override the visit method to create graph nodes and edges
    def visit(self, ctx):
        node_id = f"node{self.counter}"  # Create a unique node ID
        self.counter += 1  # Increment the counter

        if isinstance(ctx, ParserRuleContext):
            rule_name = self.parser.ruleNames[ctx.getRuleIndex()]  # Get the rule name
            label = f"{rule_name}: {ctx.getText()}"  # Create a label for the node
        else:
            label = f"Terminal: {ctx.getText()}"  # Create a label for terminal nodes

        self.graph.node(node_id, label)  # Add the node to the graph

        for i in range(ctx.getChildCount()):  # Iterate over children
            child = ctx.getChild(i)
            child_id = self.visit(child)  # Recursively visit children
            self.graph.edge(node_id, child_id)  # Add an edge from the current node to the child

        return node_id  # Return the node ID

    # Method to save the graph to a file
    def save_graph(self, filename):
        self.graph.render(filename, format='png')  # Render the graph to a file

# Compiler function
def compilador(input_stream):
    try:
        print("Entro al compilador")
        input_stream = InputStream(input_stream)  # Create an input stream
        lexer = CompiscriptLexer(input_stream)  # Create a lexer
        print("Paso el lexer")
        stream = CommonTokenStream(lexer)  # Create a token stream
        print("Paso el stream")
        parser = CompiscriptParser(stream)  # Create a parser
        print("Paso el parser")
        tree = parser.program()  # Parse the input
        print("program")
        tree_str = tree.toStringTree(recog=parser)  # Convert the parse tree to a string

        print(tree.toStringTree(recog=parser))

        visitor = MyVisitor(parser)  # Create a visitor
        visitor.visit(tree)  # Visit the parse tree
        visitor.save_graph("./output/graph")  # Save the graph

        print("Compilación y visualización del árbol exitosas")

        return tree_str  # Return the parse tree string
    except Exception as e:
        print(f"Error de compilación: {e}")  # Print any errors
        return 1  # Return an error code
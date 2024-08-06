import sys
import pickle
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from ConfRoomSchedulerLexer import ConfRoomSchedulerLexer
from ConfRoomSchedulerParser import ConfRoomSchedulerParser
from ConfRoomSchedulerListener import ConfRoomSchedulerListener


class ConfRoomSchedulerErrorListener(ErrorListener):
    def __init__(self):
        super(ConfRoomSchedulerErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception(f"Syntax error at line {line}, column {column}: {msg}")

class ConfRoomScheduler(ConfRoomSchedulerListener):
    print("Hello, I am a ConfRoomScheduler")



def main(argv):
    input_stream = FileStream(argv[1])
    lexer = ConfRoomSchedulerLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ConfRoomSchedulerParser(stream)
    tree = parser.prog()  # We are using 'prog' since this is the starting rule based on our ConfRoomScheduler grammar, yay!

if __name__ == '__main__':
    main(sys.argv)

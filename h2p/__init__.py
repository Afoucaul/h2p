from importlib import import_module

lexer = import_module(".lexer", __name__)
parser = import_module(".parser", __name__)

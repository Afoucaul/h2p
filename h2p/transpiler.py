from . import parser

def transpile(text):
    return parser.parse(text).transpile()

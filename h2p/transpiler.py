from . import parser

def transpile(text, start='module'):
    return parser.parse(text, start=start).transpile()

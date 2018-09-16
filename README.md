# h2p

Haskell to Python transpiler, based on Lex/Yacc Python implementation, PLY.


## Content

A main module `h2p`, with a Haskell lexer/parser, and a Haskell AST.
The `hast` submodule defines the Haskell AST for this project, and the way each node is transpiled
into a Python AST node, as per the `ast` standard module.


## Rationale

It's fun!

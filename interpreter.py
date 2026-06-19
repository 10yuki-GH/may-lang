from lexer import tokenize
from parser import Parser

class Interpreter:
    def __init__(self):
        self.env = {}

    def run(self, code):
        tokens = tokenize(code)
        ast = Parser(tokens).parse()
        for stmt in ast:
            self.exec(stmt)

    def exec(self, stmt):
        if stmt["type"] == "assign":
            self.env[stmt["name"]] = stmt["value"]
        elif stmt["type"] == "output":
            out = []
            for a in stmt["args"]:
                val = self.env.get(a, a)
                out.append(str(val).strip('"'))
            print("".join(out))
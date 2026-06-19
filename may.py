#!/usr/bin/env python3
# May（五月）v0.1 单文件解释器

import sys

# ===== Token =====
TOKENS = [
    ("KEYWORD", r"\b(fun|str|int|bool|True|False|output|input|return|noreturn|while|as|newvar)\b"),
    ("SYMBOL", r"[{}();=,\[\]]"),
    ("STRING", r'"[^"]*"'),
    ("NUMBER", r"\d+"),
    ("ID", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("SKIP", r"[ \t\n]+"),
]

def tokenize(code):
    import re
    tokens = []
    while code:
        for name, pat in TOKENS:
            m = re.match(pat, code)
            if m:
                if name != "SKIP":
                    tokens.append((name, m.group()))
                code = code[m.end():]
                break
        else:
            raise SyntaxError("非法字符: " + code[0])
    return tokens


# ===== Parser =====
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def next(self):
        t = self.peek()
        self.i += 1
        return t

    def parse(self):
        stmts = []
        while self.peek():
            stmts.append(self.parse_stmt())
        return stmts

    def parse_stmt(self):
        tok = self.peek()
        if tok[1] == "fun":
            return self.parse_fun()
        if tok[1] == "str" or tok[1] == "int":
            return self.parse_var()
        if tok[1] == "output":
            return self.parse_output()
        if tok[1] == "input":
            return self.parse_input()
        if tok[1] == "bool":
            return self.parse_if()
        if tok[1] == "while":
            return self.parse_while()
        raise SyntaxError("未知语句")

    def parse_fun(self):
        self.next()
        name = self.next()[1]
        self.next()
        params = []
        while self.peek()[1] != ")":
            params.append(self.next()[1])
        self.next()
        body = []
        while self.peek()[1] != "}":
            body.append(self.next())
        self.next()
        return {"type": "fun", "name": name, "params": params, "body": body}

    def parse_var(self):
        typ = self.next()[1]
        name = self.next()[1]
        self.next()
        value = self.next()[1]
        return {"type": "var", "dtype": typ, "name": name, "value": value}

    def parse_output(self):
        self.next()
        args = []
        while self.peek() and self.peek()[1] != ";":
            args.append(self.next()[1])
        return {"type": "output", "args": args}

    def parse_input(self):
        self.next()
        prompt = self.next()[1]
        self.next()
        kind = self.next()[1]
        name = self.next()[1]
        return {"type": "input", "prompt": prompt, "kind": kind, "name": name}

    def parse_if(self):
        self.next()
        left = self.next()[1]
        self.next()
        right = self.next()[1]
        self.next()
        body = []
        while self.peek()[1] != "}":
            body.append(self.next()[1])
        self.next()
        return {"type": "if", "left": left, "right": right, "body": body}

    def parse_while(self):
        self.next()
        count = int(self.next()[1])
        self.next()
        body = []
        while self.peek()[1] != "}":
            body.append(self.next()[1])
        self.next()
        return {"type": "while", "count": count, "body": body}


# ===== Interpreter =====
class Interpreter:
    def __init__(self):
        self.env = {}
        self.funs = {}

    def run(self, code):
        tokens = tokenize(code)
        stmts = Parser(tokens).parse()
        for s in stmts:
            self.exec(s)

    def exec(self, s):
        if s["type"] == "var":
            self.env[s["name"]] = s["value"].strip('"')
        elif s["type"] == "fun":
            self.funs[s["name"]] = s
        elif s["type"] == "output":
            out = []
            for a in s["args"]:
                out.append(str(self.env.get(a, a)).strip('"'))
            print("".join(out))
        elif s["type"] == "input":
            val = input(s["prompt"].strip('"'))
            if s["kind"] == "newvar":
                self.env[s["name"]] = val
        elif s["type"] == "if":
            if self.env.get(s["left"]) == s["right"].strip('"'):
                print("True:", s["body"])
        elif s["type"] == "while":
            for i in range(s["count"]):
                print(f"第{i+1}回合")


# ===== REPL / CLI =====
def repl():
    interp = Interpreter()
    print("May（五月）v0.1")
    while True:
        try:
            line = input(">>> ")
            if line == "exit":
                break
            interp.run(line)
        except Exception as e:
            print("错误:", e)


def main():
    if len(sys.argv) == 1:
        repl()
    else:
        with open(sys.argv[1], encoding="utf-8") as f:
            Interpreter().run(f.read())


if __name__ == "__main__":
    main()
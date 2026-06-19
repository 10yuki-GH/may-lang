#!/usr/bin/env python3
# May（五月）v0.1 完整单文件解释器

import sys, re

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
    tokens, pos = [], 0
    while pos < len(code):
        for name, pat in TOKENS:
            m = re.match(pat, code[pos:])
            if m:
                if name != "SKIP":
                    tokens.append((name, m.group()))
                pos += m.end()
                break
        else:
            raise SyntaxError("非法字符: " + code[pos])
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
        t = self.peek()[1]
        if t == "fun": return self.parse_fun()
        if t in ("str", "int"): return self.parse_var()
        if t == "output": return self.parse_output()
        if t == "input": return self.parse_input()
        if t == "bool": return self.parse_if()
        if t == "while": return self.parse_while()
        if t == "return": return self.parse_return()
        return self.parse_expr()

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
            body.append(self.parse_stmt())
        self.next()
        return {"type": "fun", "name": name, "params": params, "body": body}

    def parse_var(self):
        dtype = self.next()[1]
        name = self.next()[1]
        self.next()
        value = self.next()[1]
        return {"type": "var", "name": name, "value": value}

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
            body.append(self.parse_stmt())
        self.next()
        return {"type": "if", "left": left, "right": right, "body": body}

    def parse_while(self):
        self.next()
        count = int(self.next()[1])
        self.next()
        body = []
        while self.peek()[1] != "}":
            body.append(self.parse_stmt())
        self.next()
        return {"type": "while", "count": count, "body": body}

    def parse_return(self):
        self.next()
        value = self.next()[1]
        return {"type": "return", "value": value}

    def parse_expr(self):
        name = self.next()[1]
        if self.peek() and self.peek()[1] == "(":
            self.next()
            args = []
            while self.peek()[1] != ")":
                args.append(self.next()[1])
            self.next()
            return {"type": "call", "name": name, "args": args}
        return {"type": "id", "name": name}


# ===== Interpreter =====
class Interpreter:
    def __init__(self):
        self.env = {}
        self.funs = {}

    def run(self, code):
        for s in Parser(tokenize(code)).parse():
            r = self.exec(s)
            if r is not None:
                return r

    def exec(self, s):
        if s["type"] == "var":
            self.env[s["name"]] = s["value"].strip('"')

        elif s["type"] == "fun":
            self.funs[s["name"]] = s

        elif s["type"] == "call":
            fun = self.funs[s["name"]]
            old_env = self.env.copy()
            for k, v in zip(fun["params"], s["args"]):
                self.env[k] = v.strip('"')
            for stmt in fun["body"]:
                r = self.exec(stmt)
                if r is not None:
                    self.env = old_env
                    return r
            self.env = old_env

        elif s["type"] == "return":
            return self.env.get(s["value"], s["value"]).strip('"')

        elif s["type"] == "noreturn":
            pass

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
                for stmt in s["body"]:
                    self.exec(stmt)

        elif s["type"] == "while":
            for i in range(s["count"]):
                for stmt in s["body"]:
                    self.exec(stmt)


# ===== REPL / CLI =====
def repl():
    i = Interpreter()
    print("May（五月）v0.1")
    while True:
        try:
            line = input(">>> ")
            if line == "exit": break
            r = i.run(line)
            if r is not None:
                print(r)
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
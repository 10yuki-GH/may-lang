class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def next(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def parse(self):
        stmts = []
        while self.peek():
            stmts.append(self.parse_stmt())
        return stmts

    def parse_stmt(self):
        tok = self.peek()
        if tok[1] == "fun":
            return self.parse_fun()
        if tok[0] == "ID":
            return self.parse_assign()
        if tok[1] == "output":
            return self.parse_output()
        raise SyntaxError("未知语句")

    def parse_fun(self):
        self.next()
        name = self.next()[1]
        self.next()  # (
        params = []
        while self.peek()[1] != ")":
            t, v = self.next()
            params.append(v)
        self.next()
        body = []
        while self.peek()[1] != "}":
            body.append(self.next()[1])
        self.next()
        return {"type": "fun", "name": name, "body": body}

    def parse_assign(self):
        name = self.next()[1]
        self.next()  # =
        value = self.next()[1]
        return {"type": "assign", "name": name, "value": value}

    def parse_output(self):
        self.next()
        args = []
        while self.peek() and self.peek()[1] != ";":
            args.append(self.next()[1])
        return {"type": "output", "args": args}
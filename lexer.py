import re

TOKENS = [
    ("KEYWORD", r"\b(fun|str|int|bool|output|input|return|noreturn|True|False)\b"),
    ("SYMBOL", r"[{}();=,\[\]]"),
    ("STRING", r'"[^"]*"'),
    ("NUMBER", r"\d+"),
    ("ID", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("SKIP", r"[ \t\n]+"),
]

def tokenize(code):
    tokens = []
    while code:
        for name, pattern in TOKENS:
            m = re.match(pattern, code)
            if m:
                if name != "SKIP":
                    tokens.append((name, m.group()))
                code = code[m.end():]
                break
        else:
            raise SyntaxError("非法字符: " + code[0])
    return tokens
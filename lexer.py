import re

token_specification = [
    ('NUMBER',    r'\d+'),
    ('ID',        r'[A-Za-z_]\w*'),
    ('ASSIGN',    r'='),
    ('OP',        r'[+\-*/><]'),
    ('LPAREN',    r'\('),
    ('RPAREN',    r'\)'),
    ('LBRACE',    r'\{'),
    ('RBRACE',    r'\}'),
    ('SEMI',      r';'),
    ('SKIP',      r'[ \t]+'),
    ('NEWLINE',   r'\n'),
    ('COMMENT',   r'\#.*'),
    ('MLCOMMENT', r"'''[\s\S]*?'''|\"\"\"[\s\S]*?\"\"\""),
    ('MISMATCH',  r'.'),
]

tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
get_token = re.compile(tok_regex).match

keywords = {'if', 'else', 'while', 'print'}

def tokenize(code):
    code = code.replace('\r\n', '\n')
    line_num = 1
    pos = line_start = 0
    mo = get_token(code)
    tokens = []

    while mo:
        kind = mo.lastgroup
        value = mo.group()

        if kind == 'NUMBER':
            tokens.append(('NUMBER', value))
        elif kind == 'ID':
            if value in keywords:
                tokens.append(('KEYWORD', value))
            else:
                tokens.append(('ID', value))
        elif kind in ('ASSIGN', 'OP', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMI'):
            tokens.append((kind, value))
        elif kind == 'NEWLINE':
            line_num += 1
            line_start = mo.end()
        elif kind in ('SKIP', 'COMMENT', 'MLCOMMENT'):
            pass
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character {value!r} at line {line_num}')
        pos = mo.end()
        mo = get_token(code, pos)

    return tokens

with open('input.py', 'r') as f:
    sample_code = f.read()

for token in tokenize(sample_code):
    print(token)

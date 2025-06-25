from lexer import tokenize

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[self.pos] if tokens else None

    def eat(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            self.pos += 1
            self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token}")

    def parse(self):
        return self.statement_list()

    def statement_list(self):
        statements = []
        while self.current_token:
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'if':
            return self.if_statement()
        elif self.current_token[0] == 'ID':
            return self.assignment()
        else:
            raise SyntaxError(f"Unknown statement start: {self.current_token}")

    def assignment(self):
        var_name = self.current_token[1]
        self.eat('ID')
        self.eat('ASSIGN')
        expr = self.expression()
        self.eat('SEMI')
        return ('ASSIGN', var_name, expr)

    def if_statement(self):
        self.eat('KEYWORD')  
        condition = self.expression()
        self.eat('LBRACE')
        body = []
        while self.current_token and self.current_token[0] != 'RBRACE':
            body.append(self.statement())
        self.eat('RBRACE')
        return ('IF', condition, body)

    def expression(self):
        left = self.term()
        while self.current_token and self.current_token[0] == 'OP':
            op = self.current_token[1]
            self.eat('OP')
            right = self.term()
            left = ('BIN_OP', op, left, right)
        return left

    def term(self):
        token = self.current_token
        if token[0] == 'NUMBER':
            self.eat('NUMBER')
            return ('NUM', token[1])
        elif token[0] == 'ID':
            self.eat('ID')
            return ('VAR', token[1])
        elif token[0] == 'LPAREN':
            self.eat('LPAREN')
            expr = self.expression()
            self.eat('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {token}")

if __name__ == "__main__":
    with open('input.py', 'r') as f:
        sample_code = f.read()

    tokens = tokenize(sample_code)
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)

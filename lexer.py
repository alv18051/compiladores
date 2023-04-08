import re

class Token:
    def __init__(self, name, pattern):
        self.name = name
        self.pattern = pattern

class Lexer:
    def __init__(self, rules):
        self.rules = rules
        self.tokens = self.generate_tokens()

    def generate_tokens(self):
        tokens = []
        for name, pattern in self.rules:
            tokens.append(Token(name, pattern))
        return tokens

    def lex(self, text):
        pos = 0
        tokens = []
        while pos < len(text):
            match = None
            for token in self.tokens:
                pattern = "^" + token.pattern
                regex = re.compile(pattern)
                match = regex.match(text[pos:])
                if match:
                    value = match.group(0)
                    if token.name != 'WHITESPACE':
                        tokens.append((token.name, value))
                    pos += len(value)
                    break
            if not match:
                raise Exception("Illegal character: " + text[pos])
        return tokens

# Parse the yal file
with open("lexer2.yal") as f:
    data = f.read()

# Remove comments from the data
data = re.sub(r'\(\*.*?\*\)', '', data, flags=re.DOTALL)

# Split the data into sections
sections = re.split(r'rule tokens =\s*', data, flags=re.MULTILINE)

# Extract the token definitions
tokens = []
for line in sections[0].split('\n'):
    if line.strip().startswith('let'):
        parts = line.strip().split('=')
        if len(parts) == 2:
            tokens.append((parts[0].strip(), parts[1].strip()))

# Extract the lexer rules
rules = []
for line in sections[1].split('\n'):
    if line.strip():
        parts = line.strip().split('{')
        if len(parts) == 2:
            rules.append((parts[1].strip()[:-1], parts[0].strip()))

# Create the lexer and print the results
lexer = Lexer(rules)
print("Tokens:")
for token in lexer.tokens:
    print(token.name, token.pattern)

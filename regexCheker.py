import re

class RegexChecker:
    def __init__(self):
        self.regex  = ""
        self.isValid = False


    def check(self):
        valid = r"^[a-zA-Z0-9()ε+*\'-|%,!&^_:;@#/=?\s\\.]*$"
        operators = ['*', '|', '+', '?']
        self.regex = self.addDots(operators)
        pattern = re.compile(valid)
        matcher = pattern.match(self.regex)
        last_was_operator = False
        for c in self.regex:
            if c in operators:
                if last_was_operator and c != ')' and c != '|':
                    return 'Error. No se puede tener 2 operadores seguidos.'
                last_was_operator = True
            else:
                last_was_operator = False

        if '(' in self.regex or ')' in self.regex:
            self.isValid = False
            return self.getParenthesesErrors()

        if '()' in self.regex:
            self.isValid = False
            return "Error. El operador '()' no se está aplicando a ningún símbolo."

        self.isValid = True
        return self.getRegex()
    
    def addDots(self, operators):
        newRegex = ''

        for i in range(len(self.regex)):
            char = self.regex[i]

            if i + 1 < len(self.regex):
                nextChar = self.regex[i + 1]
                newRegex += char 
                if char != '(':
                    if nextChar != ')':
                        if nextChar not in operators:
                            if char != '|':
                                newRegex += '.'

        return newRegex + self.regex[-1]
    
    def getRegex(self):
        if '?' in self.regex:
            self.regex = self.regex.replace('?', '|ε')
            self.regex = self.regex.replace('.|ε', '|ε.')
            parts = self.regex.split('.')
            for i in range(len(parts)):
                if '|ε' in parts[i]:
                    parts[i] = f"({parts[i]})"
            self.regex = ".".join(parts)

        if '+' in self.regex and len(self.regex) > 1:
            parts = self.regex.split('.')
            new_parts = []
            for i, part in enumerate(parts):
                if '+' in part:
                    if '(' in part and ')' in part and part.index('(') < part.index('+') < part.index(')'):
                        subparts = part[part.index(
                            '(') + 1:part.index(')')].split('+')
                        new_part = f"({subparts[0]}.{subparts[0]}*)"
                        new_parts.append(new_part)
                    else:
                        subparts = part.split('+')
                        new_part = f"{subparts[0]}.{subparts[0]}*"
                        new_parts.append(new_part)
                else:
                    new_parts.append(part)
            self.regex = ".".join(new_parts)

        return self.regex
    
    def getOperatorErrors(self):
        op = self.regex[0]
        if op == '.':
            return "Error. El operador '.' no se está aplicando a ningún símbolo."
        elif op == '*':
            return "Error. El operador '*' no se está aplicando a ningún símbolo."
        elif op == '+':
            return "Error. El operador '+' no se está aplicando a ningún símbolo."
        elif op == '?':
            return "Error. El operador '?' no se está aplicando a ningún símbolo."
        elif op == '|':
            return "Error. El operador '|' no se está aplicando a ningún símbolo."
        else:
            return f"Error. El operador '{op}' no se está aplicando a ningún símbolo."
        
    def getSyntaxErrors(self):
        for c in self.regex:
            if not (c.isalnum() or c in '()+*|?.'):
                return f"Error. El caracter '{c}' no es un caracter valido."
        return "Error. La expresion regular no es valida."
    
    def getParenthesesErrors(self):
        openParenCount = 0
        for c in self.regex:
            if c == '(':
                openParenCount += 1
            elif c == ')':
                openParenCount -= 1
                if openParenCount < 0:
                    return "Error. Falta un parentesis abierto."

        if openParenCount > 0:
            return "Error. Falta un parentesis cerrado."
        else:
            self.isValid = True
            return self.getRegex()
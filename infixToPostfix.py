from collections import deque

class InfixToPostfix:
    def __init__(self, infix):
        self.infix = infix

    def precedence(self, c):
        if c == '|':
            return 1
        elif c == '.':
            return 2
        elif c == '*':
            return 3
        else:
            return -1

    def infixToPostfix(self):
        postfix = ""

        stack = deque()

        for i in range(len(self.infix)):
            c = self.infix[i]
            if c not in ['|', '.', '*', '(', ')']:
                postfix += c
            elif c == '(':
                stack.append(c)
            elif c == ')':
                while stack and stack[-1] != '(':
                    postfix += stack.pop()
                if stack and stack[-1] == '(':
                    stack.pop()
            else:
                while stack and self.precedence(c) <= self.precedence(stack[-1]):
                    postfix += stack.pop()
                stack.append(c)

        while stack:
            if stack[-1] == '(':
                return "Invalid Expression"
            postfix += stack.pop()

        return postfix
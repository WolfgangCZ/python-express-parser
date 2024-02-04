import os
import sys
import time


baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print('basename:    ', baseName)
print('dirname:     ', dirName)
sys.path.append(dirName)



exp_file_path = f"{dirName}\\schema\\ap242ed3.exp"

with open(exp_file_path, "r", encoding="utf-8") as file:
    file_content = file.read()


class Lexer:
    def __init__(self, content: str):
        self.content = content
        self.index = 0
        self.token = ''
        self.delimiters = "\n "
        self.operators = "()/*+-=!{}[|]<>?':;,.%$&#@"

    def grab_char(self):
        char = self.content[self.index]
        return char

    def lookup_char(self, num: int):
        return self.content[self.index+num]

    def next_char(self, num: int = 1):
        self.index += num

    def yield_token(self, buff_char: str = ''):
        tmp = self.token
        self.token = buff_char
        return tmp

    def get_next_token(self):
        comment = False
        char = ''
        if self.token:
            return self.yield_token()

        while self.index < len(self.content):
            char = self.grab_char()
            if char == '(' and self.lookup_char(1) == '*':
                self.next_char(2)
                comment = True
                if self.token:
                    return self.yield_token()
                continue

            elif char == '*' and self.lookup_char(1) == ')':
                self.next_char(2)
                comment = False
                continue

            if comment:
                self.next_char()
                continue

            if self.delimiters.find(char) != -1:
                self.next_char()
                if self.token:
                    return self.yield_token()
                continue

            if self.operators.find(char) != -1:
                self.next_char()
                operator = self.operators[self.operators.find(char)]
                if self.token:
                    return self.yield_token(operator)
                return operator

            else:
                self.token += char
                self.next_char()
        return None

    def __iter__(self):
        return self

    def __next__(self):
        token = self.get_next_token()
        if token is None:
            raise StopIteration
        else:
            return token

class TokenParser:
    def __init__(self, tokens: list):
        self.tokens = tokens

    def get_tokens(self):
        pass

    def 
    
    
lexer = Lexer(file_content)
print(file_content)
counter = 1
output = open("output.exp", "w", encoding="utf-8")
for token in lexer:
    output.writelines(f"{counter}: {token}\n")
    counter += 1
# diferentiate between initialization and reference
# space ' '
# delimiter ';'
# common objects? like LINE, VERTEX, etc
# r_values key
# l_values value
# other in other container

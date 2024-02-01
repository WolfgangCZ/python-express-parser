import os
import sys
import time


baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print('basename:    ', baseName)
print('dirname:     ', dirName)
sys.path.append(dirName)



exp_file_path = f"{dirName}\\schema\\basic_schema.exp"

with open(exp_file_path, "r", encoding="utf-8") as file:
    file_content = file.read()


class Lexer:
    def __init__(self, content: str):
        self.content = content
        self.index = 0
        self.token = ''

    def grab_char(self):
        char = self.content[self.index]
        return char

    def skip_chars(self, num: int = 1):
        self.index += num

    def look_char(self, num: int):
        return self.content[self.index+num]

    def next_char(self):
        self.index += 1

    def yield_token(self):
        tmp = self.token
        self.token = ""
        return tmp

# find all delimiters

    def get_next_token(self):
        comment = False
        while self.index < len(self.content):
            char = self.grab_char()
            if char == '(' and self.look_char(1) == '*':
                self.skip_chars(2)
                comment = True
            if char == '*' and self.look_char(1)  == ')':
                self.skip_chars(2)
                comment = False
            if comment:
                self.next_char()
                continue
            if char == '\n':
                self.next_char()
                if self.token:
                    return self.yield_token()
                else:
                    continue
            elif self.look_char(1) == ';':
                return self.yield_token()
            elif char == ';':
                self.next_char()
                return ';'
            elif char == ' ':
                self.next_char()
                if self.token:
                    return self.yield_token()
                else:
                    continue
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

lexer = Lexer(file_content)
print(file_content)


for token in lexer:
    print(f"token: {token}")

# diferentiate between initialization and reference
# space ' '
# delimiter ';'
# common objects? like LINE, VERTEX, etc
# r_values key
# l_values value
# other in other container

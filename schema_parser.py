import sys
import os

from logger import logger

baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print('basename:    ', baseName)
print('dirname:     ', dirName)
sys.path.append(dirName)

exp_file_path = f"{dirName}\\schema\\ap242ed3.exp"
exp_file_path = f"{dirName}\\schema\\basic_schema.exp"

with open(exp_file_path, "r", encoding="utf-8") as file:
    file_content = file.read()
    file.close()

class DataChecker():
    def __init__(self):
        pass

    def check_entity(self, content: list):
        if content[-1] != ';':
            print(f", sequence {content} doesnt have semicolon!")


class Lexer:
    def __init__(self, content: str):
        self.content = content
        self.index = 0
        self.token = ''
        self.delimiters = "\n "
        self.operators = "()/*+-=!{}[|]<>?':;,.%$&#@"
        self.token_list = []
        self.parse_content()

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

    def parse_content(self):
        for token in self:
            self.token_list.append(token)
        return self.token_list

    def __iter__(self):
        return self

    def __next__(self):
        token = self.get_next_token()
        if token is None:
            raise StopIteration
        else:
            return token


express_objects = ["TYPE", "ENTITY", "FUNCTION", "RULE", "CONSTANT"]


class TokenParser:
    def __init__(self):
        self.tokens = []
        self.map = {}
        self.leftovers = []
        self.data_checker = DataChecker()

    def parse_tokens(self, map, tokens):
        index = 0
        while index < len(tokens):
            known_token = False
            for exp_obj in express_objects:
                if tokens[index] == exp_obj:
                    lenght = self.lookup_end(index, tokens, exp_obj, f"END_{exp_obj}")
                    logger.debug(f"lenght {lenght}")
                    self.parse_tokens(map, tokens[index: index + lenght])
                    entity_segment = tokens[index: index + lenght + 1]
                    map.update(self.parse_entity(entity_segment))
                    index += lenght
                    known_token = True
            if not known_token:
                self.leftovers.append({index: tokens[index]})
            index += 1
        return map

    def lookup_end(self, index: int, tokens: list, start: str, end: str):
        logger.debug(f"tokens {tokens}")
        logger.debug(f"start {start}")
        logger.debug(f"end {end}")
        guard = 0
        lenght = 0
        while True:
            if tokens[index] == start:
                guard += 1
            elif tokens[index] == end:
                guard -= 1
            if guard == 0:
                lenght += 1
                break
            lenght += 1
            index += 1
        return lenght

    def parse_entity(self, entity_segment: list):
        self.data_checker.check_entity(entity_segment)
        entity_name = entity_segment[1]
        entity_map = {entity_name: []}
        for token in entity_segment[3:]:
            entity_map[entity_name].append(token)
        return entity_map

# classify token and evaluate ending condition
# add it to dictionary as key
# jump inside the key


map = {}
lexer = Lexer(file_content)
token_list = lexer.token_list
token_parser = TokenParser()
map = token_parser.parse_tokens(map, token_list)


print(file_content)
for token in token_parser.leftovers:
    logger.debug(f"token_name: {token}")

# find entities and put them in container
# analyze each token
# diferentiate between initialization and reference
# common objects? like LINE, VERTEX, etc
# r_values key
# l_values value
# other in other container

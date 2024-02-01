import os
import sys
import time

baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print('basename:    ', baseName)
print('dirname:     ', dirName)
sys.path.append(dirName + r'/../..')

from Converter.logger import logger

logger.msg(f"dir: {dirName}")
logger.msg(f"root: {baseName}")


step_file = f"{dirName}\\testfile.stp"

file = open(step_file, "r", encoding="utf-8")
file_content = file.read()

class Lexer:
    pass

# diferentiate between initialization and reference
# space ' '
# delimiter ';'
# common objects? like LINE, VERTEX, etc
# r_values key
# l_values value

# other in other container


line = ""
lines = []


# get commands
for i in file_content:
    if i == '\n':
        continue
    if i == ';':
        lines.append(line)
        line = ""
    else:
        line = line + i


# count = 0
# for obj in lines:
#     logger.msg(f"{obj}")
#     count += 1
#     if count == 30: break

rl_values = {}

for obj in lines:
    #guard against '=='
    #guard against multiple '='
    if obj.find('=') != -1:
        rl_values_list = obj.split('=')
        key = rl_values_list[0] 
        value = rl_values_list[1]
        if len(rl_values_list) > 2:
            rest = rl_values_list[2:]    
        rl_values.update({key.strip() : value.strip()})

for key, value in rl_values.items():
    logger.msg(f"{key} : {value}")
        



start = time.time()

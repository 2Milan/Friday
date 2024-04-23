import json
from fuzzywuzzy import fuzz
from typing import Optional
import os

with open('./plugin/main/commands.json', 'r', encoding='utf8') as f:
    VA_CMD_LIST = json.load(f)

with open('./plugin/main/answers.json', 'r', encoding='utf8') as f:
    VA_ANSWER_LIST = json.load(f)

for path in os.listdir('./plugin/'):
    for file in os.listdir(f'./plugin/{path}'):
        if file == 'commands.json':
            with open(f'./plugin/{path}/{file}', 'r', encoding='utf8') as f:
                VA_CMD_LIST.update(json.load(f))
        if file == 'answers.json':
            with open(f'./plugin/{path}/{file}', 'r', encoding='utf8') as f:
                VA_ANSWER_LIST.update(json.load(f))

print(VA_CMD_LIST)
print(VA_ANSWER_LIST)

def recognize_command(command: str) -> Optional[str]:
    """Recognizes the command from the input text and returns the corresponding key."""
    for key, value_list in VA_CMD_LIST.items():
        for value in value_list:
            if fuzz.ratio(command, value) >= 65:
                print(f"Recognized command: {fuzz.ratio(command, value)}")
                return key
    return None


if __name__ == "__main__":
    print(recognize_command("Как дела"))

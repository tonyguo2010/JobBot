import json

def loadJsonFromFile(file_name):
    with open(file_name, mode="r", encoding="utf-8") as read_file:
        content = json.load(read_file)
        return content

    return '{}'


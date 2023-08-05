import json

def write_file(content: str, path_file: str, type_file: str = '.json', mode: str = 'w') -> str:
    with open(path_file + type_file, mode) as outfile:
        outfile.write(json.dumps(content, indent=4))

def read_file(path_file: str, type_file: str = '.json') -> str:
    with open(path_file + type_file, 'r', encoding='utf8') as content:
        content = content.read()
    return json.loads(content)

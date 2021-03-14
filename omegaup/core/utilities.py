import json

def get_dict(path):
    with open(path + ".json") as target_file:
        return json.load(target_file)

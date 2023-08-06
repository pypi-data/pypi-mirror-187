import json

def dumps_json(data):
    return json.dumps(data)

def load_file(name : str):
    with open(name, "r") as f:
        return json.load(f)

def save_file(name : str, data: dict): 
    with open(name, "w") as f:
        json.dump(data, f)
    
def loads_json(data):
    return json.loads(data)


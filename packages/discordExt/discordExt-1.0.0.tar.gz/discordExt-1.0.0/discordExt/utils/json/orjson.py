import orjson

def dumps_json(data):
    return orjson.dumps(data)

def load_file(name : str):
    with open(name, "rb") as f:
        return orjson.loads(f.read())

def save_file(name : str, data: dict): 
    with open(name, "wb") as f:
        f.write(orjson.dumps(data))
    
def loads_json(data):
    return orjson.loads(data)


import os 

def read_file(path:str):
    if os.path.exists(path):
        return open(path)
    else:
        raise ValueError(f"Unable to open file: {path}")
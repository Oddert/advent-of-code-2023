def read_input(path: str):
    with open(path) as f:
        lines = f.readlines()
        return [line[:-1] for line in lines]

def read_input_raw(path: str):
    with open(path) as f:
        lines = f.read()
        return lines

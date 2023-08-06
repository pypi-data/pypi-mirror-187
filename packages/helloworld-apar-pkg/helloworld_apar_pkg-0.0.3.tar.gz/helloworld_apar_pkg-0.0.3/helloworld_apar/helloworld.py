from tqdm import tqdm

def say_hello(name=None):
    for i in tqdm(range(1)):
        if name is None:
            return "Hello, World!"
        else:
            return f"Hello, {name}!"
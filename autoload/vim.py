class Window:
    def __init__(self):
        self.cursor = (4,5)
class Current:
    def __init__(self):
        with open("test.http", "r") as f:
            self.buffer = Buffer(f.read().split("\n")[:-1])
        self.window = Window()

def count_list(content: list[str]):
    z = len(str(len(content)))
    return [f"{i+1:0{z}} {c}" for i, c in enumerate(content)]

class Buffer:
    def __init__(self, content: list[str]):
        self.content = content
    def __str__(self):
        return '\n'.join(count_list(self.content))
    def __getitem__(self, key):
        return self.content[key]
    def __len__(self):
        return len(self.content)

current = Current()
class SymbolTable:
    def __init__(self):
        self.dict = {}

    def getter(self, name: str):
        if name not in self.dict.keys():
            raise Exception(f"{name} not declared")
            
        return self.dict[name]
    
    def setter(self, name: str, value: int):
        self.dict[name] = value
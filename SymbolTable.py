class SymbolTable:
    def __init__(self):
        self.dict = {}

    def getter(self, name: str):
        return self.dict[name]
    
    def setter(self, name, value):
        self.dict[name]["value"] = value

    def create(self,variable, value, type):
        if variable in self.dict:
            raise ValueError("\033[91mVariable already exists\033[0m")
        self.dict[variable] = {"value": value, "type": type}



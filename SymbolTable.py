class SymbolTable:
    def __init__(self):
        self.table = {}

    def getter(self, variable):
        if variable not in self.table.keys():
            raise Exception(f"{variable} not declared")
            
        return self.table[variable]
    
    def setter(self, variable, value):
        self.table[variable]["value"] = value


    def create(self,variable, value, type):
        if variable in self.table:
            raise ValueError("variable already declared")
        self.table[variable] = {"value": value, "type": type}
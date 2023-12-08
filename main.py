import sys
import re
from SymbolTable import SymbolTable
from abc import ABC, abstractmethod


class Token:
    def __init__(self, type : str, value : int):
        self.type = type
        self.value = value

class PrePro:
    def __init__(self, pre_string):
        self.pre_string = pre_string
          
    def filter(self):
        code = re.sub('//.*', "", self.pre_string)
        
        lines = code.split('\n')
        code = '\n'.join([line.lstrip('\t') for line in lines])
        return code
    

class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    @abstractmethod
    def Evaluate(self, table: SymbolTable):
        pass



class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def Evaluate(self, table : SymbolTable):
    
        children_1 = self.children[0].Evaluate(table)
        children_2 = self.children[1].Evaluate(table)

        print(children_1, children_2)

        if self.value == ".":
            return (str(children_1[0]) + str(children_2[0]), "string")
        

        elif  children_1[1] == "string" and  children_2[1]== "string":
            if self.value == "==":
                return (int(children_1[0] == children_2[0]), "int")
            elif self.value == "!=":
                return (int(children_1[0] != children_2[0]), "int")
            elif self.value == ">":
                return (int(children_1[0] > children_2[0]), "int")
            elif self.value == "<":
                return (int(children_1[0] < children_2[0]), "int")
            elif self.value == ">=":
                return (int(children_1[0] >= children_2[0]), "int")
            elif self.value == "<=":
                return (int(children_1[0] <= children_2[0]), "int")
            
        elif children_1[1] == "int" and  children_2[1] == "int":
            if self.value == "==":
                return (int(children_1[0] == children_2[0]), "int")
            elif self.value == "!=":
                return (int(children_1[0] != children_2[0]), "int")
            elif self.value == ">":
                return (int(children_1[0] > children_2[0]), "int")
            elif self.value == "<":
                return (int(children_1[0] < children_2[0]), "int")
            elif self.value == ">=":
                return (int(children_1[0] >= children_2[0]), "int")
            elif self.value == "<=":
                return (int(children_1[0] <= children_2[0]), "int")
            elif self.value == "+":
                return(children_1[0] + children_2[0], "int")
            elif self.value == "-":
                return(children_1[0] - children_2[0], "int")
            elif self.value == "*":
                return(children_1[0] * children_2[0], "int")
            elif self.value == "/":
                return(children_1[0] // children_2[0], "int")
            elif self.value == "==":
                return(int(children_1[0] == children_2[0]), "int")
            elif self.value == "AND":
                return(int(children_1[0] and children_2[0]), "int")
            elif self.value == "OR":
                return(int(children_1[0] or children_2[0]), "int")
            elif self.value == "!=":
                return(int(children_1[0] != children_2[0]), "int")
            
        else: 
            raise ValueError("BinOP Value error")
        
class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def Evaluate(self, table : SymbolTable):
        if self.value == "+":
            return (self.children[0].Evaluate(table)[0], "int")
        elif self.value == "-":
            return (-self.children[0].Evaluate(table)[0], "int")
        elif self.value == "!":
            return (not(self.children[0].Evaluate(table))[0], "int")
        else: 
            raise ValueError("UnOP Value error")
        
        
class IntVal(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)
    def Evaluate(self,table : SymbolTable):
        return (self.value, "int")
    
class String(Node):
    def __init__(self, value, children=None):
        super().__init__(value, children)

    def Evaluate(self, table : SymbolTable):
        return (self.value, "string")
    
class VarDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def Evaluate(self, table : SymbolTable):
        if len(self.children) == 2:
            table.create(variable = self.children[0], value = self.children[1].Evaluate(table)[0], type = self.value)
        elif len(self.children) == 1:
            table.create(variable = self.children[0], value = None, type = self.value)

class NoOp(Node):
    def __init__(self):
        super().__init__(value=None, children=None) 
    def Evaluate(self,table : SymbolTable):
        pass

class Identifier(Node):
  def __init__(self, value):
        super().__init__(value, children=None)

  def Evaluate(self, table : SymbolTable):
    return (table.getter(self.value)["value"], table.getter(self.value)["type"])

class Assignment(Node):
    def __init__(self, children, value=None):
        super().__init__(value, children)

    def Evaluate(self, table : SymbolTable):
        value = self.children[1].Evaluate(table)
        variable = table.getter(self.children[0])

        if  value[1] != variable["type"]:
            raise ValueError("Type variable incorrect")
        
        table.setter(self.children[0], value[0])
        
class Scanln(Node):
    def __init__(self, children = None, value=None):
        super().__init__(value, children)
    def Evaluate(self, table : SymbolTable):
        return (int(input()), "int")
    

class Println(Node):

    def __init__(self, children, value = None):
        super().__init__(value, children)

    def Evaluate(self, table : SymbolTable):
        print(self.children[0].Evaluate(table)[0])

class For(Node):
    def __init__(self, children, value=None):
        super().__init__(value, children)

    def Evaluate(self, table : SymbolTable):
        self.children[0].Evaluate(table)
        while self.children[1].Evaluate(table)[0]:
            self.children[3].Evaluate(table)
            self.children[2].Evaluate(table)

class If(Node):
    def __init__(self, children, value=None):
        super().__init__(value, children)
        
    def Evaluate(self, table : SymbolTable):
        if self.children[0].Evaluate(table):
            self.children[1].Evaluate(table)
        elif len(self.children) > 2:
            self.children[2].Evaluate(table)

class Block(Node):
  def __init__(self, children, value=None):
        super().__init__(value, children)
  def Evaluate(self, table : SymbolTable):
    for child in self.children:
        if type(child) == ReturnNode:
            return child.Evaluate(table)
        child.Evaluate(table)
    return (None, "None")
# Parte de cima será o node.py

class FuncCall(Node):
    def __init__(self, name, children):
        super().__init__(value =name, children=children)

    def Evaluate(self, table : SymbolTable):
        node = FuncTable.get(name=self.value)["node"]
        type = FuncTable.get(name=self.value)["type"]
        
        func_table =SymbolTable()
        if len(self.children) != len(node.children) -2:
            raise ValueError("Invalid number of arguments")
        for i in range(len(self.children)):
            var_type = self.children[i].Evaluate(table)
            var_id = node.children[i+1].children[0]
            if var_type[1] != node.children[i+1].value:
                raise ValueError("Invalid type of arguments")
            
            func_table.create(variable=var_id, value=var_type[0], type=var_type[1])
        bloco = node.children[-1].Evaluate(func_table)
        return bloco
        


class ReturnNode(Node):
    def __init__(self, value, children=None):
        super().__init__(value, children)


    def evaluate(self, table: SymbolTable):
        return self.value.evaluate(table)
    
class FuncTable:
    table2 = {}

    def create(name, node, type):
        if name in FuncTable.table2:
            raise ValueError("Function already exists")
        FuncTable.table2[name] = {"node": node, "type": type}
    
    def get(name):
        if name not in FuncTable.table2:
            raise ValueError("Function not found")
        return FuncTable.table2[name]

class FuncDec(Node):
    def __init__(self,children):
        super().__init__(value = None, children = children)

    def Evaluate(self, table : SymbolTable):
        name_ = self.children[0].children[0]
        node_ = self
        type_ = self.children[0].value
        FuncTable.create(name=name_, node=node_, type=type_)

    
class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.next = None
        self.reserved_words = {"Println" : "Println", "if" : "if", "else" : "else", "for" : "for", "Scanln" : "Scanln", "var" : "var", "int" : "int", "string" : "string", "func": "FUNC", "return": "return"}

    def selectNext(self):
        if self.position >= len(self.source):
            self.next = Token("EOF", "EOF")
            return self.next
        
        elif self.source[self.position] == " ":
            self.position += 1
            self.selectNext()

        elif self.source[self.position] == '"':
            self.position += 1
            string = ""
            while self.source[self.position] != '"':
                if self.source[self.position] == "\n":
                    raise ValueError("String sem quotes no final")
                string += self.source[self.position]
                self.position += 1
            self.position += 1
            self.next = Token(type = "string", value =string)
            return self.next

        
        elif self.source[self.position].isnumeric():
            num = self.source[self.position]
            self.position += 1

            while self.position < len(self.source):
                if self.source[self.position].isnumeric():
                    num += self.source[self.position]
                    self.position += 1
                else: 
                    self.next = Token("int", int(num))
                    return self.next
            self.next = Token("int", int(num))
            return self.next
        
        elif self.source[self.position] == ";":
            self.position += 1
            self.next = Token("SEMICOLON", "SEMICOLON")
            return self.next
        
        elif self.source[self.position] == ".":
            self.position += 1
            self.next = Token(".", ".")
            return self.next

        elif self.source[self.position] == "+":
            self.position += 1
            self.next = Token("PLUS", "PLUS")
            return self.next

        elif self.source[self.position] == "-" :
            self.position += 1
            self.next = Token("MINUS", "MINUS")
            return self.next
        
        elif self.source[self.position] == "/":
            self.position += 1
            self.next = Token("DIV", "/")
            return self.next
        
        elif self.source[self.position] == "*":
            self.position += 1
            self.next = Token("MULT", "*")
            return self.next
        
        elif self.source[self.position] == ",":
            self.position += 1
            self.next = Token("COMMA", ",")
            return self.next
        


        elif self.source[self.position] == "(":
            self.position += 1
            self.next = Token("OPEN_PAREN", "(")
            return self.next

        elif self.source[self.position] == ")":
            self.position += 1
            self.next = Token("CLOSE_PAREN", ")")
            return self.next
        
        elif self.source[self.position] == "=":
            self.position += 1
            if self.source[self.position] == "=":
                self.position += 1
                self.next = Token("EQUAL_EQUAL", " ==")
                return self.next
            
            self.next = Token("EQUAL", "=")
            return self.next
        
        elif self.source[self.position] == "\n":
            self.position += 1
            self.next = Token("ENTER", "ENTER")
            return self.next
        
        elif self.source[self.position] == "<":
            self.position += 1
            if self.source[self.position] == "=":
                self.position += 1
                self.next = Token("LESS_EQUAL", "LESS_EQUAL")
                return self.next

            self.next = Token("LESS", "LESS")
            return self.next
        
        elif self.source[self.position] == ">":
            self.position += 1
            if self.source[self.position] == "=":
                self.position += 1
                self.next = Token("GREATER_EQUAL", "GREATER_EQUAL")
                return self.next
            self.next = Token("GREATER", "GREATER")
            return self.next
        

        elif self.source[self.position] == "!":
            self.position += 1
            if self.source[self.position] == "=":
                self.position += 1
                self.next = Token("NOT_EQUAL", "NOT_EQUAL")
                return self.next
            self.next = Token("NOT", "NOT")
            return self.next
        
        elif self.source[self.position] == "&":
            self.position += 1
            if self.source[self.position] == "&":
                self.position += 1
                self.next = Token("AND", "AND")
                return self.next
            else: 
                raise ValueError("& not found")
        
        elif self.source[self.position] == "|" :
            self.position += 1
            if self.source[self.position] == "|":
                self.position += 1
                self.next = Token("OR", "OR")
                return self.next
            else:
                raise ValueError("| not found")
            
        elif self.source[self.position] == "{":
            self.position += 1
            self.next = Token("OPEN_BRACES", "OPEN_BRACES")
            return self.next
        
        elif self.source[self.position] == "}":
            self.position += 1
            self.next = Token("CLOSE_BRACES", "CLOSE_BRACES")
            return self.next
        
        elif self.source[self.position].isalpha() or self.source[self.position] == "_":
            # Initialize the variable with the current character
            variable = self.source[self.position]
            self.position += 1

            # Continue appending characters while they are alphanumeric or underscores
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                variable += self.source[self.position]
                self.position += 1

            if variable in self.reserved_words:
                if variable in ["int", "string"]:
                    self.next = Token("type", variable)
                else:
                    self.next = Token(self.reserved_words[variable], None)

            else:
                if "int" in variable:
                    variable = variable.replace("int", "")
                    self.next = Token("IDENTIFIER", variable)  
                    self.position -= 3
                elif "string" in variable:
                    variable = variable.replace("string", "")
                    self.next = Token("IDENTIFIER", variable)  
                    self.position -= 6 #tamanho da palavra string
                else:
                    self.next = Token("IDENTIFIER", variable)

        else:
            raise ValueError("Invalid string")
        
class Parser:
    tokens: None

    def parseProgram():
        children = []
        while Parser.tokens.next.type != "EOF":
            if Parser.tokens.next.type == "ENTER":
                Parser.tokens.selectNext()
            else:
                children.append(Parser.parseDeclaration())
        
        children.append(FuncCall(name="main", children=[]))
        return children
    
    def parseDeclaration():
        args = []

        if Parser.tokens.next.type != "FUNC":
            raise ValueError("Invalid func")
        
        Parser.tokens.selectNext()
        if Parser.tokens.next.type != "IDENTIFIER":
            raise ValueError("Invalid id after func")
        
        func_id = Parser.tokens.next.value
        Parser.tokens.selectNext()
        if Parser.tokens.next.type != "OPEN_PAREN":
            raise ValueError("Invalid format func")
        
        Parser.tokens.selectNext()
        while Parser.tokens.next.type != "CLOSE_PAREN":
            if Parser.tokens.next.type == "IDENTIFIER":
                arg_id = Parser.tokens.next.value
                Parser.tokens.selectNext()

                if Parser.tokens.next.type != "type":
                    raise ValueError("Invalid type func")
                arg_type = Parser.tokens.next.value

                args.append(VarDec(value = arg_type, children=[arg_id]))
                Parser.tokens.selectNext()

            elif Parser.tokens.next.type == "COMMA":
                Parser.tokens.selectNext()
                if Parser.tokens.next.type == "CLOSE_PAREN":
                    raise ValueError("Invalid format func")
                
            else:
                raise ValueError("Invalid format func")
            

        Parser.tokens.selectNext()
        if Parser.tokens.next.type != "type":
            raise ValueError("Invalid type func")
        func_type = Parser.tokens.next.value  
        func_node = [VarDec(value = func_type, children=[func_id])]
        Parser.tokens.selectNext()
        node = FuncDec(children=func_node + args + [Parser.parseBlock()])
        Parser.tokens.selectNext()
        return node
        
            


    def parseFactor():
       if Parser.tokens.next.type == "int":
           node = IntVal(value=Parser.tokens.next.value)
           Parser.tokens.selectNext()


       elif Parser.tokens.next.type== "string":
           node = String(value=Parser.tokens.next.value)
           Parser.tokens.selectNext()


       elif Parser.tokens.next.type == "IDENTIFIER":
            identifier1 = Parser.tokens.next.value
            Parser.tokens.selectNext()

            if Parser.tokens.next.type != "OPEN_PAREN":
                node = Identifier(value=identifier1)

            elif Parser.tokens.next.type == "OPEN_PAREN":
                Parser.tokens.selectNext()
                list_args = []
                while Parser.tokens.next.type != "CLOSE_PAREN":
                    node_teste = Parser.parserBoolExpression()

                    if(Parser.tokens.next.type != "COMMA" and Parser.tokens.next.type != "CLOSE_PAREN"):
                        raise ValueError("Invalid string")

                    if Parser.tokens.next.type == "COMMA":
                        Parser.tokens.selectNext()

                    list_args.append(node_teste)

                Parser.tokens.selectNext()
                node = FuncCall(name=identifier1, children=list_args)
           
           

       elif Parser.tokens.next.type == "PLUS":
           Parser.tokens.selectNext()
           node = UnOp(value = "+", children= [Parser.parseFactor()])


       elif Parser.tokens.next.type == "MINUS":
           Parser.tokens.selectNext()
           node = UnOp(value ="-" , children=[Parser.parseFactor()])

       elif Parser.tokens.next.type == "NOT":
            Parser.tokens.selectNext()
            node = UnOp(value ="!", children=[Parser.parseFactor()])
      
       elif Parser.tokens.next.type == "OPEN_PAREN":
            Parser.tokens.selectNext()
            node = Parser.parserBoolExpression()
            if Parser.tokens.next.type != "CLOSE_PAREN":
               raise ValueError("Invalid string")
            Parser.tokens.selectNext()

       elif Parser.tokens.next.type == "Scanln":
            Parser.tokens.selectNext()
            if Parser.tokens.next.type == "OPEN_PAREN":
                Parser.tokens.selectNext()
                node = Scanln()
                if Parser.tokens.next.type == "CLOSE_PAREN":
                    Parser.tokens.selectNext()
                else:
                    raise ValueError("Invalid string")
            else:
                raise ValueError("Invalid string")

       else:
            raise ValueError("Invalid string")
      
       return node
    
    def parserTerm():

        node = Parser.parseFactor()

        while (Parser.tokens.next.type == "MULT" or Parser.tokens.next.type == "DIV") :

            if Parser.tokens.next.type == "DIV":
                Parser.tokens.selectNext()
                node = BinOp("/", [node, Parser.parseFactor()])

            elif Parser.tokens.next.type == "MULT":
                Parser.tokens.selectNext()
                node = BinOp("*", [node, Parser.parseFactor()])

            

        return node
    
    def parserBoolExpression():
        node = Parser.parseBooTerm()
        while (Parser.tokens.next.type == "OR"):
            Parser.tokens.selectNext()
            node = BinOp("OR", [node, Parser.parseBooTerm()])
        return node
    
    def parseBooTerm():
        node = Parser.relationExpression()
        while (Parser.tokens.next.type == "AND"):
            Parser.tokens.selectNext()
            node = BinOp("AND", [node, Parser.relationExpression()])
        return node
    
    def relationExpression():
        node = Parser.parseExpression()

        if Parser.tokens.next.type == "EQUAL_EQUAL":
            Parser.tokens.selectNext()
            node = BinOp("==", [node, Parser.parseExpression()])
        elif Parser.tokens.next.type == "LESS":
            Parser.tokens.selectNext()
            node = BinOp("<", [node, Parser.parseExpression()])
        elif Parser.tokens.next.type == "GREATER":
            Parser.tokens.selectNext()
            node = BinOp(">", [node, Parser.parseExpression()])

        elif Parser.tokens.next.type == "NOT_EQUAL":
            Parser.tokens.selectNext()
            node = BinOp("!=", [node, Parser.parseExpression()])

        elif Parser.tokens.next.type == "LESS_EQUAL":
            Parser.tokens.selectNext()
            node = BinOp("<=", [node, Parser.parseExpression()])

        elif Parser.tokens.next.type == "GREATER_EQUAL":
            Parser.tokens.selectNext()
            node = BinOp(">=", [node, Parser.parseExpression()])
        
        return node
                
    
    def parseBlock():
        if Parser.tokens.next.type == "OPEN_BRACES":
            Parser.tokens.selectNext()
            if Parser.tokens.next.type == "ENTER":
                Parser.tokens.selectNext()
            else:
                raise ValueError("sem enter")
            children_list = []  
            while (Parser.tokens.next.type != "EOF" and Parser.tokens.next.type != "CLOSE_BRACES"):
                children_list.append(Parser.parseStatement())
            if Parser.tokens.next.type != "EOF":
                Parser.tokens.selectNext()
                return Block(children = children_list)
            else:
                raise ValueError("sem enter")

        else: 
            raise ValueError("sem chaves abertas")

        
    def parseExpression():
        node = Parser.parserTerm()

        while Parser.tokens.next.type != "EOF" and ((Parser.tokens.next.type == "PLUS" or Parser.tokens.next.type == "MINUS" or Parser.tokens.next.type == ".")) :

            if Parser.tokens.next.type == "PLUS":
                Parser.tokens.selectNext()
                node = BinOp("+", [node, Parser.parserTerm()])


            elif Parser.tokens.next.type == "MINUS":
                Parser.tokens.selectNext()
                node = BinOp("-", [node, Parser.parserTerm()])

            elif Parser.tokens.next.type == ".":
                Parser.tokens.selectNext()
                node = BinOp(".", [node, Parser.parserTerm()])
                
            else: 
                raise ValueError
        return node
    
    def parseAssignment():
        node_id = Parser.tokens.next.value
        Parser.tokens.selectNext()

        if Parser.tokens.next.type == "EQUAL":
            Parser.tokens.selectNext()
            node = Assignment(children=[node_id, Parser.parserBoolExpression()])

        elif Parser.tokens.next.type == "OPEN_PAREN":
            Parser.tokens.selectNext()
            args = []

            while Parser.tokens.next.type != "CLOSE_PAREN":
                node_teste = Parser.parserBoolExpression()

                if(Parser.tokens.next.type != "COMMA" and Parser.tokens.next.type != "CLOSE_PAREN"):
                    raise ValueError("Invalid string")
                args.append(node_teste)

                if Parser.tokens.next.type == "COMMA":
                    Parser.tokens.selectNext()

            node = FuncCall(name=node_id, children=args)
            Parser.tokens.selectNext()


        return node

        

    
    def parseStatement():
        root = NoOp()
        if Parser.tokens.next.type == "Println":
            Parser.tokens.selectNext()
            if Parser.tokens.next.type == "OPEN_PAREN":
                Parser.tokens.selectNext()
                raiz_print = Parser.parserBoolExpression()
                if Parser.tokens.next.type == "CLOSE_PAREN":
                    Parser.tokens.selectNext()
                    root = Println(children=[raiz_print])
                else:
                    raise ValueError("Invalid string")
                
            else:
                raise ValueError("Invalid string")
            
        elif Parser.tokens.next.type == "if":

            Parser.tokens.selectNext()
            raiz_if = Parser.parserBoolExpression()
            raiz_block = Parser.parseBlock()
            
            if Parser.tokens.next.type == "else":
                Parser.tokens.selectNext()
                root = If(children= [raiz_if, raiz_block, Parser.parseBlock()])
            else:
                root = If(children=[raiz_if, raiz_block])

        elif Parser.tokens.next.type == "IDENTIFIER":
            root = Parser.parseAssignment()

        elif Parser.tokens.next.type == "var":
            Parser.tokens.selectNext()
            if Parser.tokens.next.type != "IDENTIFIER":
                raise ValueError("Invalid var")
            raiz_var = Parser.tokens.next.value
            Parser.tokens.selectNext()
            if Parser.tokens.next.type != "type":
                raise ValueError("Invalid var")
            tipo_var = Parser.tokens.next.value
            Parser.tokens.selectNext()

            if Parser.tokens.next.type == "EQUAL":
                Parser.tokens.selectNext()
                root = VarDec(tipo_var, [raiz_var, Parser.parserBoolExpression()])

            else:
                root = VarDec(tipo_var, [raiz_var])

        elif Parser.tokens.next.type == "return":
            Parser.tokens.selectNext()
            root = ReturnNode(value=Parser.parserBoolExpression())

        elif Parser.tokens.next.type == "for":
            Parser.tokens.selectNext()
            root_init = Parser.tokens.next.value
            Parser.tokens.selectNext()

            if Parser.tokens.next.type == "EQUAL":
                Parser.tokens.selectNext()
                root_init = Assignment (children=[root_init, Parser.parserBoolExpression()])
                if Parser.tokens.next.type == "SEMICOLON":
                    Parser.tokens.selectNext()
                    raiz_cond = Parser.parserBoolExpression()
                    if Parser.tokens.next.type == "SEMICOLON":
                        Parser.tokens.selectNext()
                        if Parser.tokens.next.type == "IDENTIFIER":
                            raiz_inc = Parser.tokens.next.value
                            Parser.tokens.selectNext()
                            if Parser.tokens.next.type == "EQUAL":
                                Parser.tokens.selectNext()
                                raiz_inc = Assignment(children=[raiz_inc, Parser.parserBoolExpression()])
                                raiz_block = Parser.parseBlock()
                                root = For(children=[root_init, raiz_cond, raiz_inc, raiz_block])
                            else:
                                raise ValueError("Invalid string")
                        else:
                            raise ValueError("Invalid string")
                    else:
                        raise ValueError("Invalid string")
                else:
                    raise ValueError("Invalid string")
            else:
                raise ValueError("Invalid string")
            

        if Parser.tokens.next.type in ["ENTER", "EOF"]:
            Parser.tokens.selectNext()
            return root
        raise ValueError("Statement quebrou")
            

    def run(arquivo):
        expressao_semcoment = PrePro(arquivo).filter()
        table = SymbolTable()

        Parser.tokens = Tokenizer(expressao_semcoment)  
        Parser.tokens.selectNext()

        for root in Parser.parseProgram():
            root.Evaluate(table)



expressao = open(sys.argv[1], "r")
code = expressao.read()
expressao.close()
teste = Parser.run(code)



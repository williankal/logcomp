import sys
import re
from SymbolTable import SymbolTable
from ASM import *
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
    def Evaluate(self, table: SymbolTable, assembly: Writer):
        pass



class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def Evaluate(self, table : SymbolTable,assembly: Writer):
    
        children_1 = self.children[1].Evaluate(table, assembly)
        assembly.write(f"PUSH EAX ; O BinOp recupera o valor da pilha em EAX\n")
        
        children_2 = self.children[0].Evaluate(table, assembly)
        assembly.write(f"POP EBX; O BinOp guarda o resultado na pilha\n")

        if self.value == ".":
            return (str(children_1[0]) + str(children_2[0]), "string")

        # elif  children_1[1] == "string" and  children_2[1]== "string":
        #     if self.value == "==":
        #         return (int(children_1[0] == children_2[0]), "int")
        #     elif self.value == "!=":
        #         return (int(children_1[0] != children_2[0]), "int")
        #     elif self.value == ">":
        #         return (int(children_1[0] > children_2[0]), "int")
        #     elif self.value == "<":
        #         return (int(children_1[0] < children_2[0]), "int")
        #     elif self.value == ">=":
        #         return (int(children_1[0] >= children_2[0]), "int")
        #     elif self.value == "<=":
        #         return (int(children_1[0] <= children_2[0]), "int")
            
        # elif children_1[1] == "int" and  children_2[1] == "int":
        #     if self.value == "==":
        #         return (int(children_1[0] == children_2[0]), "int")
        #     elif self.value == "!=":
        #         return (int(children_1[0] != children_2[0]), "int")
        #     elif self.value == ">":
        #         return (int(children_1[0] > children_2[0]), "int")
        #     elif self.value == "<":
        #         return (int(children_1[0] < children_2[0]), "int")
        #     elif self.value == ">=":
        #         return (int(children_1[0] >= children_2[0]), "int")
        #     elif self.value == "<=":
        #         return (int(children_1[0] <= children_2[0]), "int")
        #     elif self.value == "+":
        #         return(children_1[0] + children_2[0], "int")
        #     elif self.value == "-":
        #         return(children_1[0] - children_2[0], "int")
        #     elif self.value == "*":
        #         return(children_1[0] * children_2[0], "int")
        #     elif self.value == "/":
        #         return(children_1[0] // children_2[0], "int")
        #     elif self.value == "==":
        #         return(int(children_1[0] == children_2[0]), "int")
        #     elif self.value == "AND":
        #         return(int(children_1[0] and children_2[0]), "int")
        #     elif self.value == "OR":
        #         return(int(children_1[0] or children_2[0]), "int")
        #     elif self.value == "!=":
        #         return(int(children_1[0] != children_2[0]), "int")

        if self.value == "==":
            assembly.write(f"CMP EAX, EBX ; O BinOp executa a operacao correspondente\n")
            assembly.write(f"CALL binop_je\n")

        elif self.value == ">":
            assembly.write(f"CMP EAX, EBX ; O BinOp executa a operacao correspondente\n")
            assembly.write(f"CALL binop_jg\n")
        elif self.value == "<":
            assembly.write(f"CMP EAX, EBX ; O BinOp executa a operacao correspondente\n")
            assembly.write(f"CALL binop_jl\n")

        elif self.value == "+": 
            assembly.write(f"ADD EAX, EBX\n")

        elif self.value == "-":
            assembly.write(f"SUB EAX, EBX\n")

        elif self.value == "*":
            assembly.write(f"IMUL EBX\n")
        elif self.value == "/":
            assembly.write(f"IDIV EBX\n")
        elif self.value == "AND":
            assembly.write(f"AND EAX, EBX\n")
        elif self.value == "OR":
            assembly.write(f"OR EAX, EBX\n")
            
        else: 
            raise ValueError("BinOP Value error")
        
class UnOp(Node):
    def Evaluate(self, table : SymbolTable,assembly: Writer):
        if self.value == "+":
            assembly.write(f"MOV EAX, EAX ; O UnOp executa a operacao correspondente\n")
        elif self.value == "-":
            assembly.write(f"NEG EAX ; O UnOp executa a operacao correspondente\n")
        elif self.value == "!":
            assembly.write(f"NOT EAX ; O UnOp executa a operacao correspondente\n")
        else: 
            raise ValueError("UnOP Value error")
        
        
class IntVal(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)
    def Evaluate(self,table : SymbolTable, assembly: Writer):
        assembly.write(f"MOV EAX, {self.value} ; O IntVal carrega o valor {self.value} em EAX\n")
    
class String(Node):
    def __init__(self, value, children=None):
        super().__init__(value, children)

    def Evaluate(self, table : SymbolTable, assembly: Writer):
        return (self.value, "string")
    
class VarDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def Evaluate(self, table : SymbolTable, assembly: Writer):
        assembly.write(f"PUSH DWORD 0\n")
        pteste = (len(table.table)+1)*4
        if len(self.children) == 2:
            value = self.children[1].Evaluate(table, assembly)
            table.create(variable = self.children[0], value = value, type = self.value, position = pteste)
            assembly.write(f"MOV DWORD [EBP-{pteste}], EAX ;")
        elif len(self.children) == 1:
            table.create(variable = self.children[0], value = None, type = self.value, position = pteste)

class NoOp(Node):
    def __init__(self):
        super().__init__(value=None, children=[]) 
    def Evaluate(self,table : SymbolTable, assembly: Writer):
        return(None,None)
    
class Identifier(Node):
    def __init__(self, value):
        super().__init__(value, children=None)

    def Evaluate(self, table : SymbolTable, assembly: Writer):
        value = table.getter(self.value)["value"]
        position = table.getter(self.value)["position"]
        assembly.write(f"MOV EAX, [EBP-{position}] ; Evaluate do Iden {value}")
        return value


class Assignment(Node):
    def __init__(self, children, value=None):
        super().__init__(value, children)

    def Evaluate(self, table : SymbolTable, assembly: Writer):
        variable = table.getter(self.children[0])
        self.children[1].Evaluate(table, assembly)
        assembly.write(f"MOV [EBP-{variable['position']}], EAX ;")
        
class Scanln(Node):
    def __init__(self, children = None, value=None):
        super().__init__(value, children)
    def Evaluate(self, table : SymbolTable, assembly: Writer):
        assembly.write(f"PUSH scanint ;")
        assembly.write(f"PUSH formatin ;")
        assembly.write(f"CALL scanf ;")
        assembly.write(f"ADD ESP, 8 ;")
        assembly.write(f"MOV EAX, DWORD [scanint] ;")
    

class Println(Node):

    def __init__(self, children, value = None):
        super().__init__(value, children)

    def Evaluate(self, table : SymbolTable, assembly: Writer):
        self.children[0].Evaluate(table, assembly)
        assembly.write(f"PUSH EAX ;")
        assembly.write(f"PUSH formatout ;")
        assembly.write(f"CALL printf ;")
        assembly.write(f"ADD ESP, 8 ;")

class For(Node):
    def __init__(self, children, value=None):
        super().__init__(value, children)

    def Evaluate(self, table : SymbolTable, assembly: Writer):
        id = assembly.get_unique_id
        assembly.write(f"LOOP_I{id}: ;")
        self.children[1].Evaluate(table, assembly)
        assembly.write(f"CMP EAX, False ;")
        assembly.write(f"JE EXIT_{id} ;")
        self.children[2].Evaluate(table, assembly)
        self.children[3].Evaluate(table, assembly)
        assembly.write(f"JMP LOOP_I{id} ;")
        assembly.write(f"EXIT_{id}: ;")


class If(Node):
    def __init__(self, children, value=None):
        super().__init__(value, children)
        
    def Evaluate(self, table : SymbolTable, assembly: Writer):
        id = assembly.get_unique_id
        self.children[0].Evaluate(table, assembly) 
        assembly.write(f"CMP EAX, False ;")
        assembly.write(f"JE EXIST_{id} ;")
        self.children[1].Evaluate(table, assembly)
        assembly.write(f"JMP EXIT_{id} ;")
        assembly.write(f"ELSE_{id}: ;")
        if len(self.children) > 2:
            self.children[2].Evaluate(table, assembly)
        assembly.write(f"EXIT_{id}: ;")





class Block(Node):
  def __init__(self, children, value=None):
        super().__init__(value, children)
  def Evaluate(self, table : SymbolTable, assembly: Writer):
    for child in self.children:
      child.Evaluate(table, assembly)
        

# Parte de cima será o node.py
    
class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.next = None
        self.reserved_words = {"Println" : "Println", "if" : "if", "else" : "else", "for" : "for", "Scanln" : "Scanln", "var" : "var", "int" : "int", "string" : "string"}

    def selectNext(self):


        if self.position >= len(self.source):
            self.next = Token("EOF", " ")
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
            children.append(Parser.parseStatement())
        return children

    def parseFactor():
       if Parser.tokens.next.type == "int":
           node = IntVal(value=Parser.tokens.next.value)
           Parser.tokens.selectNext()


       elif Parser.tokens.next.type== "string":
           node = String(value=Parser.tokens.next.value)
           Parser.tokens.selectNext()
           if Parser.tokens.next.type == "string":
            raise ValueError("Invalid string")

           

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

       elif Parser.tokens.next.type == "IDENTIFIER":
            node = Identifier(value=Parser.tokens.next.value)
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
            while Parser.tokens.next.type != "CLOSE_BRACES" and Parser.tokens.next.type != "EOF":
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
                raiz_else = Parser.parseBlock()
                root = If(children= [raiz_if, raiz_block, raiz_else])
            else:
                root = If(children=[raiz_if, raiz_block])

        elif Parser.tokens.next.type == "IDENTIFIER":
            raiz_id = Parser.tokens.next.value
            Parser.tokens.selectNext()
            if Parser.tokens.next.type == "EQUAL":
                Parser.tokens.selectNext()
                root = Assignment(children=[raiz_id, Parser.parserBoolExpression()])
            else:
                raise ValueError("Invalid string")

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
            

    def run(arquivo, assembly):
        expressao_semcoment = PrePro(arquivo).filter()
        table = SymbolTable()

        Parser.tokens = Tokenizer(expressao_semcoment)  
        Parser.tokens.selectNext()

        for root in Parser.parseProgram():
            root.Evaluate(table, assembly)



arquivo = sys.argv[1]
arquivo_nome = arquivo.replace(".go", "")   
assembly = Writer(f"{arquivo_nome}.asm")
with open(arquivo, "r") as expressao:
    code = expressao.read()
teste = Parser.run(code, assembly)
expressao.close()


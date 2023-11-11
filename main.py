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
    def Evaluate(self, table : SymbolTable):

        children_1 = self.children[0].Evaluate(table)
        children_2 = self.children[1].Evaluate(table)
        
        if children_1[1] == "STRING" and  children_2[1]== "STRING":
            if self.value == "==":
                return (children_1[0] == children_2[0], "INT")
            elif self.value == "!=":
                return (children_1[0] != children_2[0], "INT")
            elif self.value == ">":
                return (children_1[0] > children_2[0], "INT")
            elif self.value == "<":
                return (children_1[0] < children_2[0], "INT")
            elif self.value == ">=":
                return (children_1[0] >= children_2[0], "INT")
            elif self.value == "<=":
                return (children_1[0] <= children_2[0], "INT")
            
        elif children_1[1] == "INT" and  children_2[1]== "INT":
            if self.value == "+":
                return(children_1[0] + children_2[0], "INT")
            elif self.value == "-":
                return(children_1[0] - children_2[0], "INT")
            elif self.value == "*":
                return(children_1[0] * children_2[0], "INT")
            elif self.value == "//":
                return(children_1[0] // children_2[0], "INT")
            elif self.value == "==":
                return(children_1[0] == children_2[0], "INT")
            elif self.value == "AND":
                return(children_1[0] and children_2[0], "INT")
            elif self.value == "OR":
                return(children_1[0] or children_2[0], "INT")
            elif self.value == "!=":
                return(children_1[0] != children_2[0], "INT")
            
        elif self.value == ".":
            return (str(children_1[0]) + str(children_2[0]), "STRING")
            
        else: 
            print(self.value)
            raise ValueError("BinOP Value error")
        
class UnOp(Node):
    def Evaluate(self, table : SymbolTable):
    
        children = self.children[0].Evaluate(table)

        if children[1] == "STRING":
            raise ValueError("string não pode ser usada em UnOp")

        if self.value == "+":
            return (children[0], "INT")
        elif self.value == "-":
            return (-children[0], "INT")
        elif self.value == "!":
            return (not children[0], "INT")
        else: 
            raise ValueError("UnOP Value error")
        
        
class IntVal(Node):
    def Evaluate(self,table : SymbolTable):
        return (self.value, "INT")

class NoOp(Node):
    def __init__(self):
        super().__init__(value=None, children=[]) 
    def Evaluate(self,table : SymbolTable):
        pass

class Identifier(Node):
  def Evaluate(self, table : SymbolTable):
    return table.getter(self.value)["value"]

class Assignment(Node):
    def __init__(self, children, value=None):
        super().__init__(value, children)

    def Evaluate(self, table : SymbolTable):
        table.setter(self.children[0], self.children[1].Evaluate(table))

class Scanln(Node):
    def __init__(self, children = None, value=None):
        super().__init__(value, children)
    def Evaluate(self, table : SymbolTable):
        return (int (input()), "INT")
    
class Println(Node):
    def Evaluate(self, table : SymbolTable):
        print(self.children[0].Evaluate(table)[0])

class For(Node):
    def Evaluate(self, table : SymbolTable):
        self.children[0].Evaluate(table)
        while self.children[1].Evaluate(table):
            self.children[3].Evaluate(table)
            self.children[2].Evaluate(table)

class If(Node):
    def Evaluate(self, table : SymbolTable):
        if self.children[0].Evaluate(table)[0]:
            self.children[1].Evaluate(table)
        elif len(self.children) > 3:
            self.children[2].Evaluate(table)
            

class Block(Node):
  def Evaluate(self, table : SymbolTable):
    for child in self.children:
      child.Evaluate(table)



class VarVal(Node):

    def Evaluate(self, table : SymbolTable):
        if len(self.children) == 2:
            table.create(variable = self.children[0], value = self.children[1].Evaluate(table), type = self.value)
        elif len(self.children) == 1:
            table.create(variable = self.children[0], value = None, type = self.value)

class StringVal(Node):
    def Evaluate(self, table : SymbolTable):
        return (self.value, "STRING")
    
        

# Parte de cima será o node.py
    
class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.next = None
        self.reserved_words = {"Println" : "Println", "if" : "if", "else" : "else", "for" : "for", "Scanln" : "Scanln", "var" : "var", "int" : "INT", "string" : "STRING"}

    def selectNext(self):

        #EOF case
        if self.position >= len(self.source):
            self.next = Token("EOF", " ")
            return self.next
        
        # Skip spaces
        elif self.source[self.position] == " ":
            self.position += 1
            self.selectNext()


        #INT case
        elif self.source[self.position].isnumeric():
            num = self.source[self.position]
            self.position += 1

            while self.position < len(self.source):
                if self.source[self.position].isnumeric():
                    num += self.source[self.position]
                    self.position += 1
                else: 
                    self.next = Token("INT", int(num))
                    return self.next
            self.next = Token("INT", int(num))
            return self.next
        
       #Semicolon case 
        elif self.source[self.position] == ";":
            self.position += 1
            self.next = Token("SEMICOLON", " ")
            return self.next

        #Plus case
        elif self.source[self.position] == "+":
            self.position += 1
            self.next = Token("PLUS", " ")
            return self.next

        #Minus case
        elif self.source[self.position] == "-" :
            self.position += 1
            self.next = Token("MINUS", " ")
            return self.next
        
        #Div case
        elif self.source[self.position] == "/":
            self.position += 1
            self.next = Token("DIV", "/")
            return self.next
        
        #Mult case
        elif self.source[self.position] == "*":
            self.position += 1
            self.next = Token("MULT", "*")
            return self.next
        

        #Open Parenthesis case
        elif self.source[self.position] == "(":
            self.position += 1
            self.next = Token("OPEN_PAREN", " ")
            return self.next
        

        #Close Parenthesis case
        elif self.source[self.position] == ")":
            self.position += 1
            self.next = Token("CLOSE_PAREN", " ")
            return self.next
        
        #Equal case
        elif self.source[self.position] == "=":
            self.position += 1
            if self.source[self.position] == "=":
                self.position += 1
                self.next = Token("EQUAL_EQUAL", " ")
                return self.next
            
            self.next = Token("EQUAL", " ")
            return self.next
        
        #Enter case
        elif self.source[self.position] == "\n":
            self.position += 1
            self.next = Token("ENTER", " ")
            return self.next
        
        #Less case
        elif self.source[self.position] == "<":
            self.position += 1
            self.next = Token("LESS", " ")
            return self.next
        
       #Greater case 
        elif self.source[self.position] == ">":
            self.position += 1
            self.next = Token("GREATER", " ")
            return self.next
        
        #GreaterEqual case
        elif self.source[self.position] == ">=":
            self.position += 1
            self.next = Token("GREATER_EQUAL", " ")
            return self.next
        
        #LessEqual case
        elif self.source[self.position] == "<=":
            self.position += 1
            self.next = Token("LESS_EQUAL", " ")
            return self.next
        
        #NotEqual case
        elif self.source[self.position] == "!=":
            self.position += 1
            self.next = Token("NOT_EQUAL", " ")
            return self.next
        
        #Not case
        elif self.source[self.position] == "!":
            self.position += 1
            self.next = Token("NOT", " ")
            return self.next
        
        #And case
        elif self.source[self.position] == "&":
            self.position += 1
            if self.source[self.position] == "&":
                self.position += 1
                self.next = Token("AND", " ")
                return self.next
            else: 
                raise ValueError("& not found")
            
        #Or case
        elif self.source[self.position] == "|" :
            self.position += 1
            if self.source[self.position] == "|":
                self.position += 1
                self.next = Token("OR", " ")
                return self.next
            else:
                raise ValueError("| not found")
            
        #Open Brackets case   
        elif self.source[self.position] == "{":
            self.position += 1
            self.next = Token("OPEN_BRACES", " ")
            return self.next
        
        #Close Brackets case
        elif self.source[self.position] == "}":
            self.position += 1
            self.next = Token("CLOSE_BRACES", " ")
            return self.next
        
        elif self.source[self.position] == ".":
            self.position += 1
            self.next = Token(".", ".")
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
                self.next = Token("IDENTIFIER", variable)
            return self.next
        
        elif self.source[self.position] == '"':
            self.position += 1
            string = ""
            while self.position < len(self.source) and self.source[self.position] != '"':
                string += self.source[self.position]
                self.position += 1
            self.position += 1
            self.next = Token("STRING", string)
            return self.next
        
        
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
       if Parser.tokens.next.type == "INT":
           node = IntVal(Parser.tokens.next.value, [])
           Parser.tokens.selectNext()

       elif Parser.tokens.next.type == "STRING":
            node = StringVal(Parser.tokens.next.value, [])
            Parser.tokens.selectNext()

       elif Parser.tokens.next.type == "PLUS":
           Parser.tokens.selectNext()
           node = UnOp("+", [Parser.parseFactor()])


       elif Parser.tokens.next.type == "MINUS":
           Parser.tokens.selectNext()
           node = UnOp("-" , [Parser.parseFactor()])

       elif Parser.tokens.next.type == "NOT":
            Parser.tokens.selectNext()
            node = UnOp("!", [Parser.parseFactor()])
      
       elif Parser.tokens.next.type == "OPEN_PAREN":
            Parser.tokens.selectNext()
            node = Parser.parserBoolExpression()
            if Parser.tokens.next.type != "CLOSE_PAREN":
               raise ValueError("Invalid string")

            else:
                Parser.tokens.selectNext()

       elif Parser.tokens.next.type == "IDENTIFIER":
            node = Identifier(Parser.tokens.next.value, [])
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
                root = Parser.parseStatement()
            else:
                raise ValueError("sem enter")
            if Parser.tokens.next.type == "CLOSE_BRACES":
                Parser.tokens.selectNext()
                return root
            else:
                raise ValueError("sem chaves fechadas")
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
                    root = Println("Println", [raiz_print])
                else:
                    raise ValueError("Invalid string")
                
            else:
                raise ValueError("Invalid string")
            
        elif Parser.tokens.next.type == "var":
            Parser.tokens.selectNext()
            if Parser.tokens.next.type != "IDENTIFIER":
                raise ValueError("Invalid var")
            raiz_id = Parser.tokens.next.value
            Parser.tokens.selectNext()
            if Parser.tokens.next.type == "type":
                raiz_type = Parser.tokens.next.value
                Parser.tokens.selectNext()
            if Parser.tokens.next.type == "EQUAL":
                Parser.tokens.selectNext()
                root = VarVal(raiz_type, [raiz_id, Parser.parserBoolExpression()])
            else:
                root = VarVal(raiz_type, [raiz_id])

            
        elif Parser.tokens.next.type == "if":

            Parser.tokens.selectNext()
            raiz_if = Parser.parserBoolExpression()
            raiz_block = Parser.parseBlock()
            if Parser.tokens.next.type == "else":
                Parser.tokens.selectNext()
                raiz_else = Parser.parseBlock()
                root = If("if", [raiz_if, raiz_block, raiz_else])
            else:
                root = If("if", [raiz_if, raiz_block])

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
                                root = For("for", [root_init, raiz_cond, raiz_inc, raiz_block])
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
            
        elif Parser.tokens.next.type == "IDENTIFIER":
            raiz_id = Parser.tokens.next.value
            Parser.tokens.selectNext()
            if Parser.tokens.next.type == "EQUAL":
                Parser.tokens.selectNext()
                root = Assignment(children=[raiz_id, Parser.parserBoolExpression()])

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



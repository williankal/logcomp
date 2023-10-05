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
        self.pre_string = re.sub('//.*', "", self.pre_string)
        return self.pre_string.strip()
    

class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    @abstractmethod
    def evaluate(self, table: SymbolTable):
        pass

class BinOp(Node):
    def Evaluate(self, table : SymbolTable):
        if self.value == "+":
            return self.children[0].Evaluate(table) + self.children[1].Evaluate(table)
        elif self.value == "-":
            return self.children[0].Evaluate(table) - self.children[1].Evaluate(table)
        elif self.value == "*":
            return self.children[0].Evaluate(table) * self.children[1].Evaluate(table)
        elif self.value == "/":
            return self.children[0].Evaluate(table) // self.children[1].Evaluate(table)
        
        else: 
            raise ValueError("BinOP Value error")
        
class UnOp(Node):
    def Evaluate(self, table : SymbolTable):
        if self.value == "+":
            return self.children[0].Evaluate(table)
        elif self.value == "-":
            return -self.children[0].Evaluate(table)
        else: 
            raise ValueError("UnOP Value error")
        
class IntVal(Node):
    def Evaluate(self,table : SymbolTable):
        return self.value

class NoOp(Node):
    def Evaluate(self,table : SymbolTable):
        pass

class Identifier(Node):
  def Evaluate(self, table : SymbolTable):
    return table.getter(self.value)

class Assignment(Node):
  def Evaluate(self, table : SymbolTable):
    table.setter(self.children[0].value, self.children[1].Evaluate(table))

class Println(Node):
    def Evaluate(self, table : SymbolTable):
        print(self.children[0].Evaluate(table))
class Block(Node):
  def Evaluate(self, table : SymbolTable):
    for child in self.children:
      child.Evaluate(table)
        

# Parte de cima será o node.py
    
class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.next = None
        self.reserved_words = ["Println"]

    def selectNext(self):
        if self.position >= len(self.source):
            self.next = Token("EOF", " ")
            return self.next
        

        elif self.source[self.position].isnumeric():
            num = self.source[self.position]
            self.position += 1

            while self.position < len(self.source):
                if self.source[self.position].isnumeric():
                    num += self.source[self.position]
                    self.position += 1
                else: 
                    self.next = Token("NUM", int(num))
                    return self.next
            self.next = Token("NUM", int(num))
            return self.next

        elif self.source[self.position] == "+":
            self.position += 1
            self.next = Token("PLUS", " ")
            return self.next

        elif self.source[self.position] == "-" :
            self.position += 1
            self.next = Token("MINUS", " ")
            return self.next
        
        elif self.source[self.position] == "/":
            self.position += 1
            self.next = Token("DIV", "/")
            return self.next
        
        elif self.source[self.position] == "*":
            self.position += 1
            self.next = Token("MULT", "*")
            return self.next
        

        elif self.source[self.position] == " ":
            self.position += 1
            self.selectNext()

        elif self.source[self.position] == "(":
            self.position += 1
            self.next = Token("OPEN_PAREN", " ")
            return self.next

        elif self.source[self.position] == ")":
            self.position += 1
            self.next = Token("CLOSE_PAREN", " ")
            return self.next
        
        elif self.source[self.position] == "=":
            self.position += 1
            self.next = Token("EQUAL", " ")
            return self.next
        
        elif self.source[self.position] == "\n":
            self.position += 1
            self.next = Token("ENTER", " ")
            return self.next
        
        elif self.source[self.position].isalpha() or self.source[self.position] == "_":
            # Initialize the variable with the current character
            variable = self.source[self.position]
            self.position += 1

            # Continue appending characters while they are alphanumeric or underscores
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                variable += self.source[self.position]
                self.position += 1

            # Check if the variable is a reserved word
            type = "PRINTLN" if variable in self.reserved_words else "IDENTIFIER"
            self.next = Token(type, variable)
            return self.next

        else:
            raise Exception("Invalid char")

class Parser:
    tokens: None

    def parseFactor():
       if Parser.tokens.next.type == "NUM":
           node = IntVal(Parser.tokens.next.value, [])
           Parser.tokens.selectNext()

       elif Parser.tokens.next.type == "PLUS":
           Parser.tokens.selectNext()
           node = UnOp("+", [Parser.parseFactor()])


       elif Parser.tokens.next.type == "MINUS":
           Parser.tokens.selectNext()
           node = UnOp("-" , [Parser.parseFactor()])
      
       elif Parser.tokens.next.type == "OPEN_PAREN":
            Parser.tokens.selectNext()
            node = Parser.parseExpression()
            if Parser.tokens.next.type != "CLOSE_PAREN":
               raise ValueError("Invalid string")

            else:
                Parser.tokens.selectNext()

       elif Parser.tokens.next.type == "IDENTIFIER":
            node = Identifier(Parser.tokens.next.value, [])
            Parser.tokens.selectNext()

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
                
    
    def parseBlock():
        children = []
        while Parser.tokens.next.type != "EOF":
            children.append(Parser.parseStatement())
                
        return children

        
    def parseExpression():
        node = Parser.parserTerm()

        while Parser.tokens.next.type != "EOF" and ((Parser.tokens.next.type == "PLUS" or Parser.tokens.next.type == "MINUS")) :

            if Parser.tokens.next.type == "PLUS":
                Parser.tokens.selectNext()
                node = BinOp("+", [node, Parser.parserTerm()])


            elif Parser.tokens.next.type == "MINUS":
                Parser.tokens.selectNext()
                node = BinOp("-", [node, Parser.parserTerm()])
                
            else: 
                raise ValueError
        return node
    
    def parseStatement():
        if Parser.tokens.next.type == "IDENTIFIER":
            # Parse assignment statement
            identifier = Identifier(Parser.tokens.next.value, [])
            Parser.tokens.selectNext()

            if Parser.tokens.next.type == "EQUAL":
                Parser.tokens.selectNext()
                expression = Parser.parseExpression()
                node = Assignment("=", [identifier, expression])
            else:
                raise Exception("Parse statement error: Expected '=' after identifier")

        elif Parser.tokens.next.type == "PRINTLN":
            # Parse printf statement
            Parser.tokens.selectNext()

            if Parser.tokens.next.type == "OPEN_PAREN":
                Parser.tokens.selectNext()
                expression = Parser.parseExpression()
                node = Println("PRINTLN", [expression])

                if Parser.tokens.next.type == "CLOSE_PAREN":
                    Parser.tokens.selectNext()

                else:
                    raise Exception("Parse statement error: Missing closing parenthesis")
            else:
                raise Exception("Parse statement error: Missing open parenthesis after printf")
        
        elif Parser.tokens.next.type == "ENTER" or Parser.tokens.next.type == "EOF":
            Parser.tokens.selectNext()
            node = NoOp("NOOP", [])
            return node

        else:
            raise Exception("Parse statement error: Unexpected token")
        

        return node

    def run(arquivo):
        expressao_semcoment = PrePro(arquivo).filter()
        table = SymbolTable()
        Parser.tokens = Tokenizer(expressao_semcoment)  
        Parser.tokens.selectNext()
        node1 = Parser.parseBlock()
        
        if Parser.tokens.next.type != "EOF":
            raise Exception("Invalid string")
        else:
            # print(node1.Evaluate(table))
            for node in node1:
                node.Evaluate(table)


expressao = open(sys.argv[1], "r")
code = expressao.read()
expressao.close()
teste = Parser.run(code)



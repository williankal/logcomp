import sys
import re

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
        
        def Evaluate():
            pass

# BinOP, UnOp, intVal, NoOp precisa reescrever a fun'c~aso evaluate

class BinOp(Node):
    def Evaluate(self):
        if self.value == "+":
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        elif self.value == "-":
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        elif self.value == "*":
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        elif self.value == "/":
            return self.children[0].Evaluate() // self.children[1].Evaluate()
        
        else: 
            raise ValueError("BinOP Value error")
        
class UnOp(Node):
    def Evaluate(self):
        if self.value == "+":
            return self.children[0].Evaluate()
        elif self.value == "-":
            return -self.children[0].Evaluate()
        else: 
            raise ValueError("UnOP Value error")
        
class IntVal(Node):
    def Evaluate(self):
        return self.value

class NoOp(Node):
    def Evaluate(self):
        pass
    


class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):
        if self.position >= len(self.source):
            self.next = Token("EOF", 0)
            return

        if self.source[self.position].isnumeric():
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
            self.next = Token("PLUS", "+")
            return

        elif self.source[self.position] == "-" :
            self.next = Token("MINUS", "-")
            self.position += 1
            return
        
        elif self.source[self.position] == "/":
            self.next = Token("DIV", "/")
            self.position += 1
            return
        
        elif self.source[self.position] == "*":
            self.next = Token("MULT", "*")
            self.position += 1
            return
        

        elif self.source[self.position] == " ":
            self.position += 1
            self.selectNext()

        elif self.source[self.position] == "(":
            self.next = Token("OPEN_PAREN", 0)
            self.position += 1
            return

        elif self.source[self.position] == ")":
            self.next = Token("CLOSE_PAREN", 0)
            self.position += 1
            return
    
        
        else:
            raise Exception("Invalid char")



class Parser:
    tokens: None

    @staticmethod    
    def parseFactor():
       
       node = 0
       if Parser.tokens.next.type == "NUM":
           node = IntVal(Parser.tokens.next.value, [])
           Parser.tokens.selectNext()


       elif Parser.tokens.next.type == "PLUS":
           Parser.tokens.selectNext()
           node = UnOp(" + ", [Parser.parseFactor()])


       elif Parser.tokens.next.type == "MINUS":
           Parser.tokens.selectNext()
           node = UnOp(" - " , [Parser.parseFactor()])
      
       elif Parser.tokens.next.type == "OPEN_PAREN":
            node = Parser.parseExpression()
            if Parser.tokens.next.type == "CLOSE_PAREN":
                Parser.tokens.selectNext()

            else:
               raise ValueError("Invalid string")
           
       else:
           raise ValueError("Invalid string")
      
       return node
    

    @staticmethod    
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
                
    

        

    @staticmethod    
    def parseExpression():
        
        Parser.tokens.selectNext()
        node = Parser.parserTerm()

        if all(op not in Parser.tokens.source for op in ["-", "+", "*", "/", ]) and len(Parser.tokens.source) > 1:
            raise Exception("Invalid string")

        while Parser.tokens.next.type != "EOF" and ((Parser.tokens.next.type == "PLUS" or Parser.tokens.next.type == "MINUS")) :

            if Parser.tokens.next.type == "PLUS":
                Parser.tokens.selectNext()
                node = BinOp("+", [node, Parser.parserTerm()])


            elif Parser.tokens.next.type == "MINUS":
                Parser.tokens.selectNext()
                rnode = BinOp("-", [node, Parser.parserTerm()])
                
            else: 
                raise ValueError
        return node
        


    def run(arquivo):
        f = open(arquivo, "r")
        code = f.read()
        f.close()
        code_filter = PrePro(code).filter()
        Parser.tokens = Tokenizer(code_filter)  
        node = Parser.parseExpression()
        
        if Parser.tokens.next.type != "EOF":
            raise Exception("Invalid string")
        print(node.Evaluate())


Parser.run(sys.argv[1])
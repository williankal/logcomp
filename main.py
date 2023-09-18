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
            node = Parser.parseExpression()
            if Parser.tokens.next.type != "CLOSE_PAREN":
               raise ValueError("Invalid string")

            else:
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
                
    

        
    def parseExpression():
        
        Parser.tokens.selectNext()
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
        


    def run(arquivo):
        expressao = open(arquivo, "r")
        code = expressao.read()
        expressao.close()
        expressao_semcoment = PrePro(code).filter()
        Parser.tokens = Tokenizer(expressao_semcoment)  
        node = Parser.parseExpression()
        
        if Parser.tokens.next.type != "EOF":
            raise Exception("Invalid string")
        print(node.Evaluate())


Parser.run(sys.argv[1])


##testando
# 3+6/3   *  2 -+-  +  2*4/2 + 0/1 -((6+ ((4)))/(2)) // Teste // Teste 2

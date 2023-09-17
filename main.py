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
        self.pre_string = re.sub("/\*.*?\*/", "", self.pre_string)
        
class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
        def Evaluate():
            pass
        


class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):
        while self.position < len(self.source):
            current_char = self.source[self.position]

            if current_char.isnumeric():
                num = current_char
                self.position += 1

                while self.position < len(self.source) and self.source[self.position].isnumeric():
                    num += self.source[self.position]
                    self.position += 1

                self.next = Token("NUM", int(num))
                return

            elif current_char == "+" and self.next.type != "PLUS":
                self.next = Token("PLUS", 0)
                self.position += 1
                return

            elif current_char == "-" and self.next.type != "MINUS":
                self.next = Token("MINUS", 0)
                self.position += 1
                return
            
            elif current_char == "/" and self.next.type !="DIV":
                self.next = Token("DIV", 0)
                self.position += 1
                return
            
            elif current_char == "*" and self.next.type !="MULT":
                self.next = Token("MULT", 0)
                self.position += 1
                return
            

            elif current_char == " ":
                self.position += 1
                continue

            elif current_char == "(":
                self.next = Token("OPEN_PAREN", 0)
                self.position += 1
                return

            elif current_char == ")":
                self.next = Token("CLOSE_PAREN", 0)
                self.position += 1
                return
            
            else:
                raise Exception("Invalid char")

        self.next = Token("EOF", 0)            


class Parser:
    tokens: None

    @staticmethod    
    def parseFactor():
       
       resultado = 0
       if Parser.tokens.next.type == "NUM":
           resultado = Parser.tokens.next.value
           Parser.tokens.selectNext()


       elif Parser.tokens.next.type == "PLUS":
           Parser.tokens.selectNext()
           resultado += Parser.parseFactor()


       elif Parser.tokens.next.type == "MINUS":
           Parser.tokens.selectNext()
           resultado -= Parser.parseFactor()
      
       elif Parser.tokens.next.type == "OPEN_PAREN":
            resultado = Parser.parseExpression()
            if Parser.tokens.next.type == "CLOSE_PAREN":
                Parser.tokens.selectNext()

            else:
               raise ValueError("Invalid string")
           
       else:
           raise ValueError("Invalid string")
      
       return resultado
    

    @staticmethod    
    def parserTerm():

        resultado = Parser.parseFactor()

        while (Parser.tokens.next.type == "MULT" or Parser.tokens.next.type == "DIV") :
            if Parser.tokens.next.type == "DIV":
                
                Parser.tokens.selectNext()
                resultado //= Parser.parseFactor()
                
            elif Parser.tokens.next.type == "MULT":
                Parser.tokens.selectNext()
                
                resultado *= Parser.parseFactor()

                
        return resultado
                
    

        

    @staticmethod    
    def parseExpression():
        Parser.tokens.selectNext()
        resultado = Parser.parserTerm()

        if all(op not in Parser.tokens.source for op in ["-", "+", "*", "/", ]) and len(Parser.tokens.source) > 1:
            raise Exception("Invalid string")

        while Parser.tokens.next.type != "EOF" and ((Parser.tokens.next.type == "PLUS" or Parser.tokens.next.type == "MINUS")) :

            if Parser.tokens.next.type == "PLUS":
                Parser.tokens.selectNext()
                resultado += Parser.parserTerm()


            elif Parser.tokens.next.type == "MINUS":
                Parser.tokens.selectNext()
                resultado -= Parser.parserTerm()
                
            else: 
                raise ValueError
        return resultado
        


    def run(arquivo):
        f = open(arquivo, "r")
        code = f.read()
        f.close()
        code_filter = PrePro(code).filter()
        Parser.tokens = Tokenizer(code_filter)  
        resultado = Parser.parseExpression()
        
        if Parser.tokens.next.type != "EOF":
            raise Exception("Invalid string")
        print(node.evaluate())


Parser.run(sys.argv[1])
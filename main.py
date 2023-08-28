import sys

class Token:
    def __init__(self, type : str, value : int):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source: str, position : int = 0):
        self.source = source
        self.position = 0
        self.next = Token
    
    def selectNext(self):
        if self.position == len(self.source):
            self.next = Token("EOF", " ")

        elif self.source[self.position] == " ":
            self.position += 1
            self.selectNext()
            
        elif self.source[self.position] == "+":
            self.position += 1
            self.next = Token("PLUS", self.source[self.position])
            return self.next

        elif self.source[self.position] == "-":
            self.position += 1
            self.next = Token("MINUS",  self.source[self.position])
            return self.next


        elif self.source[self.position].isnumeric():
            numero_completo = self.source[self.position]
            self.position += 1

            while self.position <= len(self.source):
                
                if self.source[self.position].isnumeric():
                    numero_completo += self.source[self.position]
                    self.position += 1

                else :
                    self.next = Token("NUM", int(numero_completo))
                    return self.next
                
            self.next = Token("NUM", int(numero_completo))
            return self.next
        
        
        else:
            raise Exception("aaa")
        
    
        
class Parser:
    tokens: Tokenizer

    def parseExpression():
        Parser.tokens.selectNext()
        resultado = 0

        while Parser.tokens.next.type != "EOF":
            if Parser.tokens.next.type == "NUM":
                resultado = Parser.tokens.next.value
                Parser.tokens.selectNext()

                while Parser.tokens.next.type == "PLUS" or Parser.tokens.next.type == "MINUS":
                    if Parser.tokens.next.type == "PLUS":
                        Parser.tokens.selectNext()
                        if Parser.tokens.next.type == "NUM":
                            resultado += Parser.tokens.next.value()

                    elif Parser.tokens.next.type == "MINUS":
                        Parser.tokens.selectNext()
                        if Parser.tokens.next.type == "NUM":
                            resultado -= Parser.tokens.next.value()
                    Parser.tokens.selectNext()

        print(resultado)
        return resultado    

    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.parseExpression()


Parser.run(sys.argv[1])
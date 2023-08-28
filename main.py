import sys

class Token:
    def __init__(self, type : str, value : int):
        self.type = type
        self.value = value

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

            elif current_char == " ":
                self.position += 1
                continue

            else:
                raise Exception("Invalid char")

        self.next = Token("EOF", 0)            


class Parser:
    tokens: None

    def parseExpression():
        resultado = 0
        Parser.tokens.selectNext()


        while Parser.tokens.next.type != "EOF":
            if Parser.tokens.next.type == "NUM":
                resultado = Parser.tokens.next.value
                Parser.tokens.selectNext()

                while Parser.tokens.next.type == "PLUS" or Parser.tokens.next.type == "MINUS":
                    if Parser.tokens.next.type == "PLUS":
                        Parser.tokens.selectNext()

                        if Parser.tokens.next.type == "NUM":
                            resultado += Parser.tokens.next.value
                        else:
                            raise Exception("aaa")

                    elif Parser.tokens.next.type == "MINUS":
                        Parser.tokens.selectNext()

                        if Parser.tokens.next.type == "NUM":
                            resultado -= Parser.tokens.next.value
                        else:
                            raise Exception("aaa")
                    
                else:
                    raise Exception("erro na string")
                        
                    Parser.tokens.selectNext()

                print(resultado)
                return resultado


                    
        else:
            raise Exception("aaa")
    

    

    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.parseExpression()


Parser.run(sys.argv[1])
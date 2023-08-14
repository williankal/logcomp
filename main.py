import sys

def ignora_espaco(string):
    tira_espaco = string.replace(" ", "")
    return tira_espaco

def check_erros(string):
    if len(string) == 0 or ('+' not in string and '-' not in string):
        raise ValueError
    else:
        return 

def operacao_aritmetica(string):
    
import sys

def ignora_espaco(string):
    tira_espaco = string.replace(" ", "")
    return tira_espaco

def check_erros(string):
    if len(string) == 0 or ('+' not in string and '-' not in string):
        raise ValueError
    
    elif string[0] == '+' or string[0] == '-':   
        raise ValueError
    
    else:
        return 

def operacao_aritmetica(string):
    lista_soma = string.split('+')
    lista_sub = []
    valor = 0
    for i in lista_soma:
        if "-" in i:
            lista_sub.append(i)
        else:
            valor += int(i)

    if len(lista_sub) > 0:
        for i in lista_sub:
            string_subs = i.split('-')
            for index, value in enumerate(string_subs):
                if index == 0:
                    valor += int(value)
                else:
                    valor -= int(value)          
    return valor

recebido = sys.argv[1]

recebido_sem = ignora_espaco(recebido)
check_erros(recebido_sem)
resultado = operacao_aritmetica(recebido_sem)
print(resultado)





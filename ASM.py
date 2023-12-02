Init = """; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data

    formatin : db "%d" , 0
    formatout : db "%d" , 10 , 0 ; newline , nul terminator
    scanint : times 4 db 0 ; 32-bits integer = 4 bytes

segment .bss ; variaveis
    res RESB 1
    extern fflush
    extern stdout

section .text

    global main ; Linux
    extern scanf ; Linux
    extern printf ; Linux

; subrotinas if / while
binop_je:
    JE binop_true
    JMP binop_false

binop_jg:
    JG binop_true
    JMP binop_false

binop_jl:
    JL binop_true
    JMP binop_false

binop_false:
    MOV EAX, False
    JMP binop_exit

binop_true:
    MOV EAX, True

binop_exit:
    RET

main:

    PUSH EBP ; guarda o base pointer
    MOV EBP, ESP ; estabelece um novo base pointer

    ; codigo gerado pelo compilador
"""

last = """
    ; depois que terminar de gerar o código:
    PUSH DWORD [stdout]
    CALL fflush
    ADD ESP, 4
    MOV ESP, EBP
    POP EBP
    MOV EAX, 1
    XOR EBX, EBX
    INT 0x80
"""

class Writer:
    
    def __init__(self, filename="programa.asm"):
        self.arquivo = filename
        self.id = 0
        self.write_initialization()
        
    def write_initialization(self):
        with open(self.file, "w") as arquivo:
            arquivo.write(Init + '\n')

    def write(self, content):
        with open(self.file, "a") as arquivo:
            arquivo.write("    " + content + '\n')
    
    def close(self):
        self.write_line(last)
        
    def get_unique_id(self):
        self.id += 1
        return self.id

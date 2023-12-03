; constantes
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

    PUSH DWORD 0

    PUSH DWORD 0

    MOV EAX, 1 ; O IntVal carrega o valor 1 em EAX

    PUSH EAX ; O BinOp recupera o valor da pilha em EAX

    MOV EAX, 3 ; O IntVal carrega o valor 3 em EAX

    POP EBX; O BinOp guarda o resultado na pilha

    ADD EAX, EBX

    MOV [EBP-4], EAX ;
    MOV EAX, [EBP-4] ; Evaluate do Iden None
    MOV [EBP-8], EAX ;
    MOV EAX, 1 ; O IntVal carrega o valor 1 em EAX

    PUSH EAX ; O BinOp recupera o valor da pilha em EAX

    MOV EAX, [EBP-4] ; Evaluate do Iden None
    POP EBX; O BinOp guarda o resultado na pilha

    CMP EAX, EBX ; O BinOp executa a operacao correspondente

    CALL binop_jg

    CMP EAX, False ;
    JE EXIST_<bound method Writer.get_unique_id of <ASM.Writer object at 0x0000027CEBCAE020>> ;
    MOV EAX, 1 ; O IntVal carrega o valor 1 em EAX

    PUSH EAX ; O BinOp recupera o valor da pilha em EAX

    MOV EAX, 5 ; O IntVal carrega o valor 5 em EAX

    POP EBX; O BinOp guarda o resultado na pilha

    SUB EAX, EBX

    MOV [EBP-4], EAX ;
    JMP EXIT_<bound method Writer.get_unique_id of <ASM.Writer object at 0x0000027CEBCAE020>> ;
    ELSE_<bound method Writer.get_unique_id of <ASM.Writer object at 0x0000027CEBCAE020>>: ;
    EXIT_<bound method Writer.get_unique_id of <ASM.Writer object at 0x0000027CEBCAE020>>: ;
    MOV EAX, 3 ; O IntVal carrega o valor 3 em EAX

    PUSH EAX ; O BinOp recupera o valor da pilha em EAX

    MOV EAX, [EBP-4] ; Evaluate do Iden None
    POP EBX; O BinOp guarda o resultado na pilha

    CMP EAX, EBX ; O BinOp executa a operacao correspondente

    CALL binop_je

    CMP EAX, False ;
    JE EXIST_<bound method Writer.get_unique_id of <ASM.Writer object at 0x0000027CEBCAE020>> ;
    JMP EXIT_<bound method Writer.get_unique_id of <ASM.Writer object at 0x0000027CEBCAE020>> ;
    ELSE_<bound method Writer.get_unique_id of <ASM.Writer object at 0x0000027CEBCAE020>>: ;
    MOV EAX, 3 ; O IntVal carrega o valor 3 em EAX

    MOV [EBP-4], EAX ;
    EXIT_<bound method Writer.get_unique_id of <ASM.Writer object at 0x0000027CEBCAE020>>: ;
    LOOP_I<bound method Writer.get_unique_id of <ASM.Writer object at 0x0000027CEBCAE020>>: ;
    MOV EAX, 5 ; O IntVal carrega o valor 5 em EAX

    PUSH EAX ; O BinOp recupera o valor da pilha em EAX

    MOV EAX, [EBP-4] ; Evaluate do Iden None
    POP EBX; O BinOp guarda o resultado na pilha

    CMP EAX, EBX ; O BinOp executa a operacao correspondente

    CALL binop_jl

    CMP EAX, False ;
    JE EXIT_<bound method Writer.get_unique_id of <ASM.Writer object at 0x0000027CEBCAE020>> ;
    MOV EAX, 1 ; O IntVal carrega o valor 1 em EAX

    PUSH EAX ; O BinOp recupera o valor da pilha em EAX

    MOV EAX, [EBP-4] ; Evaluate do Iden None
    POP EBX; O BinOp guarda o resultado na pilha

    ADD EAX, EBX

    MOV [EBP-4], EAX ;
    MOV EAX, 1 ; O IntVal carrega o valor 1 em EAX

    PUSH EAX ; O BinOp recupera o valor da pilha em EAX

    MOV EAX, [EBP-4] ; Evaluate do Iden None
    POP EBX; O BinOp guarda o resultado na pilha

    SUB EAX, EBX

    MOV [EBP-8], EAX ;
    JMP LOOP_I<bound method Writer.get_unique_id of <ASM.Writer object at 0x0000027CEBCAE020>> ;
    EXIT_<bound method Writer.get_unique_id of <ASM.Writer object at 0x0000027CEBCAE020>>: ;
    MOV EAX, [EBP-4] ; Evaluate do Iden None
    PUSH EAX ;
    PUSH formatout ;
    CALL printf ;
    ADD ESP, 8 ;

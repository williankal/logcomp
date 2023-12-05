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

    PUSH DWORD 0

    PUSH scanint ;
    PUSH formatin ;
    CALL scanf ;
    ADD ESP, 8 ;
    MOV EAX, DWORD [scanint] ;
    MOV [EBP-8], EAX ;
    MOV EAX, 1 ; O IntVal carrega o valor 1 em EAX

    MOV [EBP-12], EAX ;
    LOOP_0: ;
    MOV EAX, 1 ; O IntVal carrega o valor 1 em EAX

    PUSH EAX ; O BinOp recupera o valor da pilha em EAX

    MOV EAX, [EBP-8] ; Evaluate do Iden None
    POP EBX; O BinOp guarda o resultado na pilha

    ADD EAX, EBX

    PUSH EAX ; O BinOp recupera o valor da pilha em EAX

    MOV EAX, [EBP-4] ; Evaluate do Iden None
    POP EBX; O BinOp guarda o resultado na pilha

    CMP EAX, EBX ; O BinOp executa a operacao correspondente

    CALL binop_jl

    CMP EAX, False ;
    JE EXIT_0 ;
    MOV EAX, 1 ; O IntVal carrega o valor 1 em EAX

    PUSH EAX ; O BinOp recupera o valor da pilha em EAX

    MOV EAX, [EBP-4] ; Evaluate do Iden None
    POP EBX; O BinOp guarda o resultado na pilha

    ADD EAX, EBX

    MOV [EBP-4], EAX ;
    MOV EAX, [EBP-4] ; Evaluate do Iden None
    PUSH EAX ; O BinOp recupera o valor da pilha em EAX

    MOV EAX, [EBP-12] ; Evaluate do Iden None
    POP EBX; O BinOp guarda o resultado na pilha

    IMUL EBX

    MOV [EBP-12], EAX ;
    JMP LOOP_0 ;
    EXIT_0: ;
    MOV EAX, [EBP-12] ; Evaluate do Iden None
    PUSH EAX ;
    PUSH formatout ;
    CALL printf ;
    ADD ESP, 8 ;
    
    ; depois que terminar de gerar o código:
    PUSH DWORD [stdout]
    CALL fflush
    ADD ESP, 4
    MOV ESP, EBP
    POP EBP
    MOV EAX, 1
    XOR EBX, EBX
    INT 0x80


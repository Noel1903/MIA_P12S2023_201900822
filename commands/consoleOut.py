
class consoleOut:
    def __init__(self):
        self.consoleOut = ""

    def getConsoleOut(self):
        return self.consoleOut
    
    def setConsoleOut(self, consoleOut):
        self.consoleOut = consoleOut

    def updateConsoleOut(self, consoleOut):
        self.consoleOut += consoleOut
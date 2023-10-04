import os
class rmdisk:
    def __init__(self,path):
        self.path = path
        self.console = ""
        self.execute()

    def execute(self):
        self.path = self.path.replace(' ',r'\ ')
        if os.path.exists(self.path):
            os.remove(self.path)
            #print("Disco "+os.path.basename(self.path)+"  eliminado correctamente")
            self.console = "Disco "+os.path.basename(self.path)+"  eliminado correctamente"+ "\n"
            return self.console
        else:
            #print("Disco no encontrado")
            self.console = "Disco no encontrado o disco no existe"+ "\n"
            return self.console
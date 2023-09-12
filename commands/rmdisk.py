import os
class rmdisk:
    def __init__(self,path):
        self.path = path
        self.execute()

    def execute(self):
        self.path = self.path.replace(' ',r'\ ')
        if os.path.exists(self.path):
            os.remove(self.path)
            print("Disco "+os.path.basename(self.path)+"  eliminado correctamente")
        else:
            print("Disco no encontrado")
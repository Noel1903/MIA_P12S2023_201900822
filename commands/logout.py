from  commands.login import login
class logout:
    def __init__(self,param):
        self.param = param
        self.console = ""
        self.execute()

    def execute(self):
        if self.param == "logout":
            log = login(None)
            log.setUserLogued()
            #print("Sesión cerrada correctamente")
            #input("Presiona Enter para continuar...")
            self.console = "Sesión cerrada correctamente"
            return self.console
        else:
            #print("No se reconoce el comando logout")
            self.console = "No se reconoce el comando logout"
            return self.console
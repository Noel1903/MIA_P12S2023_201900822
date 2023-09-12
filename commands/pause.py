class pause:

    def __init__(self,paramas):
        self.params = paramas
        self.execute()

    def execute(self):
        if self.params == "pause":
            input("Presiona Enter para continuar...")
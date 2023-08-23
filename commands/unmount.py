from commands.mount import mount 
class unmount:
    def __init__(self, id):
        self.id = id
        self.execute()

    def execute(self):
        exist = False
        m = mount(None)
        for i in m.partitions_mounted:
            if i.part_id.rstrip("\x00") == self.id[0][1]:
            
                m.partitions_mounted.remove(i)
                print("Particion desmontada correctamente")
                m.showPartitions()
                return
        if not exist:
            print("No se encontró esta particion montada")
            m.showPartitions()
            return

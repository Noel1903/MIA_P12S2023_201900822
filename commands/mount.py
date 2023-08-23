import os,struct
from structs.struct import Mount
class mount:
    partitions_mounted = []
    id_carnet = "22"
    def __init__(self, params=None):
        self.params = params
        self.path = ""
        self.name = ""
        if params != None:
            self.execute()

   
    

    def nameExist(self,name,partition1,partition2,partition3,partition4):
        name_partition1 = partition1.decode('utf-8').replace(" ","").strip("\x00")
        name_partition2 = partition2.decode('utf-8').replace(" ","").strip("\x00")
        name_partition3 = partition3.decode('utf-8').replace(" ","").strip("\x00")
        name_partition4 = partition4.decode('utf-8').replace(" ","").strip("\x00")
        if (name_partition1 != name) and (name_partition2 != name) and (name_partition3 != name) and (name_partition4 != name):
            return False
        else:
            return True
        
    def getCont(self,nameDisk):
        count = 1
        for i in self.partitions_mounted:
            if i.nameDisk == nameDisk:
                count =  i.count + 1  
        return count

    def execute(self):
        for param in self.params:
            if param[0] == "path":
                self.path = param[1]
            elif param[0] == "name":
                self.name = param[1]
        self.mount()

        self.showPartitions()

    def showPartitions(self):
        for i in self.partitions_mounted:
            print("Nombre: " + i.nameDisk + " ID: " + i.part_id + " Contador: " + str(i.count))

    def mount(self):

        name_disk = os.path.basename(self.path)[:-4]
        with open(self.path.replace(" ",r"\ "), "rb+") as f:
            f.seek(0)
            format_mbr = "I I I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
            data_bytes = f.read(struct.calcsize(format_mbr))
            mbr_unpack = struct.unpack(format_mbr,data_bytes)
            
            partition1 = mbr_unpack[4:10]
            partition2 = mbr_unpack[10:16]
            partition3 = mbr_unpack[16:22]
            partition4 = mbr_unpack[22:28]
            if self.nameExist(self.name,partition1[5],partition2[5],partition3[5],partition4[5]):
                if self.name == partition1[5].decode('utf-8').rstrip("\x00"):
                    cont = self.getCont(name_disk)
                    id_mount = self.id_carnet + str(cont) + name_disk
                    self.partitions_mounted.append(Mount(name_disk,id_mount,cont))
                    print("Particion montada con exito")
                    return        
                elif self.name == partition2[5].decode('utf-8').rstrip("\x00"):
                    cont = self.getCont(name_disk)
                    id_mount = self.id_carnet + str(cont) + name_disk
                    self.partitions_mounted.append(Mount(name_disk,id_mount,cont)) 
                    print("Particion montada con exito")
                    return
                elif self.name == partition3[5].decode('utf-8').rstrip("\x00"):
                    cont = self.getCont(name_disk)
                    id_mount = self.id_carnet + str(cont) + name_disk
                    self.partitions_mounted.append(Mount(name_disk,id_mount,cont)) 
                    print("Particion montada con exito")
                    return  
                elif self.name == partition4[5].decode('utf-8').rstrip("\x00"):
                    cont = self.getCont(name_disk)
                    id_mount = self.id_carnet + str(cont) + name_disk
                    self.partitions_mounted.append(Mount(name_disk,id_mount,cont)) 
                    print("Particion montada con exito")
                    return      

            f.close()



    
from structs.struct import MBR
import struct
class fdisk:
    def __init__(self, params):
        self.params = params
        self.path = ""
        self.name = ""
        self.type = "p"
        self.size = 0
        self.unit = "k"
        self.fit = "ff"
        self.delete = ""
        self.add = ""
        self.execute()

    def createPartition(self):
        if self.unit == "b":
            self.size = self.size
        elif self.unit == "k":
            self.size = self.size * 1024
        elif self.unit == "m":
            self.size = self.size * 1024 * 1024
        else:
            print("La unidad no esta definida")
            return
        
        if self.delete != "" and self.add != "":
            print("No se puede eliminar y agregar particiones al mismo tiempo")
            return
        elif self.delete != "":
            print("Eliminar particion")
        elif self.add != "":
            print("Agregar particion")
        else:
            if self.type == "p":
                self.createPartitionP()
            '''elif self.type == "e":
                self.createPartitionE()
            elif self.type == "l":
                self.createPartitionL()'''
        
    
    def execute(self):
        for param in self.params:
            if param[0] == 'path':
                self.path = param[1]
            elif param[0] == 'name':
                self.name = param[1]
            elif param[0] == 'type':
                self.type = param[1].lower()
            elif param[0] == 'size':
                self.size = int(param[1])
            elif param[0] == "unit":
                self.unit = param[1].lower()
            elif param[0] == "fit":
                self.fit = param[1].lower()
            elif param[0] == "delete":
                self.delete = param[1].lower()
            elif param[0] == "add":
                self.add = int(param[1])
        if self.path != "" and self.name != "" and self.size > 0:
            self.createPartition()
        else:
            print("Ruta,nombre y tamaño son obligatorios")
        
    def createPartitionP(self):
        print("Creando particion primaria . . . ")
        route_path = self.path.replace(" ",r"\ ")
        with open(route_path,"rb+") as f:
            f.seek(0)
            format_mbr = "I Q I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
            data_bytes = f.read(struct.calcsize(format_mbr))
            mbr_unpack = struct.unpack(format_mbr,data_bytes)
            type_p = mbr_unpack[3].decode('utf-8').rstrip("\x00")
            
            partition1 = mbr_unpack[4:10]
            partition2 = mbr_unpack[10:16]
            partition3 = mbr_unpack[16:22]
            partition4 = mbr_unpack[22:28]
            type_p = type_p.replace(" ",r"")
            if type_p == 'f':
                self.setFirstFit(partition1,partition2,partition3,partition4,mbr_unpack)
            
            f.close()

    def setFirstFit(self,partition1,partition2,partition3,partition4,mbr_unpack):
        name_partition = partition1[5].decode('utf-8').replace(" ","")
        if name_partition == "FREE":
            if self.size > mbr_unpack[0]:
                print("El tamaño de la particion es mayor al tamaño del disco")
                return
            format_mbr = "I Q I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
            fit_disk = mbr_unpack[3].decode('utf-8')
            mbr_bytes = struct.pack(format_mbr,mbr_unpack[0],mbr_unpack[1],mbr_unpack[2],fit_disk[0].encode('utf-8'),
                '1'.encode('utf-8'),self.type[0].encode('utf-8'),self.fit[0].encode('utf-8'),struct.calcsize(format_mbr),self.size,self.name.encode('utf-8')[0:16],
                partition2[0],partition2[1],partition2[2],partition2[3],partition2[4],partition2[5],
                partition3[0],partition3[1],partition3[2],partition3[3],partition3[4],partition3[5],
                partition4[0],partition4[1],partition4[2],partition4[3],partition4[4],partition4[5])
            with open(self.path.replace(" ",r"\ "),"rb+") as f:
                f.seek(0)
                f.write(mbr_bytes)
                f.close()
                print("Particion creada exitosamente")
        else:
            name_partition = partition2[5].decode('utf-8').replace(" ","")
        if name_partition == "FREE":
            if self.size > mbr_unpack[0]:
                print("El tamaño de la particion es mayor al tamaño del disco")
                return
            format_mbr = "I Q I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
            fit_disk = mbr_unpack[3].decode('utf-8')
            mbr_bytes = struct.pack(format_mbr,mbr_unpack[0],mbr_unpack[1],mbr_unpack[2],fit_disk[0].encode('utf-8'),
                partition1[0],partition1[1],partition1[2],partition1[3],partition1[4],partition1[5],
                '1'.encode('utf-8'),self.type[0].encode('utf-8'),self.fit[0].encode('utf-8'),struct.calcsize(format_mbr)+partition1[4],self.size,self.name.encode('utf-8')[0:16],
                partition3[0],partition3[1],partition3[2],partition3[3],partition3[4],partition3[5],
                partition4[0],partition4[1],partition4[2],partition4[3],partition4[4],partition4[5])
            with open(self.path.replace(" ",r"\ "),"rb+") as f:
                f.seek(0)
                f.write(mbr_bytes)
                f.close()
                print("Particion creada exitosamente")
        else:
            name_partition = partition3[5].decode('utf-8').replace(" ","")
        if name_partition == "FREE":
            if self.size > mbr_unpack[0]:
                print("El tamaño de la particion es mayor al tamaño del disco")
                return
            format_mbr = "I Q I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
            fit_disk = mbr_unpack[3].decode('utf-8')
            mbr_bytes = struct.pack(format_mbr,mbr_unpack[0],mbr_unpack[1],mbr_unpack[2],fit_disk[0].encode('utf-8'),
                partition1[0],partition1[1],partition1[2],partition1[3],partition1[4],partition1[5],
                partition2[0],partition2[1],partition2[2],partition2[3],partition2[4],partition2[5],
                '1'.encode('utf-8'),self.type[0].encode('utf-8'),self.fit[0].encode('utf-8'),struct.calcsize(format_mbr)+partition1[4]+partition2[4],self.size,self.name.encode('utf-8')[0:16],
                partition4[0],partition4[1],partition4[2],partition4[3],partition4[4],partition4[5])
            with open(self.path.replace(" ",r"\ "),"rb+") as f:
                f.seek(0)
                f.write(mbr_bytes)
                f.close()
                print("Particion creada exitosamente")
        else:
            name_partition = partition4[5].decode('utf-8').replace(" ","")
        if name_partition == "FREE":
            if self.size > mbr_unpack[0]:
                print("El tamaño de la particion es mayor al tamaño del disco")
                return
            format_mbr = "I Q I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
            fit_disk = mbr_unpack[3].decode('utf-8')
            mbr_bytes = struct.pack(format_mbr,mbr_unpack[0],mbr_unpack[1],mbr_unpack[2],fit_disk[0].encode('utf-8'),
                partition1[0],partition1[1],partition1[2],partition1[3],partition1[4],partition1[5],
                partition2[0],partition2[1],partition2[2],partition2[3],partition2[4],partition2[5],
                partition3[0],partition3[1],partition3[2],partition3[3],partition3[4],partition3[5],
                '1'.encode('utf-8'),self.type[0].encode('utf-8'),self.fit[0].encode('utf-8'),struct.calcsize(format_mbr)+partition1[4]+partition2[4],self.size,self.name.encode('utf-8')[0:16])
            with open(self.path.replace(" ",r"\ "),"rb+") as f:
                f.seek(0)
                f.write(mbr_bytes)
                f.close()
                print("Particion creada exitosamente")
        else:
            print("No hay espacio para crear la particion")
            return

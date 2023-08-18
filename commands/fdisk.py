from structs.struct import MBR,EBR
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

    def isLong(self,sizeP,start,end):
        if sizeP > (end-start):
            return True
        else:
            return False

    def nameExist(self,name,partition1,partition2,partition3,partition4):
        name_partition1 = partition1.decode('utf-8').replace(" ","").strip("\x00")
        name_partition2 = partition2.decode('utf-8').replace(" ","").strip("\x00")
        name_partition3 = partition3.decode('utf-8').replace(" ","").strip("\x00")
        name_partition4 = partition4.decode('utf-8').replace(" ","").strip("\x00")
        if (name_partition1 != name) and (name_partition2 != name) and (name_partition3 != name) and (name_partition4 != name):
            return False
        else:
            return True
        
    def existExtend(self,partition1,partition2,partition3,partition4):
        name_partition1 = partition1.decode('utf-8').strip("\x00")
        name_partition2 = partition2.decode('utf-8').strip("\x00")
        name_partition3 = partition3.decode('utf-8').strip("\x00")
        name_partition4 = partition4.decode('utf-8').strip("\x00")
        if (name_partition1 == "e") or (name_partition2 == "e") or (name_partition3 == "e") or (name_partition4 == "e"):
            return True
        else:
            return False

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
            elif self.type == "e":
                self.createPartitionE()
            elif self.type == "l":
                self.createPartitionL()
        
    
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
                if self.nameExist(self.name,partition1[5],partition2[5],partition3[5],partition4[5]):
                    print("Ya existe una particion con ese nombre")
                    return
                self.setFirstFit(partition1,partition2,partition3,partition4,mbr_unpack)
            
            f.close()

    def setFirstFit(self,partition1,partition2,partition3,partition4,mbr_unpack):
        format_mbr = "I Q I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
        name_partition = partition1[5].decode('utf-8').replace(" ","")
        if name_partition == "FREE":
            if self.size > mbr_unpack[0]:
                print("El tamaño de la particion es mayor al tamaño del disco")
                return
            if (struct.calcsize(format_mbr)+self.size) > mbr_unpack[0]:
                print("La particion es muy grande")
                return
            if partition2[3]>0:
                if self.isLong(self.size,struct.calcsize(format_mbr),partition2[3]):
                    print("La particion es muy grande")
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
                return
        else:
            name_partition = partition2[5].decode('utf-8').replace(" ","")
        if name_partition == "FREE":
            if self.size > mbr_unpack[0]:
                print("El tamaño de la particion es mayor al tamaño del disco")
                return
            if (struct.calcsize(format_mbr)+self.size+partition1[4]) > mbr_unpack[0]:
                print("La particion es muy grande")
                return
            if partition3[3]>0:
                if self.isLong(self.size,struct.calcsize(format_mbr)+partition1[4],partition3[3]):
                    print("La particion es muy grande")
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
                return
        else:
            name_partition = partition3[5].decode('utf-8').replace(" ","")
        if name_partition == "FREE":
            if self.size > mbr_unpack[0]:
                print("El tamaño de la particion es mayor al tamaño del disco")
                return
            if (struct.calcsize(format_mbr)+self.size+partition1[4]+partition2[4]) > mbr_unpack[0]:
                print("La particion es muy grande")
                return
            if partition4[3]>0:
                if self.isLong(self.size,struct.calcsize(format_mbr)+partition1[4]+partition2[4],partition4[3]):
                    print("La particion es muy grande")
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
                return
        else:
            name_partition = partition4[5].decode('utf-8').replace(" ","")
        if name_partition == "FREE":
            if self.size > mbr_unpack[0]:
                print("El tamaño de la particion es mayor al tamaño del disco")
                return
            if self.isLong(self.size,struct.calcsize(format_mbr)+partition1[4]+partition2[4]+partition3[4],mbr_unpack[0]):
                    print("La particion es muy grande")
                    return
            format_mbr = "I Q I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
            fit_disk = mbr_unpack[3].decode('utf-8')
            mbr_bytes = struct.pack(format_mbr,mbr_unpack[0],mbr_unpack[1],mbr_unpack[2],fit_disk[0].encode('utf-8'),
                partition1[0],partition1[1],partition1[2],partition1[3],partition1[4],partition1[5],
                partition2[0],partition2[1],partition2[2],partition2[3],partition2[4],partition2[5],
                partition3[0],partition3[1],partition3[2],partition3[3],partition3[4],partition3[5],
                '1'.encode('utf-8'),self.type[0].encode('utf-8'),self.fit[0].encode('utf-8'),struct.calcsize(format_mbr)+partition1[4]+partition2[4]+partition3[4],self.size,self.name.encode('utf-8')[0:16])
            with open(self.path.replace(" ",r"\ "),"rb+") as f:
                f.seek(0)
                f.write(mbr_bytes)
                f.close()
                print("Particion creada exitosamente")
                return
        else:
            print("No hay espacio para crear la particion")
            return

    def createPartitionE(self):
        print("Creando particion extendida . . . ")
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
                if self.nameExist(self.name,partition1[5],partition2[5],partition3[5],partition4[5]):
                    print("Ya existe una particion con ese nombre")
                    return
                if self.existExtend(partition1[1],partition2[1],partition3[1],partition4[1]):
                    print("Ya existe una particion extendida")
                    return
                self.setFirstFitExtend(partition1,partition2,partition3,partition4,mbr_unpack)
            
            f.close()

    def setFirstFitExtend(self,partition1,partition2,partition3,partition4,mbr_unpack):
        format_mbr = "I Q I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
        format_ebr = "c c I I i 16s"
        ebr  = EBR('0','f',0,0,-1,"ebr_part_namebit")
        name_partition = partition1[5].decode('utf-8').replace(" ","")
        if name_partition == "FREE":
            if self.size > mbr_unpack[0]:
                print("El tamaño de la particion es mayor al tamaño del disco")
                return
            if (struct.calcsize(format_mbr)+self.size) > mbr_unpack[0]:
                print("La particion es muy grande")
                return
            if partition2[3]>0:
                if self.isLong(self.size,struct.calcsize(format_mbr),partition2[3]):
                    print("La particion es muy grande")
                    return
            format_mbr = "I Q I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
            fit_disk = mbr_unpack[3].decode('utf-8')
            mbr_bytes = struct.pack(format_mbr,mbr_unpack[0],mbr_unpack[1],mbr_unpack[2],fit_disk[0].encode('utf-8'),
                '1'.encode('utf-8'),self.type[0].encode('utf-8'),self.fit[0].encode('utf-8'),struct.calcsize(format_mbr),self.size,self.name.encode('utf-8')[0:16],
                partition2[0],partition2[1],partition2[2],partition2[3],partition2[4],partition2[5],
                partition3[0],partition3[1],partition3[2],partition3[3],partition3[4],partition3[5],
                partition4[0],partition4[1],partition4[2],partition4[3],partition4[4],partition4[5])
            ebr_bytes = struct.pack(format_ebr,
                                    ebr.part_status.encode('utf-8'),
                                    ebr.part_fit.encode('utf-8'),
                                    struct.calcsize(format_mbr),
                                    ebr.part_s,
                                    ebr.part_next,
                                    ebr.part_name.encode('utf-8'))
            with open(self.path.replace(" ",r"\ "),"rb+") as f:
                f.seek(0)
                f.write(mbr_bytes)
                f.seek(struct.calcsize(format_mbr))
                f.write(ebr_bytes)
                f.close()
                print("Particion creada exitosamente")
                return
        else:
            name_partition = partition2[5].decode('utf-8').replace(" ","")
        if name_partition == "FREE":
            if self.size > mbr_unpack[0]:
                print("El tamaño de la particion es mayor al tamaño del disco")
                return
            if (struct.calcsize(format_mbr)+self.size+partition1[4]) > mbr_unpack[0]:
                print("La particion es muy grande")
                return
            if partition3[3]>0:
                if self.isLong(self.size,struct.calcsize(format_mbr)+partition1[4],partition3[3]):
                    print("La particion es muy grande")
                    return
            format_mbr = "I Q I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
            fit_disk = mbr_unpack[3].decode('utf-8')
            mbr_bytes = struct.pack(format_mbr,mbr_unpack[0],mbr_unpack[1],mbr_unpack[2],fit_disk[0].encode('utf-8'),
                partition1[0],partition1[1],partition1[2],partition1[3],partition1[4],partition1[5],
                '1'.encode('utf-8'),self.type[0].encode('utf-8'),self.fit[0].encode('utf-8'),struct.calcsize(format_mbr)+partition1[4],self.size,self.name.encode('utf-8')[0:16],
                partition3[0],partition3[1],partition3[2],partition3[3],partition3[4],partition3[5],
                partition4[0],partition4[1],partition4[2],partition4[3],partition4[4],partition4[5])
            ebr_bytes = struct.pack(format_ebr,
                                    ebr.part_status.encode('utf-8'),
                                    ebr.part_fit.encode('utf-8'),
                                    (struct.calcsize(format_mbr)+partition1[4]),
                                    ebr.part_s,
                                    ebr.part_next,
                                    ebr.part_name.encode('utf-8'))
            with open(self.path.replace(" ",r"\ "),"rb+") as f:
                f.seek(0)
                f.write(mbr_bytes)
                f.seek(struct.calcsize(mbr_bytes)+partition1[4])
                f.write(ebr_bytes)
                f.close()
                print("Particion creada exitosamente")
                return
        else:
            name_partition = partition3[5].decode('utf-8').replace(" ","")
        if name_partition == "FREE":
            if self.size > mbr_unpack[0]:
                print("El tamaño de la particion es mayor al tamaño del disco")
                return
            if (struct.calcsize(format_mbr)+self.size+partition1[4]+partition2[4]) > mbr_unpack[0]:
                print("La particion es muy grande")
                return
            if partition4[3]>0:
                if self.isLong(self.size,struct.calcsize(format_mbr)+partition1[4]+partition2[4],partition4[3]):
                    print("La particion es muy grande")
                    return
            format_mbr = "I Q I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
            fit_disk = mbr_unpack[3].decode('utf-8')
            mbr_bytes = struct.pack(format_mbr,mbr_unpack[0],mbr_unpack[1],mbr_unpack[2],fit_disk[0].encode('utf-8'),
                partition1[0],partition1[1],partition1[2],partition1[3],partition1[4],partition1[5],
                partition2[0],partition2[1],partition2[2],partition2[3],partition2[4],partition2[5],
                '1'.encode('utf-8'),self.type[0].encode('utf-8'),self.fit[0].encode('utf-8'),struct.calcsize(format_mbr)+partition1[4]+partition2[4],self.size,self.name.encode('utf-8')[0:16],
                partition4[0],partition4[1],partition4[2],partition4[3],partition4[4],partition4[5])
            ebr_bytes = struct.pack(format_ebr,
                                    ebr.part_status.encode('utf-8'),
                                    ebr.part_fit.encode('utf-8'),
                                    (struct.calcsize(format_mbr)+partition1[4]+partition2[4]),
                                    ebr.part_s,
                                    ebr.part_next,
                                    ebr.part_name.encode('utf-8'))
            with open(self.path.replace(" ",r"\ "),"rb+") as f:
                f.seek(0)
                f.write(mbr_bytes)
                f.seek(struct.calcsize(mbr_bytes)+partition1[4]+partition2[4])
                f.write(ebr_bytes)
                f.close()
                print("Particion creada exitosamente")
                return
        else:
            name_partition = partition4[5].decode('utf-8').replace(" ","")
        if name_partition == "FREE":
            if self.size > mbr_unpack[0]:
                print("El tamaño de la particion es mayor al tamaño del disco")
                return
            if self.isLong(self.size,struct.calcsize(format_mbr)+partition1[4]+partition2[4]+partition3[4],mbr_unpack[0]):
                    print("La particion es muy grande")
                    return
            format_mbr = "I Q I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
            fit_disk = mbr_unpack[3].decode('utf-8')
            mbr_bytes = struct.pack(format_mbr,mbr_unpack[0],mbr_unpack[1],mbr_unpack[2],fit_disk[0].encode('utf-8'),
                partition1[0],partition1[1],partition1[2],partition1[3],partition1[4],partition1[5],
                partition2[0],partition2[1],partition2[2],partition2[3],partition2[4],partition2[5],
                partition3[0],partition3[1],partition3[2],partition3[3],partition3[4],partition3[5],
                '1'.encode('utf-8'),self.type[0].encode('utf-8'),self.fit[0].encode('utf-8'),struct.calcsize(format_mbr)+partition1[4]+partition2[4]+partition3[4],self.size,self.name.encode('utf-8')[0:16])
            ebr_bytes = struct.pack(format_ebr,
                                    ebr.part_status.encode('utf-8'),
                                    ebr.part_fit.encode('utf-8'),
                                    (struct.calcsize(format_mbr)+partition1[4]+partition2[4]+partition3[4]),
                                    ebr.part_s,
                                    ebr.part_next,
                                    ebr.part_name.encode('utf-8'))
            with open(self.path.replace(" ",r"\ "),"rb+") as f:
                f.seek(0)
                f.write(mbr_bytes)
                f.seek(struct.calcsize(mbr_bytes)+partition1[4]+partition2[4]+partition3[4])
                f.write(ebr_bytes)
                f.close()
                print("Particion creada exitosamente")
                return
        else:
            print("No hay espacio para crear la particion")
            return
    
    def createPartitionL(self):
        print("Creando particion logica . . . ")
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
                if self.nameExist(self.name,partition1[5],partition2[5],partition3[5],partition4[5]):
                    print("Ya existe una particion con ese nombre")
                    return
                if self.existExtend(partition1[1],partition2[1],partition3[1],partition4[1])!=True:
                    print("No existe una particion extendida")
                    return
                self.setFirstFitLogic(partition1,partition2,partition3,partition4,mbr_unpack)
            
            f.close()

    def setFirstFitLogic(self,partition1,partition2,partition3,partition4,mbr_unpack):
        format_ebr = "c c I I i 16s"
        if partition1[1].decode('utf-8').rstrip("\x00") == 'e':
            if partition1[4]<self.size:
                print("El tamaño de la particion es mayor al tamaño de la extendida")
                return
            ebr_size = struct.calcsize(format_ebr)
            route_path = self.path.replace(" ",r"\ ")
            with open(route_path,"rb+") as f:
                f.seek(partition1[3])
                ebr_bytes = f.read(ebr_size)
                ebr_unpack = struct.unpack(format_ebr,ebr_bytes)
                
                if ebr_unpack[5].decode('utf-8').rstrip("\x00") == "ebr_part_namebit":
                    if ebr_unpack[4] != -1:
                        if self.isLong(self.size,ebr_size,ebr_unpack[4]):
                            print("La particion es muy grande")
                            return
                    ebr_pack = struct.pack(format_ebr,
                                           '1'.encode('utf-8'),
                                           self.fit[0].encode('utf-8'),
                                           ebr_size,
                                           self.size,
                                           ebr_unpack[4],
                                           self.name.encode('utf-8')[0:16])
                    f.seek(partition1[3])
                    f.write(ebr_pack)
                    print("Particion logica creada exitosamente")
                    f.close()
                    return
                else:
                    f.seek(partition1[3])
                    ebr_bytes = f.read(ebr_size)
                    ebr_unpack = struct.unpack(format_ebr,ebr_bytes)
                    size_next = ebr_unpack[4]
                    size_part = ebr_unpack[3]
                    part_init = partition1[3]
                    acumSize = partition1[3]
                    while True:
                        if size_next == -1:
                            with open(route_path,"rb+") as f:
                                f.seek(part_init)
                                print(part_init)
                                ebr_pack = struct.pack(format_ebr,
                                                        ebr_unpack[0],
                                                        ebr_unpack[1],
                                                        ebr_unpack[2],
                                                        ebr_unpack[3],
                                                        size_part,
                                                        ebr_unpack[5])
                                f.write(ebr_pack)
                                f.seek(part_init+size_part)
                                ebr_pack = struct.pack(format_ebr,
                                                        '1'.encode('utf-8'),
                                                        self.fit[0].encode('utf-8'),
                                                        ebr_size+part_init+size_part,
                                                        self.size,
                                                        -1,
                                                        self.name.encode('utf-8')[0:16])
                                f.write(ebr_pack)
                                print("Particion logica creada exitosamente")
                                f.close()
                                return
                        else:
                            acumSize=acumSize+size_next
                            print(acumSize,"Acumulado")
                            f.seek(acumSize)
                            ebr_bytes = f.read(ebr_size)
                            ebr_unpack = struct.unpack(format_ebr,ebr_bytes)
                            print(ebr_unpack)
                            size_next = ebr_unpack[4]
                            size_part = ebr_unpack[3]
                            part_init = acumSize

                            if ebr_unpack[5].decode('utf-8').rstrip("\x00") == 'ebr_part_namebit':
                                ebr_pack = struct.pack(format_ebr,
                                                        '1'.encode('utf-8'),
                                                        self.fit[0].encode('utf-8'),
                                                        part_init+ebr_size,
                                                        self.size,
                                                        ebr_unpack[4],
                                                        self.name.encode('utf-8')[0:16])
                                f.seek(part_init)
                                f.write(ebr_pack)
                                f.close()
                                print("Particion logica creada exitosamente")
                                return
                            

                                                       

                                                       

                            

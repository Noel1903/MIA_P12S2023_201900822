from structs.struct import MBR, Partition
import os,datetime,random,struct
class mkdisk:
    def __init__(self, params):
        self.params = params
        self.path = ""
        self.size = 0
        self.unit = "m"
        self.fit = "ff"
        self.execute()

    def execute(self):
        for param in self.params:
            
            
            if param[0] == 'path':
                self.path = param[1]
            elif param[0] == 'size':
                self.size = int(param[1])
            elif param[0] == "unit":
                self.unit = param[1]
            elif param[0] == "fit":
                self.fit = param[1]
        self.fit = self.fit.lower()
        self.unit = self.unit.lower()
        
        if self.size > 0:
            self.createDisk()
        else:
            print("Size must be greater than 0")

    def createDisk(self):
        if self.fit == "ff":
            self.createDiskFF()

    def createDiskFF(self):
        if self.unit == "k":
            self.size = self.size * 1024
        elif self.unit == "m":
            self.size = self.size * 1024 * 1024
        else:
            return print("Unit must be k or m")
        #mbr = MBR()
        route = self.path.replace(" ",r"\ ")
        file = os.path.basename(route)
        directory = os.path.dirname(route)
        if not os.path.exists(directory):
            os.makedirs(directory)

        route_complete = os.path.join(directory, file)
        with open(route_complete, "wb") as f:
            f.write(b'\x00' * self.size)
            f.close()

        mbr_date = datetime.datetime.now()
        mbr_disk_signature = random.randint(1, 1000000000)
        partition = Partition('0', 'P', 'f', 0,0, "FREE            ")
        format_mbr = "I Q I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
        mbr = MBR(self.size, mbr_date, mbr_disk_signature, self.fit[0].encode('utf-8'), partition, partition, partition, partition)
        mbr_bytes = struct.pack(format_mbr,self.size,int(mbr_date.timestamp()),mbr_disk_signature,self.fit[0].encode('utf-8'),
                    mbr.mbr_partition_1.part_status.encode('utf-8'),mbr.mbr_partition_1.part_type.encode('utf-8'),mbr.mbr_partition_1.part_fit.encode('utf-8'),mbr.mbr_partition_1.part_start,mbr.mbr_partition_1.part_s,mbr.mbr_partition_1.part_name.encode('utf-8'),
                    mbr.mbr_partition_2.part_status.encode('utf-8'),mbr.mbr_partition_2.part_type.encode('utf-8'),mbr.mbr_partition_2.part_fit.encode('utf-8'),mbr.mbr_partition_2.part_start,mbr.mbr_partition_2.part_s,mbr.mbr_partition_2.part_name.encode('utf-8'),
                    mbr.mbr_partition_3.part_status.encode('utf-8'),mbr.mbr_partition_3.part_type.encode('utf-8'),mbr.mbr_partition_3.part_fit.encode('utf-8'),mbr.mbr_partition_3.part_start,mbr.mbr_partition_3.part_s,mbr.mbr_partition_3.part_name.encode('utf-8'),
                    mbr.mbr_partition_4.part_status.encode('utf-8'),mbr.mbr_partition_4.part_type.encode('utf-8'),mbr.mbr_partition_4.part_fit.encode('utf-8'),mbr.mbr_partition_4.part_start,mbr.mbr_partition_4.part_s,mbr.mbr_partition_4.part_name.encode('utf-8'))
        
        with open(route_complete, "rb+") as f:
            f.seek(0)
            f.write(mbr_bytes)
            f.close()
        print("Disco "+file+" creado con exito en : "+self.path)

        
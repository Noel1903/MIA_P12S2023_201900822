
#import datetime,struct



class Partition:
    def __init__(self,part_status,part_type,part_fit,part_start,part_s,part_name):
        self.part_status = part_status
        self.part_type = part_type
        self.part_fit = part_fit
        self.part_start = part_start
        self.part_s = part_s
        self.part_name = part_name

class MBR:
    def __init__(self,mbr_tamano,mbr_fecha_creacion,mbr_dsk_signature,dsk_fit,mbr_partition_1,mbr_partition_2,mbr_partition_3,mbr_partition_4):
        self.mbr_tamano = mbr_tamano
        self.mbr_fecha_creacion = mbr_fecha_creacion
        self.mbr_dsk_signature = mbr_dsk_signature
        self.dsk_fit = dsk_fit
        self.mbr_partition_1 = mbr_partition_1
        self.mbr_partition_2 = mbr_partition_2
        self.mbr_partition_3 = mbr_partition_3
        self.mbr_partition_4 = mbr_partition_4



'''
from dataclasses import dataclass
@dataclass
class Partition:
    part_status: chr
    part_type: chr
    part_fit: chr
    part_start: int
    part_s: int
    part_name: str
    
@dataclass
class MBR:
    mbr_tamano: int
    mbr_fecha_creacion: datetime
    mbr_dsk_signature: int
    dsk_fit: chr
    mbr_partition_1: Partition
    mbr_partition_2: Partition
    mbr_partition_3: Partition
    mbr_partition_4: Partition
'''

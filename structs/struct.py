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

class EBR:
    def __init__(self,part_status,part_fit,part_start,part_s,part_next,part_name):
        self.part_status = part_status
        self.part_fit = part_fit
        self.part_start = part_start
        self.part_s = part_s
        self.part_next = part_next
        self.part_name = part_name

class Mount:
    def __init__(self,nameDisk,part_id,count,name_partition,path):
        self.nameDisk = nameDisk
        self.part_id = part_id
        self.count = count
        self.name_partition = name_partition
        self.path = path

class SuperBlock:
    def __init__(self,s_filesystem_type,s_inodes_count,s_blocks_count,s_free_blocks_count,s_free_inodes_count,s_mtime,s_umtime,s_mnt_count,s_magic,s_inode_size,s_block_size,s_first_ino,s_first_blo,s_bm_inode_start,s_bm_block_start,s_inode_start,s_block_start):
        self.s_filesystem_type = s_filesystem_type
        self.s_inodes_count = s_inodes_count
        self.s_blocks_count = s_blocks_count
        self.s_free_blocks_count = s_free_blocks_count
        self.s_free_inodes_count = s_free_inodes_count
        self.s_mtime = s_mtime
        self.s_umtime = s_umtime
        self.s_mnt_count = s_mnt_count
        self.s_magic = s_magic
        self.s_inode_s = s_inode_size
        self.s_block_s = s_block_size
        self.s_first_ino = s_first_ino
        self.s_first_blo = s_first_blo
        self.s_bm_inode_start = s_bm_inode_start
        self.s_bm_block_start = s_bm_block_start
        self.s_inode_start = s_inode_start
        self.s_block_start = s_block_start

class Inode:
    def __init__(self,i_uid,i_gid,i_size,i_atime,i_ctime,i_mtime,i_block,i_type,i_perm):
        self.i_uid = i_uid
        self.i_gid = i_gid
        self.i_s = i_size
        self.i_atime = i_atime
        self.i_ctime = i_ctime
        self.i_mtime = i_mtime
        self.i_block = i_block
        self.i_type = i_type
        self.i_perm = i_perm

class Content:
    def __init__(self,b_name,b_inodo):
        self.b_name = b_name
        self.b_inodo = b_inodo

class FolderBlock:
    def __init__(self,b_content):
        self.b_content = b_content

class FileBlock:
    def __init__(self,b_content):
        self.b_content = b_content

class PointerBlock:
    def __init__(self,b_pointers):
        self.b_pointers = b_pointers

class Journaling:
    def __init__(self,journaling_type,journaling_operation,journaling_content,journaling_date):
        self.journaling_type = journaling_type
        self.journaling_operation = journaling_operation
        self.journaling_content = journaling_content
        self.journaling_date = journaling_date
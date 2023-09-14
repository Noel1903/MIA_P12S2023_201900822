from commands.mount import mount
from structs.struct import SuperBlock
from structs.struct import Journaling
import pickle
import struct,math,datetime
class mkfs:

    def __init__(self, params):
        self.params = params
        self.id = ""
        self.type = ""
        self.fs = "2fs"
        self.execute()

    def execute(self):
        for param in self.params:
            if param[0] == 'id':
                self.id = param[1]
            elif param[0] == 'type':
                self.type = param[1]
            elif param[0] == "fs":
                self.fs = param[1]
        self.type = self.type.lower()
        self.fs = self.fs.lower()
        if self.id != "":
            self.createFileSystem()
        else:
            print("No ha ingresado el id de la particion")
            return
        
    def createFileSystem(self):
        if self.fs =="2fs":
            self.createFileSystem2fs()
        elif self.fs == "3fs":
            self.createFileSystem3fs()
        else:
            print("Tipo de particion no valida")
            return
        

    def getIndexBock(self,bitmap_block):
        bitmap_block = bitmap_block.decode('utf-8')
        for i in range(len(bitmap_block)):
            if bitmap_block[i] == '0':
                return i+1
        return -1
    
    def getIndexInode(self,bitmap_inode):
        bitmap_inode = bitmap_inode.decode('utf-8')
        for i in range(len(bitmap_inode)):
            if bitmap_inode[i] == '0':
                return i+1
        return -1
        
        
    def createFileSystem2fs(self):
        print("Creando sistema de archivos 2fs")
        format_mbr = "I I I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
        format_ebr = "I I I c c c c I I 16s c c c I I 16s c c c I I 16s"
        format_sb = "I I I I I I I I I I I I I I I I I"
        format_i = "I I I I I I 16i c I"
        format_b_folder = "12s i"
        format_b = "64s"
        part_m = 0
        exist = False
        m = mount(None)
        for i in m.partitions_mounted:
            if i.part_id.rstrip("\x00") == self.id:
                part_m = i
                exist = True
                break
        if not exist:
            print("No se encontro la particion")
            return
        
        path_mount = part_m.path

        if self.type == "full":
            with open(path_mount,"rb+") as f:
                f.seek(0)
                data_bytes = f.read(struct.calcsize(format_mbr))
                mbr_unpack = struct.unpack(format_mbr,data_bytes)
                partition1 = mbr_unpack[4:10]
                partition2 = mbr_unpack[10:16]
                partition3 = mbr_unpack[16:22]
                partition4 = mbr_unpack[22:28]
              


                if partition1[5].decode('utf-8').rstrip("\x00")==part_m.name_partition:
                    #Se hacen los calculos para el super bloque
                    n = (partition1[4] - struct.calcsize(format_sb))/(4 + struct.calcsize(format_i) + 3 * struct.calcsize(format_b))
                    struct_n = math.floor(n)
                    bitmap_inodes = struct_n
                    bitmap_blocks = struct_n * 3
                    size_bitmap_inodes = bitmap_inodes * struct.calcsize(format_i)
                    size_bitmap_blocks = bitmap_blocks * struct.calcsize(format_b)
                    file_sistem = 2
                    inodes_count = bitmap_inodes
                    blocks_count = bitmap_blocks
                    free_blocks_count = bitmap_blocks - 1
                    free_inodes_count = bitmap_inodes - 1
                    mtime = 0
                    umtime = 0
                    mnt_count = 0
                    magic = 0xEF53
                    inode_size = struct.calcsize(format_i)
                    block_size = struct.calcsize(format_b)
                    first_ino = 0
                    first_blo = 0
                    bm_inode_start = partition1[3] + struct.calcsize(format_sb)
                    bm_block_start = bm_inode_start + bitmap_inodes
                    inode_start = bm_block_start + bitmap_blocks
                    block_start = inode_start + bitmap_inodes * inode_size
                    #se le asigna al superbloque todo lo que se calculó
                    sb = SuperBlock(file_sistem,inodes_count,blocks_count,free_blocks_count,free_inodes_count,mtime,umtime,mnt_count,magic,inode_size,block_size,first_ino,first_blo,bm_inode_start,bm_block_start,inode_start,block_start)
                    sb_bytes = struct.pack(format_sb,sb.s_filesystem_type,sb.s_inodes_count,sb.s_blocks_count,sb.s_free_blocks_count,sb.s_free_inodes_count,sb.s_mtime,
                                           sb.s_umtime,sb.s_mnt_count,sb.s_magic,sb.s_inode_s,sb.s_block_s,sb.s_first_ino,sb.s_first_blo,sb.s_bm_inode_start,sb.s_bm_block_start,
                                           sb.s_inode_start,sb.s_block_start)
                    f.seek(partition1[3])
                    #Se escribe el superbloque
                    f.write(sb_bytes)
                    #Se escriben los bitmap de inodos y bloques
                    f.seek(bm_inode_start)
                    for i in range(bitmap_inodes):
                        f.write(b'0')
                    f.seek(bm_block_start)
                    for i in range(bitmap_blocks):
                        f.write(b'0')
                    #Se escriben los inodos
                    f.seek(inode_start)
                    iblock = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
                    for i in range(bitmap_inodes):
                        inode = struct.pack(format_i,0,0,0,0,0,0,*iblock,'0'.encode('utf-8'),0)
                        f.write(inode)
                        f.seek(inode_start + (i+1) * inode_size)
                    #Se escriben los bloques
                    f.seek(block_start)
                    for i in range(bitmap_blocks):
                        block = struct.pack(format_b,b'')
                        f.write(block)
                        f.seek(block_start + (i+1) * block_size)

                    #Creacion de la carpeta raiz
                    f.seek(bm_block_start)
                    index_b = self.getIndexBock(f.read(blocks_count))
                    print(index_b)
                    f.seek(inode_start)
                    inode_root = f.read(inode_size)
                    inode_root_unpack = struct.unpack(format_i,inode_root)
                    inode_root_unpack = list(inode_root_unpack)
                    inode_root_unpack[0] = 1
                    inode_root_unpack[1] = 1
                    inode_root_unpack[2] = 27
                    inode_root_unpack[3] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[4] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[5] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[6] = index_b
                    inode_root_unpack[22] = '0'.encode('utf-8')
                    inode_root_unpack[23] = 777
                    f.seek(bm_inode_start)
                    f.seek(inode_start+((self.getIndexInode(f.read(inodes_count))-1)*inode_size))
                    f.write(struct.pack(format_i,inode_root_unpack[0],inode_root_unpack[1],inode_root_unpack[2],inode_root_unpack[3],inode_root_unpack[4],
                                        inode_root_unpack[5],inode_root_unpack[6],inode_root_unpack[7],inode_root_unpack[8],inode_root_unpack[9],inode_root_unpack[10],
                                        inode_root_unpack[11],inode_root_unpack[12],inode_root_unpack[13],inode_root_unpack[14],inode_root_unpack[15],inode_root_unpack[16],
                                        inode_root_unpack[17],inode_root_unpack[18],inode_root_unpack[19],inode_root_unpack[20],inode_root_unpack[21],inode_root_unpack[22],inode_root_unpack[23]))
                    #se setea 1 en el bitmap de inodos
                    f.seek(bm_inode_start)
                    f.write(b'1')
                    #se setea 1 en el bitmap de bloques
                    f.seek(bm_block_start)
                    f.write(b'1')
                    #se crea el bloque de la carpeta raiz
                    count = 0
                    f.seek(bm_inode_start)
                    count = self.getIndexInode(f.read(inodes_count))
                    f.seek(block_start)
                    block_root = struct.pack('12s i 12s i 12s i 12s i',
                                        '.'.encode ('utf-8'),0,
                                        '..'.encode ('utf-8'),0,
                                        'users.txt'.encode ('utf-8'),count,
                                        ''.encode ('utf-8'),-1)
                    f.write(block_root)
                    #se crea el inodo del archivo users.txt
                    f.seek(bm_block_start)
                    index_b = self.getIndexBock(f.read(blocks_count))
                    f.seek(bm_inode_start)
                    f.seek(inode_start+(self.getIndexInode(f.read(inodes_count))*inode_size))
                    inode_users = f.read(inode_size)
                    inode_users_unpack = struct.unpack(format_i,inode_users)
                    inode_users_unpack = list(inode_users_unpack)
                    inode_users_unpack[0] = 1
                    inode_users_unpack[1] = 1
                    inode_users_unpack[2] = 27
                    inode_users_unpack[3] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[4] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[5] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[6] = index_b
                    inode_users_unpack[22] = '1'.encode('utf-8')
                    inode_users_unpack[23] = 777
                    f.seek(bm_inode_start)
                    f.seek(inode_start+((self.getIndexInode(f.read(inodes_count))-1)*inode_size))
                    f.write(struct.pack(format_i,inode_users_unpack[0],inode_users_unpack[1],inode_users_unpack[2],inode_users_unpack[3],inode_users_unpack[4],inode_users_unpack[5],inode_users_unpack[6],inode_users_unpack[7],inode_users_unpack[8],inode_users_unpack[9],inode_users_unpack[10],inode_users_unpack[11],inode_users_unpack[12],inode_users_unpack[13],inode_users_unpack[14],inode_users_unpack[15],inode_users_unpack[16],inode_users_unpack[17],inode_users_unpack[18],inode_users_unpack[19],inode_users_unpack[20],inode_users_unpack[21],inode_users_unpack[22],inode_users_unpack[23]))
                    #se setea 1 en el bitmap de inodos
                    f.seek(bm_inode_start)
                    f.seek(bm_inode_start+self.getIndexInode(f.read(inodes_count))-1)
                    f.write(b'1')
                    #se crea el bloque del archivo users.txt
                    f.seek(bm_block_start)
                    f.seek(block_start+((self.getIndexBock(f.read(blocks_count))-1)*block_size))
                    block_user_pack = struct.pack(format_b,'1,G,root\n1,U,root,root,123\n'.encode('utf-8'))
                    f.write(block_user_pack)
                    #se setea 1 en el bitmap de bloques
                    f.seek(bm_block_start)
                    f.seek(bm_block_start+self.getIndexBock(f.read(blocks_count))-1)
                    f.write(b'1')
                    
                    print("Sistema de archivos creado correctamente")
                elif partition2[5].decode('utf-8').rstrip("\x00")==part_m.name_partition:
                    #Se hacen los calculos para el super bloque
                    n = (partition2[4] - struct.calcsize(format_sb))/(4 + struct.calcsize(format_i) + 3 * struct.calcsize(format_b))
                    struct_n = math.floor(n)
                    bitmap_inodes = struct_n
                    bitmap_blocks = struct_n * 3
                    size_bitmap_inodes = bitmap_inodes * struct.calcsize(format_i)
                    size_bitmap_blocks = bitmap_blocks * struct.calcsize(format_b)
                    file_sistem = 2
                    inodes_count = bitmap_inodes
                    blocks_count = bitmap_blocks
                    free_blocks_count = bitmap_blocks - 1
                    free_inodes_count = bitmap_inodes - 1
                    mtime = 0
                    umtime = 0
                    mnt_count = 0
                    magic = 0xEF53
                    inode_size = struct.calcsize(format_i)
                    block_size = struct.calcsize(format_b)
                    first_ino = 0
                    first_blo = 0
                    bm_inode_start = partition2[3] + struct.calcsize(format_sb)
                    bm_block_start = bm_inode_start + bitmap_inodes
                    inode_start = bm_block_start + bitmap_blocks
                    block_start = inode_start + bitmap_inodes * inode_size
                    #se le asigna al superbloque todo lo que se calculó
                    sb = SuperBlock(file_sistem,inodes_count,blocks_count,free_blocks_count,free_inodes_count,mtime,umtime,mnt_count,magic,inode_size,block_size,first_ino,first_blo,bm_inode_start,bm_block_start,inode_start,block_start)
                    sb_bytes = struct.pack(format_sb,sb.s_filesystem_type,sb.s_inodes_count,sb.s_blocks_count,sb.s_free_blocks_count,sb.s_free_inodes_count,sb.s_mtime,
                                           sb.s_umtime,sb.s_mnt_count,sb.s_magic,sb.s_inode_s,sb.s_block_s,sb.s_first_ino,sb.s_first_blo,sb.s_bm_inode_start,sb.s_bm_block_start,
                                           sb.s_inode_start,sb.s_block_start)
                    f.seek(partition2[3])
                    #Se escribe el superbloque
                    f.write(sb_bytes)
                    #Se escriben los bitmap de inodos y bloques
                    f.seek(bm_inode_start)
                    for i in range(bitmap_inodes):
                        f.write(b'0')
                    f.seek(bm_block_start)
                    for i in range(bitmap_blocks):
                        f.write(b'0')
                    #Se escriben los inodos
                    f.seek(inode_start)
                    iblock = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
                    for i in range(bitmap_inodes):
                        inode = struct.pack(format_i,0,0,0,0,0,0,*iblock,'0'.encode('utf-8'),0)
                        f.write(inode)
                        f.seek(inode_start + (i+1) * inode_size)
                    #Se escriben los bloques
                    f.seek(block_start)
                    for i in range(bitmap_blocks):
                        block = struct.pack(format_b,b'')
                        f.write(block)
                        f.seek(block_start + (i+1) * block_size)

                    #Creacion de la carpeta raiz
                    f.seek(bm_block_start)
                    index_b = self.getIndexBock(f.read(blocks_count))
                    print(index_b)
                    f.seek(inode_start)
                    inode_root = f.read(inode_size)
                    inode_root_unpack = struct.unpack(format_i,inode_root)
                    inode_root_unpack = list(inode_root_unpack)
                    inode_root_unpack[0] = 1
                    inode_root_unpack[1] = 1
                    inode_root_unpack[2] = 27
                    inode_root_unpack[3] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[4] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[5] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[6] = index_b
                    inode_root_unpack[22] = '0'.encode('utf-8')
                    inode_root_unpack[23] = 777
                    f.seek(bm_inode_start)
                    f.seek(inode_start+((self.getIndexInode(f.read(inodes_count))-1)*inode_size))
                    f.write(struct.pack(format_i,inode_root_unpack[0],inode_root_unpack[1],inode_root_unpack[2],inode_root_unpack[3],inode_root_unpack[4],
                                        inode_root_unpack[5],inode_root_unpack[6],inode_root_unpack[7],inode_root_unpack[8],inode_root_unpack[9],inode_root_unpack[10],
                                        inode_root_unpack[11],inode_root_unpack[12],inode_root_unpack[13],inode_root_unpack[14],inode_root_unpack[15],inode_root_unpack[16],
                                        inode_root_unpack[17],inode_root_unpack[18],inode_root_unpack[19],inode_root_unpack[20],inode_root_unpack[21],inode_root_unpack[22],inode_root_unpack[23]))
                    #se setea 1 en el bitmap de inodos
                    f.seek(bm_inode_start)
                    f.write(b'1')
                    #se setea 1 en el bitmap de bloques
                    f.seek(bm_block_start)
                    f.write(b'1')
                    #se crea el bloque de la carpeta raiz
                    count = 0
                    f.seek(bm_inode_start)
                    count = self.getIndexInode(f.read(inodes_count))
                    f.seek(block_start)
                    block_root = struct.pack('12s i 12s i 12s i 12s i',
                                        '.'.encode ('utf-8'),0,
                                        '..'.encode ('utf-8'),0,
                                        'users.txt'.encode ('utf-8'),count,
                                        ''.encode ('utf-8'),-1)
                    f.write(block_root)
                    #se crea el inodo del archivo users.txt
                    f.seek(bm_block_start)
                    index_b = self.getIndexBock(f.read(blocks_count))
                    f.seek(bm_inode_start)
                    f.seek(inode_start+(self.getIndexInode(f.read(inodes_count))*inode_size))
                    inode_users = f.read(inode_size)
                    inode_users_unpack = struct.unpack(format_i,inode_users)
                    inode_users_unpack = list(inode_users_unpack)
                    inode_users_unpack[0] = 1
                    inode_users_unpack[1] = 1
                    inode_users_unpack[2] = 27
                    inode_users_unpack[3] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[4] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[5] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[6] = index_b
                    inode_users_unpack[22] = '1'.encode('utf-8')
                    inode_users_unpack[23] = 777
                    f.seek(bm_inode_start)
                    f.seek(inode_start+((self.getIndexInode(f.read(inodes_count))-1)*inode_size))
                    f.write(struct.pack(format_i,inode_users_unpack[0],inode_users_unpack[1],inode_users_unpack[2],inode_users_unpack[3],inode_users_unpack[4],inode_users_unpack[5],inode_users_unpack[6],inode_users_unpack[7],inode_users_unpack[8],inode_users_unpack[9],inode_users_unpack[10],inode_users_unpack[11],inode_users_unpack[12],inode_users_unpack[13],inode_users_unpack[14],inode_users_unpack[15],inode_users_unpack[16],inode_users_unpack[17],inode_users_unpack[18],inode_users_unpack[19],inode_users_unpack[20],inode_users_unpack[21],inode_users_unpack[22],inode_users_unpack[23]))
                    #se setea 1 en el bitmap de inodos
                    f.seek(bm_inode_start)
                    f.seek(bm_inode_start+self.getIndexInode(f.read(inodes_count))-1)
                    f.write(b'1')
                    #se crea el bloque del archivo users.txt
                    f.seek(bm_block_start)
                    f.seek(block_start+((self.getIndexBock(f.read(blocks_count))-1)*block_size))
                    block_user_pack = struct.pack(format_b,'1,G,root\n1,U,root,root,123\n'.encode('utf-8'))
                    f.write(block_user_pack)
                    #se setea 1 en el bitmap de bloques
                    f.seek(bm_block_start)
                    f.seek(bm_block_start+self.getIndexBock(f.read(blocks_count))-1)
                    f.write(b'1')
                    
                    print("Sistema de archivos creado correctamente")
                elif partition3[5].decode('utf-8').rstrip("\x00")==part_m.name_partition:
                    #Se hacen los calculos para el super bloque
                    n = (partition3[4] - struct.calcsize(format_sb))/(4 + struct.calcsize(format_i) + 3 * struct.calcsize(format_b))
                    struct_n = math.floor(n)
                    bitmap_inodes = struct_n
                    bitmap_blocks = struct_n * 3
                    size_bitmap_inodes = bitmap_inodes * struct.calcsize(format_i)
                    size_bitmap_blocks = bitmap_blocks * struct.calcsize(format_b)
                    file_sistem = 2
                    inodes_count = bitmap_inodes
                    blocks_count = bitmap_blocks
                    free_blocks_count = bitmap_blocks - 1
                    free_inodes_count = bitmap_inodes - 1
                    mtime = 0
                    umtime = 0
                    mnt_count = 0
                    magic = 0xEF53
                    inode_size = struct.calcsize(format_i)
                    block_size = struct.calcsize(format_b)
                    first_ino = 0
                    first_blo = 0
                    bm_inode_start = partition3[3] + struct.calcsize(format_sb)
                    bm_block_start = bm_inode_start + bitmap_inodes
                    inode_start = bm_block_start + bitmap_blocks
                    block_start = inode_start + bitmap_inodes * inode_size
                    #se le asigna al superbloque todo lo que se calculó
                    sb = SuperBlock(file_sistem,inodes_count,blocks_count,free_blocks_count,free_inodes_count,mtime,umtime,mnt_count,magic,inode_size,block_size,first_ino,first_blo,bm_inode_start,bm_block_start,inode_start,block_start)
                    sb_bytes = struct.pack(format_sb,sb.s_filesystem_type,sb.s_inodes_count,sb.s_blocks_count,sb.s_free_blocks_count,sb.s_free_inodes_count,sb.s_mtime,
                                           sb.s_umtime,sb.s_mnt_count,sb.s_magic,sb.s_inode_s,sb.s_block_s,sb.s_first_ino,sb.s_first_blo,sb.s_bm_inode_start,sb.s_bm_block_start,
                                           sb.s_inode_start,sb.s_block_start)
                    f.seek(partition3[3])
                    #Se escribe el superbloque
                    f.write(sb_bytes)
                    #Se escriben los bitmap de inodos y bloques
                    f.seek(bm_inode_start)
                    for i in range(bitmap_inodes):
                        f.write(b'0')
                    f.seek(bm_block_start)
                    for i in range(bitmap_blocks):
                        f.write(b'0')
                    #Se escriben los inodos
                    f.seek(inode_start)
                    iblock = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
                    for i in range(bitmap_inodes):
                        inode = struct.pack(format_i,0,0,0,0,0,0,*iblock,'0'.encode('utf-8'),0)
                        f.write(inode)
                        f.seek(inode_start + (i+1) * inode_size)
                    #Se escriben los bloques
                    f.seek(block_start)
                    for i in range(bitmap_blocks):
                        block = struct.pack(format_b,b'')
                        f.write(block)
                        f.seek(block_start + (i+1) * block_size)

                    #Creacion de la carpeta raiz
                    f.seek(bm_block_start)
                    index_b = self.getIndexBock(f.read(blocks_count))
                    print(index_b)
                    f.seek(inode_start)
                    inode_root = f.read(inode_size)
                    inode_root_unpack = struct.unpack(format_i,inode_root)
                    inode_root_unpack = list(inode_root_unpack)
                    inode_root_unpack[0] = 1
                    inode_root_unpack[1] = 1
                    inode_root_unpack[2] = 27
                    inode_root_unpack[3] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[4] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[5] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[6] = index_b
                    inode_root_unpack[22] = '0'.encode('utf-8')
                    inode_root_unpack[23] = 777
                    f.seek(bm_inode_start)
                    f.seek(inode_start+((self.getIndexInode(f.read(inodes_count))-1)*inode_size))
                    f.write(struct.pack(format_i,inode_root_unpack[0],inode_root_unpack[1],inode_root_unpack[2],inode_root_unpack[3],inode_root_unpack[4],
                                        inode_root_unpack[5],inode_root_unpack[6],inode_root_unpack[7],inode_root_unpack[8],inode_root_unpack[9],inode_root_unpack[10],
                                        inode_root_unpack[11],inode_root_unpack[12],inode_root_unpack[13],inode_root_unpack[14],inode_root_unpack[15],inode_root_unpack[16],
                                        inode_root_unpack[17],inode_root_unpack[18],inode_root_unpack[19],inode_root_unpack[20],inode_root_unpack[21],inode_root_unpack[22],inode_root_unpack[23]))
                    #se setea 1 en el bitmap de inodos
                    f.seek(bm_inode_start)
                    f.write(b'1')
                    #se setea 1 en el bitmap de bloques
                    f.seek(bm_block_start)
                    f.write(b'1')
                    #se crea el bloque de la carpeta raiz
                    count = 0
                    f.seek(bm_inode_start)
                    count = self.getIndexInode(f.read(inodes_count))
                    f.seek(block_start)
                    block_root = struct.pack('12s i 12s i 12s i 12s i',
                                        '.'.encode ('utf-8'),0,
                                        '..'.encode ('utf-8'),0,
                                        'users.txt'.encode ('utf-8'),count,
                                        ''.encode ('utf-8'),-1)
                    f.write(block_root)
                    #se crea el inodo del archivo users.txt
                    f.seek(bm_block_start)
                    index_b = self.getIndexBock(f.read(blocks_count))
                    f.seek(bm_inode_start)
                    f.seek(inode_start+(self.getIndexInode(f.read(inodes_count))*inode_size))
                    inode_users = f.read(inode_size)
                    inode_users_unpack = struct.unpack(format_i,inode_users)
                    inode_users_unpack = list(inode_users_unpack)
                    inode_users_unpack[0] = 1
                    inode_users_unpack[1] = 1
                    inode_users_unpack[2] = 27
                    inode_users_unpack[3] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[4] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[5] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[6] = index_b
                    inode_users_unpack[22] = '1'.encode('utf-8')
                    inode_users_unpack[23] = 777
                    f.seek(bm_inode_start)
                    f.seek(inode_start+((self.getIndexInode(f.read(inodes_count))-1)*inode_size))
                    f.write(struct.pack(format_i,inode_users_unpack[0],inode_users_unpack[1],inode_users_unpack[2],inode_users_unpack[3],inode_users_unpack[4],inode_users_unpack[5],inode_users_unpack[6],inode_users_unpack[7],inode_users_unpack[8],inode_users_unpack[9],inode_users_unpack[10],inode_users_unpack[11],inode_users_unpack[12],inode_users_unpack[13],inode_users_unpack[14],inode_users_unpack[15],inode_users_unpack[16],inode_users_unpack[17],inode_users_unpack[18],inode_users_unpack[19],inode_users_unpack[20],inode_users_unpack[21],inode_users_unpack[22],inode_users_unpack[23]))
                    #se setea 1 en el bitmap de inodos
                    f.seek(bm_inode_start)
                    f.seek(bm_inode_start+self.getIndexInode(f.read(inodes_count))-1)
                    f.write(b'1')
                    #se crea el bloque del archivo users.txt
                    f.seek(bm_block_start)
                    f.seek(block_start+((self.getIndexBock(f.read(blocks_count))-1)*block_size))
                    block_user_pack = struct.pack(format_b,'1,G,root\n1,U,root,root,123\n'.encode('utf-8'))
                    f.write(block_user_pack)
                    #se setea 1 en el bitmap de bloques
                    f.seek(bm_block_start)
                    f.seek(bm_block_start+self.getIndexBock(f.read(blocks_count))-1)
                    f.write(b'1')
                    
                    print("Sistema de archivos creado correctamente")
                elif partition4[5].decode('utf-8').rstrip("\x00")==part_m.name_partition:
                    #Se hacen los calculos para el super bloque
                    n = (partition4[4] - struct.calcsize(format_sb))/(4 + struct.calcsize(format_i) + 3 * struct.calcsize(format_b))
                    struct_n = math.floor(n)
                    bitmap_inodes = struct_n
                    bitmap_blocks = struct_n * 3
                    size_bitmap_inodes = bitmap_inodes * struct.calcsize(format_i)
                    size_bitmap_blocks = bitmap_blocks * struct.calcsize(format_b)
                    file_sistem = 2
                    inodes_count = bitmap_inodes
                    blocks_count = bitmap_blocks
                    free_blocks_count = bitmap_blocks - 1
                    free_inodes_count = bitmap_inodes - 1
                    mtime = 0
                    umtime = 0
                    mnt_count = 0
                    magic = 0xEF53
                    inode_size = struct.calcsize(format_i)
                    block_size = struct.calcsize(format_b)
                    first_ino = 0
                    first_blo = 0
                    bm_inode_start = partition4[3] + struct.calcsize(format_sb)
                    bm_block_start = bm_inode_start + bitmap_inodes
                    inode_start = bm_block_start + bitmap_blocks
                    block_start = inode_start + bitmap_inodes * inode_size
                    #se le asigna al superbloque todo lo que se calculó
                    sb = SuperBlock(file_sistem,inodes_count,blocks_count,free_blocks_count,free_inodes_count,mtime,umtime,mnt_count,magic,inode_size,block_size,first_ino,first_blo,bm_inode_start,bm_block_start,inode_start,block_start)
                    sb_bytes = struct.pack(format_sb,sb.s_filesystem_type,sb.s_inodes_count,sb.s_blocks_count,sb.s_free_blocks_count,sb.s_free_inodes_count,sb.s_mtime,
                                           sb.s_umtime,sb.s_mnt_count,sb.s_magic,sb.s_inode_s,sb.s_block_s,sb.s_first_ino,sb.s_first_blo,sb.s_bm_inode_start,sb.s_bm_block_start,
                                           sb.s_inode_start,sb.s_block_start)
                    f.seek(partition4[3])
                    #Se escribe el superbloque
                    f.write(sb_bytes)
                    #Se escriben los bitmap de inodos y bloques
                    f.seek(bm_inode_start)
                    for i in range(bitmap_inodes):
                        f.write(b'0')
                    f.seek(bm_block_start)
                    for i in range(bitmap_blocks):
                        f.write(b'0')
                    #Se escriben los inodos
                    f.seek(inode_start)
                    iblock = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
                    for i in range(bitmap_inodes):
                        inode = struct.pack(format_i,0,0,0,0,0,0,*iblock,'0'.encode('utf-8'),0)
                        f.write(inode)
                        f.seek(inode_start + (i+1) * inode_size)
                    #Se escriben los bloques
                    f.seek(block_start)
                    for i in range(bitmap_blocks):
                        block = struct.pack(format_b,b'')
                        f.write(block)
                        f.seek(block_start + (i+1) * block_size)

                    #Creacion de la carpeta raiz
                    f.seek(bm_block_start)
                    index_b = self.getIndexBock(f.read(blocks_count))
                    print(index_b)
                    f.seek(inode_start)
                    inode_root = f.read(inode_size)
                    inode_root_unpack = struct.unpack(format_i,inode_root)
                    inode_root_unpack = list(inode_root_unpack)
                    inode_root_unpack[0] = 1
                    inode_root_unpack[1] = 1
                    inode_root_unpack[2] = 27
                    inode_root_unpack[3] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[4] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[5] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[6] = index_b
                    inode_root_unpack[22] = '0'.encode('utf-8')
                    inode_root_unpack[23] = 777
                    f.seek(bm_inode_start)
                    f.seek(inode_start+((self.getIndexInode(f.read(inodes_count))-1)*inode_size))
                    f.write(struct.pack(format_i,inode_root_unpack[0],inode_root_unpack[1],inode_root_unpack[2],inode_root_unpack[3],inode_root_unpack[4],
                                        inode_root_unpack[5],inode_root_unpack[6],inode_root_unpack[7],inode_root_unpack[8],inode_root_unpack[9],inode_root_unpack[10],
                                        inode_root_unpack[11],inode_root_unpack[12],inode_root_unpack[13],inode_root_unpack[14],inode_root_unpack[15],inode_root_unpack[16],
                                        inode_root_unpack[17],inode_root_unpack[18],inode_root_unpack[19],inode_root_unpack[20],inode_root_unpack[21],inode_root_unpack[22],inode_root_unpack[23]))
                    #se setea 1 en el bitmap de inodos
                    f.seek(bm_inode_start)
                    f.write(b'1')
                    #se setea 1 en el bitmap de bloques
                    f.seek(bm_block_start)
                    f.write(b'1')
                    #se crea el bloque de la carpeta raiz
                    count = 0
                    f.seek(bm_inode_start)
                    count = self.getIndexInode(f.read(inodes_count))
                    f.seek(block_start)
                    block_root = struct.pack('12s i 12s i 12s i 12s i',
                                        '.'.encode ('utf-8'),0,
                                        '..'.encode ('utf-8'),0,
                                        'users.txt'.encode ('utf-8'),count,
                                        ''.encode ('utf-8'),-1)
                    f.write(block_root)
                    #se crea el inodo del archivo users.txt
                    f.seek(bm_block_start)
                    index_b = self.getIndexBock(f.read(blocks_count))
                    f.seek(bm_inode_start)
                    f.seek(inode_start+(self.getIndexInode(f.read(inodes_count))*inode_size))
                    inode_users = f.read(inode_size)
                    inode_users_unpack = struct.unpack(format_i,inode_users)
                    inode_users_unpack = list(inode_users_unpack)
                    inode_users_unpack[0] = 1
                    inode_users_unpack[1] = 1
                    inode_users_unpack[2] = 27
                    inode_users_unpack[3] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[4] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[5] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[6] = index_b
                    inode_users_unpack[22] = '1'.encode('utf-8')
                    inode_users_unpack[23] = 777
                    f.seek(bm_inode_start)
                    f.seek(inode_start+((self.getIndexInode(f.read(inodes_count))-1)*inode_size))
                    f.write(struct.pack(format_i,inode_users_unpack[0],inode_users_unpack[1],inode_users_unpack[2],inode_users_unpack[3],inode_users_unpack[4],inode_users_unpack[5],inode_users_unpack[6],inode_users_unpack[7],inode_users_unpack[8],inode_users_unpack[9],inode_users_unpack[10],inode_users_unpack[11],inode_users_unpack[12],inode_users_unpack[13],inode_users_unpack[14],inode_users_unpack[15],inode_users_unpack[16],inode_users_unpack[17],inode_users_unpack[18],inode_users_unpack[19],inode_users_unpack[20],inode_users_unpack[21],inode_users_unpack[22],inode_users_unpack[23]))
                    #se setea 1 en el bitmap de inodos
                    f.seek(bm_inode_start)
                    f.seek(bm_inode_start+self.getIndexInode(f.read(inodes_count))-1)
                    f.write(b'1')
                    #se crea el bloque del archivo users.txt
                    f.seek(bm_block_start)
                    f.seek(block_start+((self.getIndexBock(f.read(blocks_count))-1)*block_size))
                    block_user_pack = struct.pack(format_b,'1,G,root\n1,U,root,root,123\n'.encode('utf-8'))
                    f.write(block_user_pack)
                    #se setea 1 en el bitmap de bloques
                    f.seek(bm_block_start)
                    f.seek(bm_block_start+self.getIndexBock(f.read(blocks_count))-1)
                    f.write(b'1')
                    
                    print("Sistema de archivos creado correctamente")
                else:
                    print("No se encontro la particion")
                    return

                f.close()
                return

    def createFileSystem3fs(self):
        print("Creando sistema de archivos 3fs")
        format_mbr = "I I I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
        format_ebr = "I I I c c c c I I 16s c c c I I 16s c c c I I 16s"
        format_sb = "I I I I I I I I I I I I I I I I I"
        format_i = "I I I I I I 16i c I"
        format_b_folder = "12s i"
        format_b = "64s"
        part_m = 0
        exist = False
        m = mount(None)
        for i in m.partitions_mounted:
            if i.part_id.rstrip("\x00") == self.id:
                part_m = i
                exist = True
                break
        if not exist:
            print("No se encontro la particion")
            return
        
        path_mount = part_m.path

        if self.type == "full":
            with open(path_mount,"rb+") as f:
                f.seek(0)
                data_bytes = f.read(struct.calcsize(format_mbr))
                mbr_unpack = struct.unpack(format_mbr,data_bytes)
                partition1 = mbr_unpack[4:10]
                partition2 = mbr_unpack[10:16]
                partition3 = mbr_unpack[16:22]
                partition4 = mbr_unpack[22:28]
              


                if partition1[5].decode('utf-8').rstrip("\x00")==part_m.name_partition:
                    size_journaling  = partition1[4] * 0.010
                    size_journaling = math.floor(size_journaling)
                    n = (partition1[4] - struct.calcsize(format_sb))/(4 + struct.calcsize(format_i) + 3 * struct.calcsize(format_b) + size_journaling)
                    struct_n = math.floor(n)
                    bitmap_inodes = struct_n
                    bitmap_blocks = struct_n * 3
                    size_bitmap_inodes = bitmap_inodes * struct.calcsize(format_i)
                    size_bitmap_blocks = bitmap_blocks * struct.calcsize(format_b)
                    file_sistem = 3
                    inodes_count = bitmap_inodes
                    blocks_count = bitmap_blocks
                    free_blocks_count = bitmap_blocks - 1
                    free_inodes_count = bitmap_inodes - 1
                    mtime = 0
                    umtime = 0
                    mnt_count = 0
                    magic = 0xEF53
                    inode_size = struct.calcsize(format_i)
                    block_size = struct.calcsize(format_b)
                    first_ino = 0
                    first_blo = 0
                    bm_inode_start = partition1[3] + struct.calcsize(format_sb) + size_journaling
                    bm_block_start = bm_inode_start + bitmap_inodes
                    inode_start = bm_block_start + bitmap_blocks
                    block_start = inode_start + bitmap_inodes * inode_size
                    #se le asigna al superbloque todo lo que se calculó
                    sb = SuperBlock(file_sistem,inodes_count,blocks_count,free_blocks_count,free_inodes_count,mtime,umtime,mnt_count,magic,inode_size,block_size,first_ino,first_blo,bm_inode_start,bm_block_start,inode_start,block_start)
                    sb_bytes = struct.pack(format_sb,sb.s_filesystem_type,sb.s_inodes_count,sb.s_blocks_count,sb.s_free_blocks_count,sb.s_free_inodes_count,sb.s_mtime,
                                           sb.s_umtime,sb.s_mnt_count,sb.s_magic,sb.s_inode_s,sb.s_block_s,sb.s_first_ino,sb.s_first_blo,sb.s_bm_inode_start,sb.s_bm_block_start,
                                           sb.s_inode_start,sb.s_block_start)
                    f.seek(partition1[3])
                    #Se escribe el superbloque
                    f.write(sb_bytes)
                    #Se escriben los bitmap de inodos y bloques
                    f.seek(bm_inode_start)
                    for i in range(bitmap_inodes):
                        f.write(b'0')
                    f.seek(bm_block_start)
                    for i in range(bitmap_blocks):
                        f.write(b'0')
                    #Se escriben los inodos
                    f.seek(inode_start)
                    iblock = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
                    for i in range(bitmap_inodes):
                        inode = struct.pack(format_i,0,0,0,0,0,0,*iblock,'0'.encode('utf-8'),0)
                        f.write(inode)
                        f.seek(inode_start + (i+1) * inode_size)
                    #Se escriben los bloques
                    f.seek(block_start)
                    for i in range(bitmap_blocks):
                        block = struct.pack(format_b,b'')
                        f.write(block)
                        f.seek(block_start + (i+1) * block_size)

                    #Creacion de la carpeta raiz
                    f.seek(bm_block_start)
                    index_b = self.getIndexBock(f.read(blocks_count))
                    print(index_b)
                    f.seek(inode_start)
                    inode_root = f.read(inode_size)
                    inode_root_unpack = struct.unpack(format_i,inode_root)
                    inode_root_unpack = list(inode_root_unpack)
                    inode_root_unpack[0] = 1
                    inode_root_unpack[1] = 1
                    inode_root_unpack[2] = 27
                    inode_root_unpack[3] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[4] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[5] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[6] = index_b
                    inode_root_unpack[22] = '0'.encode('utf-8')
                    inode_root_unpack[23] = 777
                    f.seek(bm_inode_start)
                    f.seek(inode_start+((self.getIndexInode(f.read(inodes_count))-1)*inode_size))
                    f.write(struct.pack(format_i,inode_root_unpack[0],inode_root_unpack[1],inode_root_unpack[2],inode_root_unpack[3],inode_root_unpack[4],
                                        inode_root_unpack[5],inode_root_unpack[6],inode_root_unpack[7],inode_root_unpack[8],inode_root_unpack[9],inode_root_unpack[10],
                                        inode_root_unpack[11],inode_root_unpack[12],inode_root_unpack[13],inode_root_unpack[14],inode_root_unpack[15],inode_root_unpack[16],
                                        inode_root_unpack[17],inode_root_unpack[18],inode_root_unpack[19],inode_root_unpack[20],inode_root_unpack[21],inode_root_unpack[22],inode_root_unpack[23]))
                    #se setea 1 en el bitmap de inodos
                    f.seek(bm_inode_start)
                    f.write(b'1')
                    #se setea 1 en el bitmap de bloques
                    f.seek(bm_block_start)
                    f.write(b'1')
                    #se crea el bloque de la carpeta raiz
                    count = 0
                    f.seek(bm_inode_start)
                    count = self.getIndexInode(f.read(inodes_count))
                    f.seek(block_start)
                    block_root = struct.pack('12s i 12s i 12s i 12s i',
                                        '.'.encode ('utf-8'),0,
                                        '..'.encode ('utf-8'),0,
                                        'users.txt'.encode ('utf-8'),count,
                                        ''.encode ('utf-8'),-1)
                    f.write(block_root)
                    #se crea el inodo del archivo users.txt
                    f.seek(bm_block_start)
                    index_b = self.getIndexBock(f.read(blocks_count))
                    f.seek(bm_inode_start)
                    f.seek(inode_start+(self.getIndexInode(f.read(inodes_count))*inode_size))
                    inode_users = f.read(inode_size)
                    inode_users_unpack = struct.unpack(format_i,inode_users)
                    inode_users_unpack = list(inode_users_unpack)
                    inode_users_unpack[0] = 1
                    inode_users_unpack[1] = 1
                    inode_users_unpack[2] = 27
                    inode_users_unpack[3] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[4] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[5] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[6] = index_b
                    inode_users_unpack[22] = '1'.encode('utf-8')
                    inode_users_unpack[23] = 777
                    f.seek(bm_inode_start)
                    f.seek(inode_start+((self.getIndexInode(f.read(inodes_count))-1)*inode_size))
                    f.write(struct.pack(format_i,inode_users_unpack[0],inode_users_unpack[1],inode_users_unpack[2],inode_users_unpack[3],inode_users_unpack[4],inode_users_unpack[5],inode_users_unpack[6],inode_users_unpack[7],inode_users_unpack[8],inode_users_unpack[9],inode_users_unpack[10],inode_users_unpack[11],inode_users_unpack[12],inode_users_unpack[13],inode_users_unpack[14],inode_users_unpack[15],inode_users_unpack[16],inode_users_unpack[17],inode_users_unpack[18],inode_users_unpack[19],inode_users_unpack[20],inode_users_unpack[21],inode_users_unpack[22],inode_users_unpack[23]))
                    #se setea 1 en el bitmap de inodos
                    f.seek(bm_inode_start)
                    f.seek(bm_inode_start+self.getIndexInode(f.read(inodes_count))-1)
                    f.write(b'1')
                    #se crea el bloque del archivo users.txt
                    f.seek(bm_block_start)
                    f.seek(block_start+((self.getIndexBock(f.read(blocks_count))-1)*block_size))
                    block_user_pack = struct.pack(format_b,'1,G,root\n1,U,root,root,123\n'.encode('utf-8'))
                    f.write(block_user_pack)
                    #se setea 1 en el bitmap de bloques
                    f.seek(bm_block_start)
                    f.seek(bm_block_start+self.getIndexBock(f.read(blocks_count))-1)
                    f.write(b'1')
                    
                    

                    print("Sistema de archivos creado correctamente")
                elif partition2[5].decode('utf-8').rstrip("\x00")==part_m.name_partition:
                    size_journaling  = partition2[4] * 0.010
                    size_journaling = math.floor(size_journaling)
                    n = (partition2[4] - struct.calcsize(format_sb))/(4 + struct.calcsize(format_i) + 3 * struct.calcsize(format_b) + size_journaling)
                    struct_n = math.floor(n)
                    bitmap_inodes = struct_n
                    bitmap_blocks = struct_n * 3
                    size_bitmap_inodes = bitmap_inodes * struct.calcsize(format_i)
                    size_bitmap_blocks = bitmap_blocks * struct.calcsize(format_b)
                    file_sistem = 3
                    inodes_count = bitmap_inodes
                    blocks_count = bitmap_blocks
                    free_blocks_count = bitmap_blocks - 1
                    free_inodes_count = bitmap_inodes - 1
                    mtime = 0
                    umtime = 0
                    mnt_count = 0
                    magic = 0xEF53
                    inode_size = struct.calcsize(format_i)
                    block_size = struct.calcsize(format_b)
                    first_ino = 0
                    first_blo = 0
                    bm_inode_start = partition2[3] + struct.calcsize(format_sb) + size_journaling
                    bm_block_start = bm_inode_start + bitmap_inodes
                    inode_start = bm_block_start + bitmap_blocks
                    block_start = inode_start + bitmap_inodes * inode_size
                    #se le asigna al superbloque todo lo que se calculó
                    sb = SuperBlock(file_sistem,inodes_count,blocks_count,free_blocks_count,free_inodes_count,mtime,umtime,mnt_count,magic,inode_size,block_size,first_ino,first_blo,bm_inode_start,bm_block_start,inode_start,block_start)
                    sb_bytes = struct.pack(format_sb,sb.s_filesystem_type,sb.s_inodes_count,sb.s_blocks_count,sb.s_free_blocks_count,sb.s_free_inodes_count,sb.s_mtime,
                                           sb.s_umtime,sb.s_mnt_count,sb.s_magic,sb.s_inode_s,sb.s_block_s,sb.s_first_ino,sb.s_first_blo,sb.s_bm_inode_start,sb.s_bm_block_start,
                                           sb.s_inode_start,sb.s_block_start)
                    f.seek(partition2[3])
                    #Se escribe el superbloque
                    f.write(sb_bytes)
                    #Se escriben los bitmap de inodos y bloques
                    f.seek(bm_inode_start)
                    for i in range(bitmap_inodes):
                        f.write(b'0')
                    f.seek(bm_block_start)
                    for i in range(bitmap_blocks):
                        f.write(b'0')
                    #Se escriben los inodos
                    f.seek(inode_start)
                    iblock = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
                    for i in range(bitmap_inodes):
                        inode = struct.pack(format_i,0,0,0,0,0,0,*iblock,'0'.encode('utf-8'),0)
                        f.write(inode)
                        f.seek(inode_start + (i+1) * inode_size)
                    #Se escriben los bloques
                    f.seek(block_start)
                    for i in range(bitmap_blocks):
                        block = struct.pack(format_b,b'')
                        f.write(block)
                        f.seek(block_start + (i+1) * block_size)

                    #Creacion de la carpeta raiz
                    f.seek(bm_block_start)
                    index_b = self.getIndexBock(f.read(blocks_count))
                    print(index_b)
                    f.seek(inode_start)
                    inode_root = f.read(inode_size)
                    inode_root_unpack = struct.unpack(format_i,inode_root)
                    inode_root_unpack = list(inode_root_unpack)
                    inode_root_unpack[0] = 1
                    inode_root_unpack[1] = 1
                    inode_root_unpack[2] = 27
                    inode_root_unpack[3] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[4] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[5] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[6] = index_b
                    inode_root_unpack[22] = '0'.encode('utf-8')
                    inode_root_unpack[23] = 777
                    f.seek(bm_inode_start)
                    f.seek(inode_start+((self.getIndexInode(f.read(inodes_count))-1)*inode_size))
                    f.write(struct.pack(format_i,inode_root_unpack[0],inode_root_unpack[1],inode_root_unpack[2],inode_root_unpack[3],inode_root_unpack[4],
                                        inode_root_unpack[5],inode_root_unpack[6],inode_root_unpack[7],inode_root_unpack[8],inode_root_unpack[9],inode_root_unpack[10],
                                        inode_root_unpack[11],inode_root_unpack[12],inode_root_unpack[13],inode_root_unpack[14],inode_root_unpack[15],inode_root_unpack[16],
                                        inode_root_unpack[17],inode_root_unpack[18],inode_root_unpack[19],inode_root_unpack[20],inode_root_unpack[21],inode_root_unpack[22],inode_root_unpack[23]))
                    #se setea 1 en el bitmap de inodos
                    f.seek(bm_inode_start)
                    f.write(b'1')
                    #se setea 1 en el bitmap de bloques
                    f.seek(bm_block_start)
                    f.write(b'1')
                    #se crea el bloque de la carpeta raiz
                    count = 0
                    f.seek(bm_inode_start)
                    count = self.getIndexInode(f.read(inodes_count))
                    f.seek(block_start)
                    block_root = struct.pack('12s i 12s i 12s i 12s i',
                                        '.'.encode ('utf-8'),0,
                                        '..'.encode ('utf-8'),0,
                                        'users.txt'.encode ('utf-8'),count,
                                        ''.encode ('utf-8'),-1)
                    f.write(block_root)
                    #se crea el inodo del archivo users.txt
                    f.seek(bm_block_start)
                    index_b = self.getIndexBock(f.read(blocks_count))
                    f.seek(bm_inode_start)
                    f.seek(inode_start+(self.getIndexInode(f.read(inodes_count))*inode_size))
                    inode_users = f.read(inode_size)
                    inode_users_unpack = struct.unpack(format_i,inode_users)
                    inode_users_unpack = list(inode_users_unpack)
                    inode_users_unpack[0] = 1
                    inode_users_unpack[1] = 1
                    inode_users_unpack[2] = 27
                    inode_users_unpack[3] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[4] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[5] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[6] = index_b
                    inode_users_unpack[22] = '1'.encode('utf-8')
                    inode_users_unpack[23] = 777
                    f.seek(bm_inode_start)
                    f.seek(inode_start+((self.getIndexInode(f.read(inodes_count))-1)*inode_size))
                    f.write(struct.pack(format_i,inode_users_unpack[0],inode_users_unpack[1],inode_users_unpack[2],inode_users_unpack[3],inode_users_unpack[4],inode_users_unpack[5],inode_users_unpack[6],inode_users_unpack[7],inode_users_unpack[8],inode_users_unpack[9],inode_users_unpack[10],inode_users_unpack[11],inode_users_unpack[12],inode_users_unpack[13],inode_users_unpack[14],inode_users_unpack[15],inode_users_unpack[16],inode_users_unpack[17],inode_users_unpack[18],inode_users_unpack[19],inode_users_unpack[20],inode_users_unpack[21],inode_users_unpack[22],inode_users_unpack[23]))
                    #se setea 1 en el bitmap de inodos
                    f.seek(bm_inode_start)
                    f.seek(bm_inode_start+self.getIndexInode(f.read(inodes_count))-1)
                    f.write(b'1')
                    #se crea el bloque del archivo users.txt
                    f.seek(bm_block_start)
                    f.seek(block_start+((self.getIndexBock(f.read(blocks_count))-1)*block_size))
                    block_user_pack = struct.pack(format_b,'1,G,root\n1,U,root,root,123\n'.encode('utf-8'))
                    f.write(block_user_pack)
                    #se setea 1 en el bitmap de bloques
                    f.seek(bm_block_start)
                    f.seek(bm_block_start+self.getIndexBock(f.read(blocks_count))-1)
                    f.write(b'1')
                    
                    journaling = []
                    journaling.append(Journaling("mkfile","/users.txt","1,G,root\n1,U,root,root,123\n",datetime.datetime.now()))
                    f.seek(partition2[3]+struct.calcsize(format_sb))
                    f.write(pickle.dumps(journaling[0]))

                    print("Sistema de archivos creado correctamente")
                elif partition3[5].decode('utf-8').rstrip("\x00")==part_m.name_partition:
                    size_journaling  = partition3[4] * 0.010
                    size_journaling = math.floor(size_journaling)
                    n = (partition3[4] - struct.calcsize(format_sb))/(4 + struct.calcsize(format_i) + 3 * struct.calcsize(format_b) + size_journaling)
                    struct_n = math.floor(n)
                    bitmap_inodes = struct_n
                    bitmap_blocks = struct_n * 3
                    size_bitmap_inodes = bitmap_inodes * struct.calcsize(format_i)
                    size_bitmap_blocks = bitmap_blocks * struct.calcsize(format_b)
                    file_sistem = 3
                    inodes_count = bitmap_inodes
                    blocks_count = bitmap_blocks
                    free_blocks_count = bitmap_blocks - 1
                    free_inodes_count = bitmap_inodes - 1
                    mtime = 0
                    umtime = 0
                    mnt_count = 0
                    magic = 0xEF53
                    inode_size = struct.calcsize(format_i)
                    block_size = struct.calcsize(format_b)
                    first_ino = 0
                    first_blo = 0
                    bm_inode_start = partition3[3] + struct.calcsize(format_sb) + size_journaling
                    bm_block_start = bm_inode_start + bitmap_inodes
                    inode_start = bm_block_start + bitmap_blocks
                    block_start = inode_start + bitmap_inodes * inode_size
                    #se le asigna al superbloque todo lo que se calculó
                    sb = SuperBlock(file_sistem,inodes_count,blocks_count,free_blocks_count,free_inodes_count,mtime,umtime,mnt_count,magic,inode_size,block_size,first_ino,first_blo,bm_inode_start,bm_block_start,inode_start,block_start)
                    sb_bytes = struct.pack(format_sb,sb.s_filesystem_type,sb.s_inodes_count,sb.s_blocks_count,sb.s_free_blocks_count,sb.s_free_inodes_count,sb.s_mtime,
                                           sb.s_umtime,sb.s_mnt_count,sb.s_magic,sb.s_inode_s,sb.s_block_s,sb.s_first_ino,sb.s_first_blo,sb.s_bm_inode_start,sb.s_bm_block_start,
                                           sb.s_inode_start,sb.s_block_start)
                    f.seek(partition3[3])
                    #Se escribe el superbloque
                    f.write(sb_bytes)
                    #Se escriben los bitmap de inodos y bloques
                    f.seek(bm_inode_start)
                    for i in range(bitmap_inodes):
                        f.write(b'0')
                    f.seek(bm_block_start)
                    for i in range(bitmap_blocks):
                        f.write(b'0')
                    #Se escriben los inodos
                    f.seek(inode_start)
                    iblock = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
                    for i in range(bitmap_inodes):
                        inode = struct.pack(format_i,0,0,0,0,0,0,*iblock,'0'.encode('utf-8'),0)
                        f.write(inode)
                        f.seek(inode_start + (i+1) * inode_size)
                    #Se escriben los bloques
                    f.seek(block_start)
                    for i in range(bitmap_blocks):
                        block = struct.pack(format_b,b'')
                        f.write(block)
                        f.seek(block_start + (i+1) * block_size)

                    #Creacion de la carpeta raiz
                    f.seek(bm_block_start)
                    index_b = self.getIndexBock(f.read(blocks_count))
                    print(index_b)
                    f.seek(inode_start)
                    inode_root = f.read(inode_size)
                    inode_root_unpack = struct.unpack(format_i,inode_root)
                    inode_root_unpack = list(inode_root_unpack)
                    inode_root_unpack[0] = 1
                    inode_root_unpack[1] = 1
                    inode_root_unpack[2] = 27
                    inode_root_unpack[3] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[4] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[5] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[6] = index_b
                    inode_root_unpack[22] = '0'.encode('utf-8')
                    inode_root_unpack[23] = 777
                    f.seek(bm_inode_start)
                    f.seek(inode_start+((self.getIndexInode(f.read(inodes_count))-1)*inode_size))
                    f.write(struct.pack(format_i,inode_root_unpack[0],inode_root_unpack[1],inode_root_unpack[2],inode_root_unpack[3],inode_root_unpack[4],
                                        inode_root_unpack[5],inode_root_unpack[6],inode_root_unpack[7],inode_root_unpack[8],inode_root_unpack[9],inode_root_unpack[10],
                                        inode_root_unpack[11],inode_root_unpack[12],inode_root_unpack[13],inode_root_unpack[14],inode_root_unpack[15],inode_root_unpack[16],
                                        inode_root_unpack[17],inode_root_unpack[18],inode_root_unpack[19],inode_root_unpack[20],inode_root_unpack[21],inode_root_unpack[22],inode_root_unpack[23]))
                    #se setea 1 en el bitmap de inodos
                    f.seek(bm_inode_start)
                    f.write(b'1')
                    #se setea 1 en el bitmap de bloques
                    f.seek(bm_block_start)
                    f.write(b'1')
                    #se crea el bloque de la carpeta raiz
                    count = 0
                    f.seek(bm_inode_start)
                    count = self.getIndexInode(f.read(inodes_count))
                    f.seek(block_start)
                    block_root = struct.pack('12s i 12s i 12s i 12s i',
                                        '.'.encode ('utf-8'),0,
                                        '..'.encode ('utf-8'),0,
                                        'users.txt'.encode ('utf-8'),count,
                                        ''.encode ('utf-8'),-1)
                    f.write(block_root)
                    #se crea el inodo del archivo users.txt
                    f.seek(bm_block_start)
                    index_b = self.getIndexBock(f.read(blocks_count))
                    f.seek(bm_inode_start)
                    f.seek(inode_start+(self.getIndexInode(f.read(inodes_count))*inode_size))
                    inode_users = f.read(inode_size)
                    inode_users_unpack = struct.unpack(format_i,inode_users)
                    inode_users_unpack = list(inode_users_unpack)
                    inode_users_unpack[0] = 1
                    inode_users_unpack[1] = 1
                    inode_users_unpack[2] = 27
                    inode_users_unpack[3] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[4] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[5] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[6] = index_b
                    inode_users_unpack[22] = '1'.encode('utf-8')
                    inode_users_unpack[23] = 777
                    f.seek(bm_inode_start)
                    f.seek(inode_start+((self.getIndexInode(f.read(inodes_count))-1)*inode_size))
                    f.write(struct.pack(format_i,inode_users_unpack[0],inode_users_unpack[1],inode_users_unpack[2],inode_users_unpack[3],inode_users_unpack[4],inode_users_unpack[5],inode_users_unpack[6],inode_users_unpack[7],inode_users_unpack[8],inode_users_unpack[9],inode_users_unpack[10],inode_users_unpack[11],inode_users_unpack[12],inode_users_unpack[13],inode_users_unpack[14],inode_users_unpack[15],inode_users_unpack[16],inode_users_unpack[17],inode_users_unpack[18],inode_users_unpack[19],inode_users_unpack[20],inode_users_unpack[21],inode_users_unpack[22],inode_users_unpack[23]))
                    #se setea 1 en el bitmap de inodos
                    f.seek(bm_inode_start)
                    f.seek(bm_inode_start+self.getIndexInode(f.read(inodes_count))-1)
                    f.write(b'1')
                    #se crea el bloque del archivo users.txt
                    f.seek(bm_block_start)
                    f.seek(block_start+((self.getIndexBock(f.read(blocks_count))-1)*block_size))
                    block_user_pack = struct.pack(format_b,'1,G,root\n1,U,root,root,123\n'.encode('utf-8'))
                    f.write(block_user_pack)
                    #se setea 1 en el bitmap de bloques
                    f.seek(bm_block_start)
                    f.seek(bm_block_start+self.getIndexBock(f.read(blocks_count))-1)
                    f.write(b'1')
                    
                    journaling = []
                    journaling.append(Journaling("mkfile","/users.txt","1,G,root\n1,U,root,root,123\n",datetime.datetime.now()))
                    f.seek(partition3[3]+struct.calcsize(format_sb))
                    f.write(pickle.dumps(journaling[0]))

                    print("Sistema de archivos creado correctamente")
                elif partition4[5].decode('utf-8').rstrip("\x00")==part_m.name_partition:
                    size_journaling  = partition4[4] * 0.010
                    size_journaling = math.floor(size_journaling)
                    n = (partition4[4] - struct.calcsize(format_sb))/(4 + struct.calcsize(format_i) + 3 * struct.calcsize(format_b) + size_journaling)
                    struct_n = math.floor(n)
                    bitmap_inodes = struct_n
                    bitmap_blocks = struct_n * 3
                    size_bitmap_inodes = bitmap_inodes * struct.calcsize(format_i)
                    size_bitmap_blocks = bitmap_blocks * struct.calcsize(format_b)
                    file_sistem = 3
                    inodes_count = bitmap_inodes
                    blocks_count = bitmap_blocks
                    free_blocks_count = bitmap_blocks - 1
                    free_inodes_count = bitmap_inodes - 1
                    mtime = 0
                    umtime = 0
                    mnt_count = 0
                    magic = 0xEF53
                    inode_size = struct.calcsize(format_i)
                    block_size = struct.calcsize(format_b)
                    first_ino = 0
                    first_blo = 0
                    bm_inode_start = partition4[3] + struct.calcsize(format_sb) + size_journaling
                    bm_block_start = bm_inode_start + bitmap_inodes
                    inode_start = bm_block_start + bitmap_blocks
                    block_start = inode_start + bitmap_inodes * inode_size
                    #se le asigna al superbloque todo lo que se calculó
                    sb = SuperBlock(file_sistem,inodes_count,blocks_count,free_blocks_count,free_inodes_count,mtime,umtime,mnt_count,magic,inode_size,block_size,first_ino,first_blo,bm_inode_start,bm_block_start,inode_start,block_start)
                    sb_bytes = struct.pack(format_sb,sb.s_filesystem_type,sb.s_inodes_count,sb.s_blocks_count,sb.s_free_blocks_count,sb.s_free_inodes_count,sb.s_mtime,
                                           sb.s_umtime,sb.s_mnt_count,sb.s_magic,sb.s_inode_s,sb.s_block_s,sb.s_first_ino,sb.s_first_blo,sb.s_bm_inode_start,sb.s_bm_block_start,
                                           sb.s_inode_start,sb.s_block_start)
                    f.seek(partition4[3])
                    #Se escribe el superbloque
                    f.write(sb_bytes)
                    #Se escriben los bitmap de inodos y bloques
                    f.seek(bm_inode_start)
                    for i in range(bitmap_inodes):
                        f.write(b'0')
                    f.seek(bm_block_start)
                    for i in range(bitmap_blocks):
                        f.write(b'0')
                    #Se escriben los inodos
                    f.seek(inode_start)
                    iblock = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
                    for i in range(bitmap_inodes):
                        inode = struct.pack(format_i,0,0,0,0,0,0,*iblock,'0'.encode('utf-8'),0)
                        f.write(inode)
                        f.seek(inode_start + (i+1) * inode_size)
                    #Se escriben los bloques
                    f.seek(block_start)
                    for i in range(bitmap_blocks):
                        block = struct.pack(format_b,b'')
                        f.write(block)
                        f.seek(block_start + (i+1) * block_size)

                    #Creacion de la carpeta raiz
                    f.seek(bm_block_start)
                    index_b = self.getIndexBock(f.read(blocks_count))
                    print(index_b)
                    f.seek(inode_start)
                    inode_root = f.read(inode_size)
                    inode_root_unpack = struct.unpack(format_i,inode_root)
                    inode_root_unpack = list(inode_root_unpack)
                    inode_root_unpack[0] = 1
                    inode_root_unpack[1] = 1
                    inode_root_unpack[2] = 27
                    inode_root_unpack[3] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[4] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[5] = int(datetime.datetime.now().timestamp())
                    inode_root_unpack[6] = index_b
                    inode_root_unpack[22] = '0'.encode('utf-8')
                    inode_root_unpack[23] = 777
                    f.seek(bm_inode_start)
                    f.seek(inode_start+((self.getIndexInode(f.read(inodes_count))-1)*inode_size))
                    f.write(struct.pack(format_i,inode_root_unpack[0],inode_root_unpack[1],inode_root_unpack[2],inode_root_unpack[3],inode_root_unpack[4],
                                        inode_root_unpack[5],inode_root_unpack[6],inode_root_unpack[7],inode_root_unpack[8],inode_root_unpack[9],inode_root_unpack[10],
                                        inode_root_unpack[11],inode_root_unpack[12],inode_root_unpack[13],inode_root_unpack[14],inode_root_unpack[15],inode_root_unpack[16],
                                        inode_root_unpack[17],inode_root_unpack[18],inode_root_unpack[19],inode_root_unpack[20],inode_root_unpack[21],inode_root_unpack[22],inode_root_unpack[23]))
                    #se setea 1 en el bitmap de inodos
                    f.seek(bm_inode_start)
                    f.write(b'1')
                    #se setea 1 en el bitmap de bloques
                    f.seek(bm_block_start)
                    f.write(b'1')
                    #se crea el bloque de la carpeta raiz
                    count = 0
                    f.seek(bm_inode_start)
                    count = self.getIndexInode(f.read(inodes_count))
                    f.seek(block_start)
                    block_root = struct.pack('12s i 12s i 12s i 12s i',
                                        '.'.encode ('utf-8'),0,
                                        '..'.encode ('utf-8'),0,
                                        'users.txt'.encode ('utf-8'),count,
                                        ''.encode ('utf-8'),-1)
                    f.write(block_root)
                    #se crea el inodo del archivo users.txt
                    f.seek(bm_block_start)
                    index_b = self.getIndexBock(f.read(blocks_count))
                    f.seek(bm_inode_start)
                    f.seek(inode_start+(self.getIndexInode(f.read(inodes_count))*inode_size))
                    inode_users = f.read(inode_size)
                    inode_users_unpack = struct.unpack(format_i,inode_users)
                    inode_users_unpack = list(inode_users_unpack)
                    inode_users_unpack[0] = 1
                    inode_users_unpack[1] = 1
                    inode_users_unpack[2] = 27
                    inode_users_unpack[3] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[4] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[5] = int(datetime.datetime.now().timestamp())
                    inode_users_unpack[6] = index_b
                    inode_users_unpack[22] = '1'.encode('utf-8')
                    inode_users_unpack[23] = 777
                    f.seek(bm_inode_start)
                    f.seek(inode_start+((self.getIndexInode(f.read(inodes_count))-1)*inode_size))
                    f.write(struct.pack(format_i,inode_users_unpack[0],inode_users_unpack[1],inode_users_unpack[2],inode_users_unpack[3],inode_users_unpack[4],inode_users_unpack[5],inode_users_unpack[6],inode_users_unpack[7],inode_users_unpack[8],inode_users_unpack[9],inode_users_unpack[10],inode_users_unpack[11],inode_users_unpack[12],inode_users_unpack[13],inode_users_unpack[14],inode_users_unpack[15],inode_users_unpack[16],inode_users_unpack[17],inode_users_unpack[18],inode_users_unpack[19],inode_users_unpack[20],inode_users_unpack[21],inode_users_unpack[22],inode_users_unpack[23]))
                    #se setea 1 en el bitmap de inodos
                    f.seek(bm_inode_start)
                    f.seek(bm_inode_start+self.getIndexInode(f.read(inodes_count))-1)
                    f.write(b'1')
                    #se crea el bloque del archivo users.txt
                    f.seek(bm_block_start)
                    f.seek(block_start+((self.getIndexBock(f.read(blocks_count))-1)*block_size))
                    block_user_pack = struct.pack(format_b,'1,G,root\n1,U,root,root,123\n'.encode('utf-8'))
                    f.write(block_user_pack)
                    #se setea 1 en el bitmap de bloques
                    f.seek(bm_block_start)
                    f.seek(bm_block_start+self.getIndexBock(f.read(blocks_count))-1)
                    f.write(b'1')
                    
                    journaling = []
                    journaling.append(Journaling("mkfile","/users.txt","1,G,root\n1,U,root,root,123\n",datetime.datetime.now()))
                    f.seek(partition4[3]+struct.calcsize(format_sb))
                    f.write(pickle.dumps(journaling[0]))

                    print("Sistema de archivos creado correctamente")


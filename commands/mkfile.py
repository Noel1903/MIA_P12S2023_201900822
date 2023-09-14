from  commands.login import login
from commands.mount import mount
import struct

class mkfile:
    path_mount =""
    def __init__(self,params = None):
        self.params = params
        if params != None:
            self.path = ""
            self.r = ""
            self.size = 0
            self.cont = ""
            self.execute()
            


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
        
    def execute(self):
        for i in self.params:
            if i[0] == "path":
                self.path = i[1]
            elif i[0] == "r":
                self.r = i[1]
            elif i[0] == "size":
                self.size = i[1]
            elif i[0] == "cont":
                self.cont = i[1]
        
        log = login(None)
        id = log.getId()[len(log.getId())-1]
        userlogued = log.getUserLogued()[len(log.getUserLogued())-1]
        user = log.getUser()[len(log.getUser())-1]
        #print(id,userlogued,user)
        if userlogued and id!= "":
            format_mbr = "I I I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
            format_ebr = "I I I c c c c I I 16s c c c I I 16s c c c I I 16s"
            format_sb = "I I I I I I I I I I I I I I I I I"
            format_i = "I I I I I I 15i c I"
            format_b_folder = "12s i 12s i 12s i 12s i"
            format_b = "64s"

            part_m = 0
            exist = False
            m = mount(None)
            for i in m.partitions_mounted:
                if i.part_id.rstrip("\x00") == id:
                    part_m = i
                    exist = True
                    break
            if not exist:
                print("No se encontro la particion")
                return
            
            self.path_mount = part_m.path
            with open(self.path_mount,"rb+") as f:
                f.seek(0)
                data_bytes = f.read(struct.calcsize(format_mbr))
                mbr_unpack = struct.unpack(format_mbr,data_bytes)
                partition1 = mbr_unpack[4:10]
                partition2 = mbr_unpack[10:16]
                partition3 = mbr_unpack[16:22]
                partition4 = mbr_unpack[22:28]
                if partition1[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    f.seek(partition1[3])
                    data_sb = f.read(struct.calcsize(format_sb))
                    sb_unpack = struct.unpack(format_sb,data_sb)
                    index_inode = 0
                    inode_file = 0
                    self.path = self.path.split("/")
                    cont = 0
                    for i in self.path:
                        if i == "":
                            cont += 1
                            continue

                        index_inode = self.searchInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                        if cont == len(self.path)-2:
                            inode_file = index_inode

                        if cont == len(self.path)-1:
                            #print(i,index_inode-1)
                            self.createFile(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode-1,i)
                        
                        cont += 1

                    print("Archivo creado")
                elif partition2[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    f.seek(partition2[3])
                    data_sb = f.read(struct.calcsize(format_sb))
                    sb_unpack = struct.unpack(format_sb,data_sb)
                    index_inode = 0
                    inode_file = 0
                    self.path = self.path.split("/")
                    cont = 0
                    for i in self.path:
                        if i == "":
                            cont += 1
                            continue

                        index_inode = self.searchInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                        if cont == len(self.path)-2:
                            inode_file = index_inode

                        if cont == len(self.path)-1:
                            print(i,index_inode-1)
                            self.createFile(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode-1,i)
                        
                        cont += 1

                    print("Archivo creado")
                elif partition3[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    f.seek(partition3[3])
                    data_sb = f.read(struct.calcsize(format_sb))
                    sb_unpack = struct.unpack(format_sb,data_sb)
                    index_inode = 0
                    inode_file = 0
                    self.path = self.path.split("/")
                    cont = 0
                    for i in self.path:
                        if i == "":
                            cont += 1
                            continue

                        index_inode = self.searchInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                        if cont == len(self.path)-2:
                            inode_file = index_inode

                        if cont == len(self.path)-1:
                            print(i,index_inode-1)
                            self.createFile(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode-1,i)
                        
                        cont += 1

                    print("Archivo creado")
                elif partition4[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    f.seek(partition4[3])
                    data_sb = f.read(struct.calcsize(format_sb))
                    sb_unpack = struct.unpack(format_sb,data_sb)
                    index_inode = 0
                    inode_file = 0
                    self.path = self.path.split("/")
                    cont = 0
                    for i in self.path:
                        if i == "":
                            cont += 1
                            continue

                        index_inode = self.searchInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                        
                        if cont == len(self.path)-1:
                            print(i,index_inode-1)
                            self.createFile(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                        
                        cont += 1
                print("**********************************ARCHIVO**********************************")
                #self.showBlocks(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2])
                print("Archivo creado")


    def searchInode(self,bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,index,folder):
        format_i = "I I I I I I 16i c I"
        format_b_folder = "12s i 12s i 12s i 12s i"
        format_pointers = "16i"
        block_p = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        with open(self.path_mount,"rb+") as f:
            if index != 0:
                index = index - 1 
            posicion_init = start_inodes+(struct.calcsize(format_i)*(index))
            f.seek(start_inodes+(struct.calcsize(format_i)*(index)))
            inode_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
            #inode_unpack = list(inode_unpack)
            #print(inode_unpack,"INODO PADRE")
            i_block = inode_unpack[6:22]
            inode_unpack = list(inode_unpack)
            
            cont = 0
            for i in i_block:
                if i != -1:
                    i = i-1
                    if cont < 13:
                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                        block_unpack = struct.unpack(format_b_folder,f.read(struct.calcsize(format_b_folder)))
                        block_unpack = list(block_unpack)
                        if block_unpack[0].decode('utf-8').rstrip("\x00") == folder:
                            return block_unpack[1]
                        elif block_unpack[2].decode('utf-8').rstrip("\x00") == folder:
                            return block_unpack[3]
                        elif block_unpack[4].decode('utf-8').rstrip("\x00") == folder:
                            return block_unpack[5]
                        elif block_unpack[6].decode('utf-8').rstrip("\x00") == folder:
                            return block_unpack[7]
                        elif block_unpack[0].decode('utf-8').rstrip("\x00") == "":
                            f.seek(bm_inodes)
                            inode_pointer = self.getIndexInode(f.read(inode_size))
                            block_unpack[0] = folder.encode('utf-8')
                            block_unpack[1] = inode_pointer
                            f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                            f.write(struct.pack(format_b_folder,block_unpack[0],block_unpack[1],block_unpack[2],block_unpack[3],block_unpack[4],block_unpack[5],block_unpack[6],block_unpack[7]))
                            
                            f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                            f.write(struct.pack(format_i,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                            f.seek(bm_inodes+(inode_pointer-1))
                            f.write(b'1')
                            f.seek(bm_blocks)
                            block_pointer = self.getIndexBock(f.read(block_size))
                            f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_pointer-1)))
                            f.write(struct.pack(format_b_folder,b'.',0,b'..',0,b'',-1,b'',-1))
                            f.seek(bm_blocks+(block_pointer-1))
                            f.write(b'1')
                            f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                            f.write(struct.pack(format_i,1,1,1,1,1,1,block_pointer,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                            f.seek(bm_inodes)
                            inode_pointer = self.getIndexInode(f.read(inode_size))
                            return inode_pointer - 1
                        elif block_unpack[2].decode('utf-8').rstrip("\x00") == "":
                            f.seek(bm_inodes)
                            inode_pointer = self.getIndexInode(f.read(inode_size))
                            block_unpack[2] = folder.encode('utf-8')
                            block_unpack[3] = inode_pointer
                            f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                            f.write(struct.pack(format_b_folder,block_unpack[0],block_unpack[1],block_unpack[2],block_unpack[3],block_unpack[4],block_unpack[5],block_unpack[6],block_unpack[7]))
                            f.seek(bm_inodes+(inode_pointer-1))
                            f.write(b'1')
                            f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                            f.write(struct.pack(format_i,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                            f.seek(bm_blocks)
                            block_pointer = self.getIndexBock(f.read(block_size))
                            f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_pointer-1)))
                            f.write(struct.pack(format_b_folder,b'.',0,b'..',0,b'',-1,b'',-1))
                            f.seek(bm_blocks+(block_pointer-1))
                            f.write(b'1')
                            f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                            f.write(struct.pack(format_i,1,1,1,1,1,1,block_pointer,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                            f.seek(bm_inodes)
                            inode_pointer = self.getIndexInode(f.read(inode_size))
                            return inode_pointer - 1
                        elif block_unpack[4].decode('utf-8').rstrip("\x00") == "":
                            f.seek(bm_inodes)
                            inode_pointer = self.getIndexInode(f.read(inode_size))
                            block_unpack[4] = folder.encode('utf-8')
                            block_unpack[5] = inode_pointer
                            f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                            f.write(struct.pack(format_b_folder,block_unpack[0],block_unpack[1],block_unpack[2],block_unpack[3],block_unpack[4],block_unpack[5],block_unpack[6],block_unpack[7]))
                            f.seek(bm_inodes+(inode_pointer-1))
                            f.write(b'1')
                            f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                            f.write(struct.pack(format_i,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                            f.seek(bm_blocks)
                            block_pointer = self.getIndexBock(f.read(block_size))
                            f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_pointer-1)))
                            f.write(struct.pack(format_b_folder,b'.',0,b'..',0,b'',-1,b'',-1))
                            f.seek(bm_blocks+(block_pointer-1))
                            f.write(b'1')
                            f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                            f.write(struct.pack(format_i,1,1,1,1,1,1,block_pointer,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                            f.seek(bm_inodes)
                            inode_pointer = self.getIndexInode(f.read(inode_size))
                            return inode_pointer - 1
                        elif block_unpack[6].decode('utf-8').rstrip("\x00") == "":
                            print("Aqui debe estr el home")
                            f.seek(bm_inodes)
                            inode_pointer = self.getIndexInode(f.read(inode_size))
                            block_unpack[6] = folder.encode('utf-8')
                            block_unpack[7] = inode_pointer
                            f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                            #print(start_blocks+(block_size*i),"bloque de carpeta")
                            f.write(struct.pack(format_b_folder,block_unpack[0],block_unpack[1],block_unpack[2],block_unpack[3],block_unpack[4],block_unpack[5],block_unpack[6],block_unpack[7]))
                            f.seek(bm_inodes+(inode_pointer-1))
                            f.write(b'1')
                            f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                            #print(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                            f.write(struct.pack(format_i,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                            f.seek(bm_blocks)
                            block_pointer = self.getIndexBock(f.read(block_size))
                            f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_pointer-1)))
                            #print(start_blocks+(block_size*block_pointer-1),"bloque de carpeta . . . ")
                            f.write(struct.pack(format_b_folder,b'.',0,b'..',0,b'',-1,b'',-1))
                            f.seek(bm_blocks+(block_pointer-1))
                            f.write(b'1')
                            f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                            print(block_pointer)
                            print(f.write(struct.pack(format_i,1,1,1,1,1,1,block_pointer,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664)))
                        
                            f.seek(bm_inodes)
                            inode_pointer = self.getIndexInode(f.read(inode_size))
                            print(inode_pointer)
                            return inode_pointer - 1
                    elif cont >= 13:
                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                        block_unpack = struct.unpack(format_pointers,f.read(struct.calcsize(format_pointers)))
                        block_unpack = list(block_unpack)
                        #print(block_unpack)
                        for j in range(len(block_unpack)):
                            if block_unpack[j] != -1:
                                f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_unpack[j]-1)))
                                block_unpack2 = struct.unpack(format_b_folder,f.read(struct.calcsize(format_b_folder)))
                                block_unpack2 = list(block_unpack2)
                                print(block_unpack2)
                                if block_unpack2[0].decode('utf-8').rstrip("\x00") == folder:
                                    return block_unpack2[1]
                                elif block_unpack2[2].decode('utf-8').rstrip("\x00") == folder:
                                    return block_unpack2[3]
                                elif block_unpack2[4].decode('utf-8').rstrip("\x00") == folder:
                                    return block_unpack2[5]
                                elif block_unpack2[6].decode('utf-8').rstrip("\x00") == folder:
                                    return block_unpack2[7]
                                elif block_unpack2[0].decode('utf-8').rstrip("\x00") == "":
                                    f.seek(bm_inodes)
                                    inode_pointer = self.getIndexInode(f.read(inode_size))
                                    block_unpack2[0] = folder.encode('utf-8')
                                    block_unpack2[1] = inode_pointer
                                    f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_unpack[j]-1)))
                                    f.write(struct.pack(format_b_folder,block_unpack2[0],block_unpack2[1],block_unpack2[2],block_unpack2[3],block_unpack2[4],block_unpack[5],block_unpack2[6],block_unpack2[7]))
                                    
                                    f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                                    f.write(struct.pack(format_i,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                                    f.seek(bm_inodes+(inode_pointer-1))
                                    f.write(b'1')
                                    f.seek(bm_blocks)
                                    block_pointer = self.getIndexBock(f.read(block_size))
                                    f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_pointer-1)))
                                    f.write(struct.pack(format_b_folder,b'.',0,b'..',0,b'',-1,b'',-1))
                                    f.seek(bm_blocks+(block_pointer-1))
                                    f.write(b'1')
                                    f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                                    f.write(struct.pack(format_i,1,1,1,1,1,1,block_pointer,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                                    f.seek(bm_inodes)
                                    inode_pointer = self.getIndexInode(f.read(inode_size))
                                    return inode_pointer - 1
                                elif block_unpack2[2].decode('utf-8').rstrip("\x00") == "":
                                    f.seek(bm_inodes)
                                    inode_pointer = self.getIndexInode(f.read(inode_size))
                                    block_unpack2[2] = folder.encode('utf-8')
                                    block_unpack2[3] = inode_pointer
                                    f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_unpack[j]-1)))
                                    f.write(struct.pack(format_b_folder,block_unpack2[0],block_unpack2[1],block_unpack2[2],block_unpack2[3],block_unpack2[4],block_unpack2[5],block_unpack2[6],block_unpack2[7]))
                                    f.seek(bm_inodes+(inode_pointer-1))
                                    f.write(b'1')
                                    f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                                    f.write(struct.pack(format_i,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                                    f.seek(bm_blocks)
                                    block_pointer = self.getIndexBock(f.read(block_size))
                                    f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_pointer-1)))
                                    f.write(struct.pack(format_b_folder,b'.',0,b'..',0,b'',-1,b'',-1))
                                    f.seek(bm_blocks+(block_pointer-1))
                                    f.write(b'1')
                                    f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                                    f.write(struct.pack(format_i,1,1,1,1,1,1,block_pointer,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                                    f.seek(bm_inodes)
                                    inode_pointer = self.getIndexInode(f.read(inode_size))
                                    return inode_pointer - 1
                                elif block_unpack2[4].decode('utf-8').rstrip("\x00") == "":
                                    f.seek(bm_inodes)
                                    inode_pointer = self.getIndexInode(f.read(inode_size))
                                    block_unpack2[4] = folder.encode('utf-8')
                                    block_unpack2[5] = inode_pointer
                                    f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_unpack[j]-1)))
                                    f.write(struct.pack(format_b_folder,block_unpack2[0],block_unpack2[1],block_unpack2[2],block_unpack2[3],block_unpack2[4],block_unpack2[5],block_unpack2[6],block_unpack2[7]))
                                    f.seek(bm_inodes+(inode_pointer-1))
                                    f.write(b'1')
                                    f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                                    f.write(struct.pack(format_i,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                                    f.seek(bm_blocks)
                                    block_pointer = self.getIndexBock(f.read(block_size))
                                    f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_pointer-1)))
                                    f.write(struct.pack(format_b_folder,b'.',0,b'..',0,b'',-1,b'',-1))
                                    f.seek(bm_blocks+(block_pointer-1))
                                    f.write(b'1')
                                    f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                                    f.write(struct.pack(format_i,1,1,1,1,1,1,block_pointer,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                                    f.seek(bm_inodes)
                                    inode_pointer = self.getIndexInode(f.read(inode_size))
                                    return inode_pointer - 1
                                elif block_unpack2[6].decode('utf-8').rstrip("\x00") == "":
                                    print("Aqui debe estr el home")
                                    f.seek(bm_inodes)
                                    inode_pointer = self.getIndexInode(f.read(inode_size))
                                    block_unpack2[6] = folder.encode('utf-8')
                                    block_unpack2[7] = inode_pointer
                                    f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_unpack[j]-1)))
                                    #print(start_blocks+(block_size*i),"bloque de carpeta")
                                    f.write(struct.pack(format_b_folder,block_unpack2[0],block_unpack2[1],block_unpack2[2],block_unpack2[3],block_unpack2[4],block_unpack2[5],block_unpack2[6],block_unpack2[7]))
                                    f.seek(bm_inodes+(inode_pointer-1))
                                    f.write(b'1')
                                    f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                                    #print(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                                    f.write(struct.pack(format_i,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                                    f.seek(bm_blocks)
                                    block_pointer = self.getIndexBock(f.read(block_size))
                                    f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_pointer-1)))
                                    #print(start_blocks+(block_size*block_pointer-1),"bloque de carpeta . . . ")
                                    f.write(struct.pack(format_b_folder,b'.',0,b'..',0,b'',-1,b'',-1))
                                    f.seek(bm_blocks+(block_pointer-1))
                                    f.write(b'1')
                                    f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                                    print(block_pointer)
                                    print(f.write(struct.pack(format_i,1,1,1,1,1,1,block_pointer,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664)))
                                
                                    f.seek(bm_inodes)
                                    inode_pointer = self.getIndexInode(f.read(inode_size))
                                    print(inode_pointer)
                                    return inode_pointer - 1
                            else:
                                f.seek(bm_blocks)
                                block_pointer = self.getIndexBock(f.read(block_size))
                                block_unpack[j] = block_pointer
                                f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                f.write(struct.pack(format_pointers,block_unpack[0],block_unpack[1],block_unpack[2],block_unpack[3],block_unpack[4],block_unpack[5],block_unpack[6],block_unpack[7],block_unpack[8],block_unpack[9],block_unpack[10],block_unpack[11],block_unpack[12],block_unpack[13],block_unpack[14],block_unpack[15]))
                                f.seek(bm_inodes)
                                inode_pointer = self.getIndexInode(f.read(inode_size))
                                inode_return = inode_pointer
                                f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_pointer-1)))
                                #se localiza y se crea el nuevo bloque de la carpeta
                                f.write(struct.pack(format_b_folder,folder.encode('utf-8')[0:12],inode_pointer,b'',-1,b'',-1,b'',-1))
                                f.seek(bm_blocks+(block_pointer-1))
                                #se marca como ocupado el bloque
                                f.write(b'1')
                                f.seek(bm_blocks)
                                block_pointer = self.getIndexBock(f.read(block_size))
                                f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                                #se crea el nuevo inodo
                                f.write(struct.pack(format_i,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                                #se marca como ocupado el inodo
                                f.seek(bm_inodes+(inode_pointer-1))
                                f.write(b'1')
                                #se crea el bloque de la carpeta padre
                                f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_pointer-1)))
                                f.write(struct.pack(format_b_folder,b'.',0,b'..',0,b'',-1,b'',-1))
                                #se marca como ocupado el bloque
                                f.seek(bm_blocks+(block_pointer-1))
                                f.write(b'1')
                                f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                                #se escribe el nuevo inodo
                                f.write(struct.pack(format_i,1,1,1,1,1,1,block_pointer,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                                f.seek(bm_inodes)
                                inode_return = self.getIndexInode(f.read(inode_size))
                                return inode_return - 1
                else:
                    if cont < 13:
                        f.seek(bm_blocks)
                        block_pointer = self.getIndexBock(f.read(block_size))
                        f.seek(bm_inodes)
                        inode_pointer = self.getIndexInode(f.read(inode_size))
                        inode_return = inode_pointer
                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_pointer-1)))
                        #se localiza y se crea el nuevo bloque de la carpeta
                        f.write(struct.pack(format_b_folder,folder.encode('utf-8')[0:12],inode_pointer,b'',-1,b'',-1,b'',-1))
                        f.seek(bm_blocks+(block_pointer-1))
                        #se marca como ocupado el bloque
                        f.write(b'1')
                        f.seek(bm_blocks)
                        block_pointer = self.getIndexBock(f.read(block_size))
                        f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                        #se crea el nuevo inodo
                        f.write(struct.pack(format_i,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                        #se marca como ocupado el inodo
                        f.seek(bm_inodes+(inode_pointer-1))
                        f.write(b'1')
                        #se crea el bloque de la carpeta padre
                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_pointer-1)))
                        f.write(struct.pack(format_b_folder,b'.',0,b'..',0,b'',-1,b'',-1))
                        #se marca como ocupado el bloque
                        f.seek(bm_blocks+(block_pointer-1))
                        f.write(b'1')
                        f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                        #se escribe el nuevo inodo
                        f.write(struct.pack(format_i,1,1,1,1,1,1,block_pointer,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                        inode_unpack[cont+6] = block_pointer - 1
                        f.seek(bm_inodes)
                        inode_return = self.getIndexInode(f.read(inode_size))
                        f.seek(posicion_init)
                        f.write(struct.pack(format_i,inode_unpack[0],inode_unpack[1],inode_unpack[2],inode_unpack[3],inode_unpack[4],inode_unpack[5],inode_unpack[6],inode_unpack[7],inode_unpack[8],inode_unpack[9],inode_unpack[10],inode_unpack[11],inode_unpack[12],inode_unpack[13],inode_unpack[14],inode_unpack[15],inode_unpack[16],inode_unpack[17],inode_unpack[18],inode_unpack[19],inode_unpack[20],inode_unpack[21],inode_unpack[22],inode_unpack[23]))
                        return inode_return - 1
                    elif cont >= 13:
                        f.seek(bm_blocks)
                        block_pointer01 = self.getIndexBock(f.read(block_size))
                        f.seek(bm_inodes)
                        inode_pointer = self.getIndexInode(f.read(inode_size))
                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_pointer01-1)))
                        #se localiza y se crea el bloque de apuntadores
                        f.write(struct.pack(format_pointers,*block_p))
                        f.seek(bm_blocks+(block_pointer01-1))
                        #se marca como ocupado el bloque
                        f.write(b'1')
                        f.seek(bm_blocks)
                        block_pointer = self.getIndexBock(f.read(block_size))
                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_pointer01-1)))
                        p = struct.unpack(format_pointers,f.read(struct.calcsize(format_pointers)))
                        p = list(p)
                        p[0] = block_pointer
                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_pointer01-1)))
                        f.write(struct.pack(format_pointers,p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10],p[11],p[12],p[13],p[14],p[15]))
                        
                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_pointer-1)))
                        #se localiza y se crea el nuevo bloque de la carpeta
                        f.write(struct.pack(format_b_folder,folder.encode('utf-8')[0:12],inode_pointer,b'',-1,b'',-1,b'',-1))
                        f.seek(bm_blocks+(block_pointer-1))
                        #se marca como ocupado el bloque
                        f.write(b'1')
                        f.seek(bm_blocks)
                        block_pointer = self.getIndexBock(f.read(block_size))
                        f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                        #se crea el nuevo inodo
                        f.write(struct.pack(format_i,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                        #se marca como ocupado el inodo
                        f.seek(bm_inodes+(inode_pointer-1))
                        f.write(b'1')
                        #se crea el bloque de la carpeta padre
                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*(block_pointer-1)))
                        f.write(struct.pack(format_b_folder,b'.',0,b'..',0,b'',-1,b'',-1))
                        #se marca como ocupado el bloque
                        f.seek(bm_blocks+(block_pointer-1))
                        f.write(b'1')
                        f.seek(start_inodes+(struct.calcsize(format_i)*(inode_pointer-1)))
                        #se escribe el nuevo inodo
                        f.write(struct.pack(format_i,1,1,1,1,1,1,block_pointer,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,b'0',664))
                        inode_unpack[cont+6] = block_pointer01
                        f.seek(bm_inodes)
                        inode_return = self.getIndexInode(f.read(inode_size))
                        f.seek(posicion_init)
                        f.write(struct.pack(format_i,inode_unpack[0],inode_unpack[1],inode_unpack[2],inode_unpack[3],inode_unpack[4],inode_unpack[5],inode_unpack[6],inode_unpack[7],inode_unpack[8],inode_unpack[9],inode_unpack[10],inode_unpack[11],inode_unpack[12],inode_unpack[13],inode_unpack[14],inode_unpack[15],inode_unpack[16],inode_unpack[17],inode_unpack[18],inode_unpack[19],inode_unpack[20],inode_unpack[21],inode_unpack[22],inode_unpack[23]))
                        return inode_return - 1

                cont += 1


    def createFile(self,bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,index,folder):
        format_i = "I I I I I I 16i c I"
        format_b_folder = "12s i 12s i 12s i 12s i"
        format_b = "64s"
        format_pointer = "16i"
        with open(self.path_mount,"rb+") as f:
            pos_init = start_inodes+(struct.calcsize(format_i)*(index))
            f.seek(start_inodes+(struct.calcsize(format_i)*(index)))
            inode_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
            #print(inode_unpack,"inodo file")
            #inode_unpack = list(inode_unpack)
            i_block = inode_unpack[6:22]
            inode_unpack = list(inode_unpack)
            cont = 0
            text_file = ""
            if self.size > 0:
                n = 0
                for i in range(self.size+1):
                    text_file += str(n)
                    n += 1
                    if n == 10:
                        n = 0
            else:
                print(self.cont)
                try:
                    with open(self.cont,"r") as file:
                        
                        text_file = file.read()
                        file.close()
                except:
                    print("No se encontro el archivo")
                    return
                
            i = i_block[0]
            i = i-1
            print(i,"index archivo")
            f.seek(start_blocks+(struct.calcsize(format_b_folder)*(i)))
            sizeP = len(text_file)
            cont = 0
            if sizeP <= 64:
                f.write(struct.pack(format_b,text_file.encode('utf-8')))

                print("Archivo creado")
                
           
            else:
                count = 0
                while sizeP > 64:
                    f.seek(bm_blocks)
                    if count == 0:
                        i = i + 1 
                    else:
                        i = self.getIndexBock(f.read(block_size))
                    print(i-1,"index archivo")
                    f.seek(start_blocks+(struct.calcsize(format_b_folder)*(i-1)))
                    f.write(struct.pack(format_b,text_file[0:64].encode('utf-8')))
                    f.seek(bm_blocks+(i-1))
                    f.write(b'1')
                    print("Archivo creado")
                    inode_unpack[cont+6] = i
                    cont += 1
                    text_file = text_file[64:]
                    sizeP = len(text_file)
                    if sizeP <= 64:
                        f.seek(bm_blocks)
                        i = self.getIndexBock(f.read(block_size))
                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*(i-1)))
                        f.write(struct.pack(format_b,text_file.encode('utf-8')))
                        f.seek(bm_blocks+(i-1))
                        f.write(b'1')
                        inode_unpack[cont+6] = i
                        cont += 1
                        print("Archivo creado")

                    count += 1
            f.seek(pos_init)
            inodo_pack = struct.pack(format_i,inode_unpack[0],inode_unpack[1],inode_unpack[2],inode_unpack[3],inode_unpack[4],inode_unpack[5],inode_unpack[6],inode_unpack[7],inode_unpack[8],inode_unpack[9],inode_unpack[10],inode_unpack[11],inode_unpack[12],inode_unpack[13],inode_unpack[14],inode_unpack[15],inode_unpack[16],inode_unpack[17],inode_unpack[18],inode_unpack[19],inode_unpack[20],inode_unpack[21],'1'.encode('utf-8'),inode_unpack[23])           
            f.write(inodo_pack)
            f.close()
            return
            

    def showBlocks(self,bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size):

        format_i = "I I I I I I 15i c I"
        format_b_folder = "12s i 12s i 12s i 12s i"
        with open(self.path_mount,"rb+") as f:
            f.seek(bm_inodes)
            bitmap_inodes = f.read(inode_size)
            print(bitmap_inodes)
            bitmap_inodes = bitmap_inodes.decode('utf-8')
            bitmap_inodes = list(bitmap_inodes)
            
            f.seek(bm_blocks)
            bitmap_blocks = f.read(block_size)

            print(bitmap_blocks)
            bitmap_blocks = bitmap_blocks.decode('utf-8')
            bitmap_blocks = list(bitmap_blocks)

            for i in range(len(bitmap_inodes)):
                if bitmap_inodes[i] != '0':
                    f.seek(start_inodes+(struct.calcsize(format_i)*i))
                    inode_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                    print("Inodo: ",i+1,inode_unpack)
            
            for i in range(len(bitmap_blocks)):
                if bitmap_blocks[i] != '0':
                    f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                    block_unpack = struct.unpack(format_b_folder,f.read(struct.calcsize(format_b_folder)))
                    block_unpack = list(block_unpack)
                    block_unpack[0] = block_unpack[0].decode('utf-8').rstrip("\x00")
                    block_unpack[2] = block_unpack[2].decode('utf-8').rstrip("\x00")
                    block_unpack[4] = block_unpack[4].decode('utf-8').rstrip("\x00")
                    block_unpack[6] = block_unpack[6].decode('utf-8').rstrip("\x00")
                    print("Bloque: ",i+1,block_unpack)





                    

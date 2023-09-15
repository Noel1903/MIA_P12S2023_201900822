from commands.login import login
from commands.mount import mount
import struct

class rename:

    def __init__(self,params):
        self.params = params
        self.path = ""
        self.name = ""
        self.execute()

    def execute(self):
        for i in self.params:
            if i[0] == "path":
                self.path = i[1]
            elif i[0] == "name":
                self.name = i[1]
        if self.path == "":
            print("No se encontro el parametro obligatorio path")
            return
        
        log = login(None)
        id = log.getId()[len(log.getId())-1]
        userlogued = log.getUserLogued()[len(log.getUserLogued())-1]
        user = log.getUser()[len(log.getUser())-1]
        #print(id,userlogued,user)
        if userlogued and id!= "":
            format_mbr = "I I I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
            format_ebr = "I I I c c c c I I 16s c c c I I 16s c c c I I 16s"
            format_sb = "I I I I I I I I I I I I I I I I I"
            format_i = "I I I I I I 16i c I"
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
                    pathsize = self.path
                    self.path = self.path.split("/")
                    contPath = 0
                    for i in self.path:
                        if i == "":
                            continue
                        if contPath == len(self.path)-2:
                            self.renameInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                        else:
                            index_inode = self.searchInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                            if index_inode == None:
                                return
                        contPath += 1
                    
                    #print(index_inode)
                    
                elif partition2[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    f.seek(partition2[3])
                    data_sb = f.read(struct.calcsize(format_sb))
                    sb_unpack = struct.unpack(format_sb,data_sb)
                    index_inode = 0
                    inode_file = 0
                    pathsize = self.path
                    self.path = self.path.split("/")
                    contPath = 0
                    for i in self.path:
                        if i == "":
                            continue
                        if contPath == len(self.path)-2:
                            self.renameInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                        else:
                            index_inode = self.searchInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                            if index_inode == None:
                                return
                        contPath += 1
                elif partition3[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    f.seek(partition3[3])
                    data_sb = f.read(struct.calcsize(format_sb))
                    sb_unpack = struct.unpack(format_sb,data_sb)
                    index_inode = 0
                    inode_file = 0
                    pathsize = self.path
                    self.path = self.path.split("/")
                    contPath = 0
                    for i in self.path:
                        if i == "":
                            continue
                        if contPath == len(self.path)-2:
                            self.renameInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                        else:
                            index_inode = self.searchInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                            if index_inode == None:
                                return
                        contPath += 1
                elif partition4[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    f.seek(partition4[3])
                    data_sb = f.read(struct.calcsize(format_sb))
                    sb_unpack = struct.unpack(format_sb,data_sb)
                    index_inode = 0
                    inode_file = 0
                    pathsize = self.path
                    self.path = self.path.split("/")
                    contPath = 0
                    for i in self.path:
                        if i == "":
                            continue
                        if contPath == len(self.path)-2:
                            self.renameInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                        else:
                            index_inode = self.searchInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                            if index_inode == None:
                                return
                        contPath += 1


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
                i = i - 1
                
                if cont < 13:
                    f.seek(start_blocks+(struct.calcsize(format_b_folder)*(i)))
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
                   
                elif cont>=13:
                    f.seek(start_blocks+(struct.calcsize(format_pointers)*(i)))
                    block_p = struct.unpack(format_pointers,f.read(struct.calcsize(format_pointers)))
                    for j in block_p:
                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*(j-1)))
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
                cont += 1

                
    def renameInode(self,bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,index,folder):
        format_i = "I I I I I I 16i c I"
        format_b_folder = "12s i 12s i 12s i 12s i"
        format_pointers = "16i"
        block_p = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        #print("Folder",folder)
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
                i = i - 1
                
                if cont < 13:
                    f.seek(start_blocks+(struct.calcsize(format_b_folder)*(i)))
                    block_unpack = struct.unpack(format_b_folder,f.read(struct.calcsize(format_b_folder)))
                    block_unpack = list(block_unpack)
                    
                    #print(block_unpack)
                    if block_unpack[0].decode('utf-8').rstrip("\x00") == folder:
                        block_unpack[0] = self.name[0:12].encode('utf-8')
                    elif block_unpack[2].decode('utf-8').rstrip("\x00") == folder:
                        block_unpack[2] = self.name[0:12].encode('utf-8')
                    elif block_unpack[4].decode('utf-8').rstrip("\x00") == folder:
                        block_unpack[4] = self.name[0:12].encode('utf-8')
                    elif block_unpack[6].decode('utf-8').rstrip("\x00") == folder:
                        block_unpack[6] = self.name[0:12].encode('utf-8')
                    else:
                        print("No se encontro el archivo")
                        return
                    f.seek(start_blocks+(struct.calcsize(format_b_folder)*(i)))
                    f.write(struct.pack(format_b_folder,block_unpack[0],block_unpack[1],block_unpack[2],block_unpack[3],block_unpack[4],block_unpack[5],block_unpack[6],block_unpack[7]))
                    print("Se renombro el archivo exitosamente")
                    return
                elif cont>=13:
                    f.seek(start_blocks+(struct.calcsize(format_pointers)*(i)))
                    block_p = struct.unpack(format_pointers,f.read(struct.calcsize(format_pointers)))
                    for j in block_p:
                        
                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*(j-1)))
                        block_unpack = struct.unpack(format_b_folder,f.read(struct.calcsize(format_b_folder)))
                        block_unpack = list(block_unpack)
                        if block_unpack[0].decode('utf-8').rstrip("\x00") == folder:
                            block_unpack[0] = self.name[0:12].encode('utf-8')
                        elif block_unpack[2].decode('utf-8').rstrip("\x00") == folder:
                            block_unpack[2] = self.name[0:12].encode('utf-8')
                        elif block_unpack[4].decode('utf-8').rstrip("\x00") == folder:
                            block_unpack[4] = self.name[0:12].encode('utf-8')
                        elif block_unpack[6].decode('utf-8').rstrip("\x00") == folder:
                            block_unpack[6] = self.name[0:12].encode('utf-8')
                        else:
                            print("No se encontro el archivo")
                            return
                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*(i)))
                        f.write(struct.pack(format_b_folder,block_unpack[0],block_unpack[1],block_unpack[2],block_unpack[3],block_unpack[4],block_unpack[5],block_unpack[6],block_unpack[7]))
                        print("Se renombro el archivo exitosamente")
                        return 
                cont += 1


from commands.login import login
from commands.mount import mount
import struct

class cat:

    def __init__(self,params):
        self.params = params
        self.paths = []
        self.execute()

    def execute(self):
        self.params = self.params[0]
        for i in self.params:
            if i[0] == "path":
                self.paths.append(i[1])
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
                    for p in self.paths:
                        f.seek(partition1[3])
                        data_sb = f.read(struct.calcsize(format_sb))
                        sb_unpack = struct.unpack(format_sb,data_sb)
                        index_inode = 0
                        inode_file = 0
                        path = p.split("/")
                        cont = 0
                        for i in path:
                            if i == "":
                                cont += 1
                                continue

                            index_inode = self.searchInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                        #print(index_inode)
                        f.seek(sb_unpack[15]+(struct.calcsize(format_i)*(index_inode-1)))
                        inode_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                        #print(inode_unpack)
                        inode_file = inode_unpack[6:22]
                        inode_file = list(inode_file)
                        print("Archivo "+path[len(path)-1]+" se va imprimir:")
                        for i in inode_file:
                            if i == -1:
                                continue
                            f.seek(sb_unpack[16]+(struct.calcsize(format_b)*(i-1)))
                            block_unpack = struct.unpack(format_b,f.read(struct.calcsize(format_b)))
                            print(block_unpack[0].decode('utf-8').rstrip("\x00"))
                elif partition2[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    for p in self.paths:
                        f.seek(partition2[3])
                        data_sb = f.read(struct.calcsize(format_sb))
                        sb_unpack = struct.unpack(format_sb,data_sb)
                        index_inode = 0
                        inode_file = 0
                        path = p.split("/")
                        cont = 0
                        for i in path:
                            if i == "":
                                cont += 1
                                continue

                            index_inode = self.searchInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                        #print(index_inode)
                        f.seek(sb_unpack[15]+(struct.calcsize(format_i)*(index_inode-1)))
                        inode_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                        #print(inode_unpack)
                        inode_file = inode_unpack[6:22]
                        inode_file = list(inode_file)
                        print("Archivo "+path[len(path)-1]+" se va imprimir:")
                        for i in inode_file:
                            if i == -1:
                                continue
                            f.seek(sb_unpack[16]+(struct.calcsize(format_b)*(i-1)))
                            block_unpack = struct.unpack(format_b,f.read(struct.calcsize(format_b)))
                            print(block_unpack[0].decode('utf-8').rstrip("\x00"))
                elif partition3[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    for p in self.paths:
                        f.seek(partition3[3])
                        data_sb = f.read(struct.calcsize(format_sb))
                        sb_unpack = struct.unpack(format_sb,data_sb)
                        index_inode = 0
                        inode_file = 0
                        path = p.split("/")
                        cont = 0
                        for i in path:
                            if i == "":
                                cont += 1
                                continue

                            index_inode = self.searchInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                        #print(index_inode)
                        f.seek(sb_unpack[15]+(struct.calcsize(format_i)*(index_inode-1)))
                        inode_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                        #print(inode_unpack)
                        inode_file = inode_unpack[6:22]
                        inode_file = list(inode_file)
                        print("Archivo "+path[len(path)-1]+" se va imprimir:")
                        for i in inode_file:
                            if i == -1:
                                continue
                            f.seek(sb_unpack[16]+(struct.calcsize(format_b)*(i-1)))
                            block_unpack = struct.unpack(format_b,f.read(struct.calcsize(format_b)))
                            print(block_unpack[0].decode('utf-8').rstrip("\x00"))
                elif partition4[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    for p in self.paths:
                        f.seek(partition4[3])
                        data_sb = f.read(struct.calcsize(format_sb))
                        sb_unpack = struct.unpack(format_sb,data_sb)
                        index_inode = 0
                        inode_file = 0
                        path = p.split("/")
                        cont = 0
                        for i in path:
                            if i == "":
                                cont += 1
                                continue

                            index_inode = self.searchInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                        #print(index_inode)
                        f.seek(sb_unpack[15]+(struct.calcsize(format_i)*(index_inode-1)))
                        inode_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                        #print(inode_unpack)
                        inode_file = inode_unpack[6:22]
                        inode_file = list(inode_file)
                        print("Archivo "+path[len(path)-1]+" se va imprimir:")
                        for i in inode_file:
                            if i == -1:
                                continue
                            f.seek(sb_unpack[16]+(struct.calcsize(format_b)*(i-1)))
                            block_unpack = struct.unpack(format_b,f.read(struct.calcsize(format_b)))
                            print(block_unpack[0].decode('utf-8').rstrip("\x00"))
                    


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
                    #print(block_unpack)
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

                
                
                        

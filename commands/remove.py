from  commands.login import login
from commands.mount import mount
import struct

class remove:
    def __init__(self,params):
        self.params = params
        self.path = ""
        self.execute()

    def execute(self):
        for i in self.params:
            if i[0] == "path":
                self.path = i[1]
        
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
                print("Removiendo ruta")
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
                    path_file = self.path.split("/")

                    cont = 0
                    for i in path_file:
                        if i == "":
                            cont += 1
                            continue
                        
                        if cont == len(path_file)-1:
                            #print(i)
                            self.removeFolderFile(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                            break
                        
                        index_inode = self.searchInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)

                       
                        cont += 1
                    return
                elif partition2[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    f.seek(partition2[3])
                    data_sb = f.read(struct.calcsize(format_sb))
                    sb_unpack = struct.unpack(format_sb,data_sb)
                    index_inode = 0
                    inode_file = 0
                    path_file = self.path.split("/")

                    cont = 0
                    for i in path_file:
                        if i == "":
                            cont += 1
                            continue
                        
                        if cont == len(path_file)-1:
                            #print(i)
                            self.removeFolderFile(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                            break
                        
                        index_inode = self.searchInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)

                       
                        cont += 1
                    return
                elif partition3[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    f.seek(partition3[3])
                    data_sb = f.read(struct.calcsize(format_sb))
                    sb_unpack = struct.unpack(format_sb,data_sb)
                    index_inode = 0
                    inode_file = 0
                    path_file = self.path.split("/")

                    cont = 0
                    for i in path_file:
                        if i == "":
                            cont += 1
                            continue
                        
                        if cont == len(path_file)-1:
                            #print(i)
                            self.removeFolderFile(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                            break
                        
                        index_inode = self.searchInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)

                       
                        cont += 1
                    return
                elif partition4[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    f.seek(partition4[3])
                    data_sb = f.read(struct.calcsize(format_sb))
                    sb_unpack = struct.unpack(format_sb,data_sb)
                    index_inode = 0
                    inode_file = 0
                    path_file = self.path.split("/")

                    cont = 0
                    for i in path_file:
                        if i == "":
                            cont += 1
                            continue
                        
                        if cont == len(path_file)-1:
                            #print(i)
                            self.removeFolderFile(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)
                            break
                        
                        index_inode = self.searchInode(sb_unpack[13],sb_unpack[14],sb_unpack[15],sb_unpack[16],sb_unpack[1],sb_unpack[2],index_inode,i)

                       
                        cont += 1

    
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
                                if block_unpack2[0].decode('utf-8').rstrip("\x00") == folder:
                                    return block_unpack2[1]
                                elif block_unpack2[2].decode('utf-8').rstrip("\x00") == folder:
                                    return block_unpack2[3]
                                elif block_unpack2[4].decode('utf-8').rstrip("\x00") == folder:
                                    return block_unpack2[5]
                                elif block_unpack2[6].decode('utf-8').rstrip("\x00") == folder:
                                    return block_unpack2[7]
                cont += 1

    def removeFolderFile(self,bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,index,folder):
        format_i = "I I I I I I 16i c I"
        format_b_folder = "12s i 12s i 12s i 12s i"
        format_pointers = "16i"
        format_b = "64s"
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
                            f.seek(start_inodes+(struct.calcsize(format_i)*(block_unpack[1]-1)))
                            position = start_inodes+(struct.calcsize(format_i)*(block_unpack[1]-1))
                            inoderemove_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                            typeInode = inoderemove_unpack[22]
                            if typeInode.decode('utf-8') == '1':
                                self.removeFile(position,start_blocks,bm_blocks,bm_inodes,block_unpack[1]-1)
                                block_unpack[0] = bytes("",'utf-8')
                                block_unpack[1] = -1
                                f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                f.write(struct.pack(format_b_folder,*block_unpack))
                                return
                            else:
                                index_block = block_unpack[1]-1
                                block_unpack[0] = bytes("",'utf-8')
                                block_unpack[1] = -1
                                f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                f.write(struct.pack(format_b_folder,*block_unpack))
                                self.removeFolder(bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,index_block,folder)
                    

                            
                        elif block_unpack[2].decode('utf-8').rstrip("\x00") == folder:
                            f.seek(start_inodes+(struct.calcsize(format_i)*(block_unpack[3]-1)))
                            position = start_inodes+(struct.calcsize(format_i)*(block_unpack[3]-1))
                            inoderemove_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                            typeInode = inoderemove_unpack[22]
                            if typeInode.decode('utf-8') == '1':
                                self.removeFile(position,start_blocks,bm_blocks,bm_inodes,block_unpack[3]-1)
                                block_unpack[2] = bytes("",'utf-8')
                                block_unpack[3] = -1
                                f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                f.write(struct.pack(format_b_folder,*block_unpack))
                                return
                            else:
                                index_block = block_unpack[3]-1
                                block_unpack[2] = bytes("",'utf-8')
                                block_unpack[3] = -1
                                f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                f.write(struct.pack(format_b_folder,*block_unpack))
                                self.removeFolder(bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,index_block,folder)
                    
                        elif block_unpack[4].decode('utf-8').rstrip("\x00") == folder:
                            f.seek(start_inodes+(struct.calcsize(format_i)*(block_unpack[5]-1)))
                            position = start_inodes+(struct.calcsize(format_i)*(block_unpack[5]-1))
                            inoderemove_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                            typeInode = inoderemove_unpack[22]
                            if typeInode.decode('utf-8') == '1':
                                self.removeFile(position,start_blocks,bm_blocks,bm_inodes,block_unpack[5]-1)
                                block_unpack[4] = bytes("",'utf-8')
                                block_unpack[5] = -1
                                f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                f.write(struct.pack(format_b_folder,*block_unpack))
                                return
                            else:
                                index_block = block_unpack[5]-1
                                block_unpack[4] = bytes("",'utf-8')
                                block_unpack[5] = -1
                                f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                f.write(struct.pack(format_b_folder,*block_unpack))
                                self.removeFolder(bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,index_block,folder)
                    
                        elif block_unpack[6].decode('utf-8').rstrip("\x00") == folder:
                            #print("ENTRO")
                            f.seek(start_inodes+(struct.calcsize(format_i)*(block_unpack[7]-1)))
                            position = start_inodes+(struct.calcsize(format_i)*(block_unpack[7]-1))
                            inoderemove_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                            typeInode = inoderemove_unpack[22]
                            if typeInode.decode('utf-8') == '1':
                                self.removeFile(position,start_blocks,bm_blocks,bm_inodes,block_unpack[7]-1)
                                block_unpack[6] = bytes("",'utf-8')
                                block_unpack[7] = -1
                                f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                f.write(struct.pack(format_b_folder,*block_unpack))
                                return
                            else:
                                index_block = block_unpack[7]-1
                                block_unpack[6] = bytes("",'utf-8')
                                block_unpack[7] = -1
                                f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                f.write(struct.pack(format_b_folder,*block_unpack))
                                self.removeFolder(bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,index_block,folder)
                    
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
                                if block_unpack2[0].decode('utf-8').rstrip("\x00") == folder:
                                    f.seek(start_inodes+(struct.calcsize(format_i)*(block_unpack2[1]-1)))
                                    position = start_inodes+(struct.calcsize(format_i)*(block_unpack2[1]-1))
                                    inoderemove_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                                    typeInode = inoderemove_unpack[22]
                                    if typeInode.decode('utf-8') == '1':
                                        self.removeFile(position,start_blocks,bm_blocks,bm_inodes,block_unpack2[1]-1)
                                        block_unpack2[0] = bytes("",'utf-8')
                                        block_unpack2[1] = -1
                                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                        f.write(struct.pack(format_b_folder,*block_unpack2))
                                        return
                                    else:
                                        index_block = block_unpack2[1]-1
                                        block_unpack2[0] = bytes("",'utf-8')
                                        block_unpack2[1] = -1
                                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                        f.write(struct.pack(format_b_folder,*block_unpack2))
                                        self.removeFolder(bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,index_block,folder)
                            

                                    
                                elif block_unpack2[2].decode('utf-8').rstrip("\x00") == folder:
                                    f.seek(start_inodes+(struct.calcsize(format_i)*(block_unpack2[3]-1)))
                                    position = start_inodes+(struct.calcsize(format_i)*(block_unpack2[3]-1))
                                    inoderemove_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                                    typeInode = inoderemove_unpack[22]
                                    if typeInode.decode('utf-8') == '1':
                                        self.removeFile(position,start_blocks,bm_blocks,bm_inodes,block_unpack2[3]-1)
                                        block_unpack2[2] = bytes("",'utf-8')
                                        block_unpack2[3] = -1
                                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                        f.write(struct.pack(format_b_folder,*block_unpack2))
                                        return
                                    else:
                                        index_block = block_unpack2[3]-1
                                        block_unpack2[2] = bytes("",'utf-8')
                                        block_unpack2[3] = -1
                                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                        f.write(struct.pack(format_b_folder,*block_unpack2))
                                        self.removeFolder(bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,index_block,folder)
                            
                                elif block_unpack2[4].decode('utf-8').rstrip("\x00") == folder:
                                    f.seek(start_inodes+(struct.calcsize(format_i)*(block_unpack2[5]-1)))
                                    position = start_inodes+(struct.calcsize(format_i)*(block_unpack2[5]-1))
                                    inoderemove_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                                    typeInode = inoderemove_unpack[22]
                                    if typeInode.decode('utf-8') == '1':
                                        self.removeFile(position,start_blocks,bm_blocks,bm_inodes,block_unpack2[5]-1)
                                        block_unpack2[4] = bytes("",'utf-8')
                                        block_unpack2[5] = -1
                                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                        f.write(struct.pack(format_b_folder,*block_unpack2))
                                        return
                                    else:
                                        index_block = block_unpack2[5]-1
                                        block_unpack2[4] = bytes("",'utf-8')
                                        block_unpack2[5] = -1
                                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                        f.write(struct.pack(format_b_folder,*block_unpack2))
                                        self.removeFolder(bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,index_block,folder)
                            
                                elif block_unpack2[6].decode('utf-8').rstrip("\x00") == folder:
                                    #print("ENTRO")
                                    f.seek(start_inodes+(struct.calcsize(format_i)*(block_unpack2[7]-1)))
                                    position = start_inodes+(struct.calcsize(format_i)*(block_unpack2[7]-1))
                                    inoderemove_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                                    typeInode = inoderemove_unpack[22]
                                    if typeInode.decode('utf-8') == '1':
                                        self.removeFile(position,start_blocks,bm_blocks,bm_inodes,block_unpack2[7]-1)
                                        block_unpack2[6] = bytes("",'utf-8')
                                        block_unpack2[7] = -1
                                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                        f.write(struct.pack(format_b_folder,*block_unpack2))
                                        return
                                    else:
                                        index_block = block_unpack2[7]-1
                                        block_unpack2[6] = bytes("",'utf-8')
                                        block_unpack2[7] = -1
                                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                        f.write(struct.pack(format_b_folder,*block_unpack2))
                                        self.removeFolder(bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,index_block,folder)
                            
                cont += 1
        
                    

    def removeFile(self,position,start_blocks,bm_blocks,bm_inodes,index):
        format_i = "I I I I I I 16i c I"
        format_b_folder = "12s i 12s i 12s i 12s i"
        format_pointers = "16i"
        format_b = "64s"
        block_p = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        with open(self.path_mount,"rb+") as f:
            f.seek(position)
            inoderemove_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
            i_block = inoderemove_unpack[6:22]
            inoderemove_unpack = list(inoderemove_unpack)
            cont = 0
            for i in i_block:
                i = i - 1
                if i != -1:
                    f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                    f.write(struct.pack(format_b,bytes("",'utf-8')))
                    f.seek(bm_blocks+i)
                    f.write(b'0')
                    inoderemove_unpack[6+cont] = -1
                    cont += 1
            f.seek(position)
            f.write(struct.pack(format_i,*inoderemove_unpack))
            f.seek(bm_inodes+index)
            f.write(b'0')
            print("Se elimino el archivo")
            
            return

            

    def removeFolder(self,bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,index,folder):
        format_i = "I I I I I I 16i c I"
        format_b_folder = "12s i 12s i 12s i 12s i"
        format_pointers = "16i"
        format_b = "64s"
        block_p = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        with open(self.path_mount,"rb+") as f:
            f.seek(start_inodes+(struct.calcsize(format_i)*index))
            inode_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
            i_block = inode_unpack[6:22]
            inode_unpack = list(inode_unpack)
            cont = 0
            for i in i_block:
                i = i - 1
                if i != -1:
                    if cont < 13:
                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                        block = struct.unpack(format_b_folder,f.read(struct.calcsize(format_b_folder)))
                        block = list(block)
                        if block[1] != -1 and block[1] != 0:
                            f.seek(start_inodes+(struct.calcsize(format_i)*(block[1]-1)))
                            inoderemove_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                            typeInode = inoderemove_unpack[22]
                            if typeInode.decode('utf-8') == '1':
                                self.removeFile(start_inodes+(struct.calcsize(format_i)*(block[1]-1)),start_blocks,bm_blocks,bm_inodes,block[1]-1)
                            else:
                                self.removeFolder(bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,block[1]-1,folder)
                        if block[3] != -1 and block[3] != 0:
                            f.seek(start_inodes+(struct.calcsize(format_i)*(block[3]-1)))
                            inoderemove_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                            typeInode = inoderemove_unpack[22]
                            if typeInode.decode('utf-8') == '1':
                                self.removeFile(start_inodes+(struct.calcsize(format_i)*(block[3]-1)),start_blocks,bm_blocks,bm_inodes,block[3]-1)
                            else:
                                self.removeFolder(bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,block[3]-1,folder)
                        if block[5] != -1 and block[5] != 0:
                            f.seek(start_inodes+(struct.calcsize(format_i)*(block[5]-1)))
                            inoderemove_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                            typeInode = inoderemove_unpack[22]
                            if typeInode.decode('utf-8') == '1':
                                self.removeFile(start_inodes+(struct.calcsize(format_i)*(block[5]-1)),start_blocks,bm_blocks,bm_inodes,block[5]-1)
                            else:
                                self.removeFolder(bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,block[5]-1,folder)
                        if block[7] != -1 and block[7] != 0:
                            f.seek(start_inodes+(struct.calcsize(format_i)*(block[7]-1)))
                            inoderemove_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                            typeInode = inoderemove_unpack[22]
                            if typeInode.decode('utf-8') == '1':
                                self.removeFile(start_inodes+(struct.calcsize(format_i)*(block[7]-1)),start_blocks,bm_blocks,bm_inodes,block[7]-1)
                            else:
                                self.removeFolder(bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,block[7]-1,folder)
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
                                if block_unpack2[0].decode('utf-8').rstrip("\x00") == folder:
                                    f.seek(start_inodes+(struct.calcsize(format_i)*(block_unpack2[1]-1)))
                                    position = start_inodes+(struct.calcsize(format_i)*(block_unpack2[1]-1))
                                    inoderemove_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                                    typeInode = inoderemove_unpack[22]
                                    if typeInode.decode('utf-8') == '1':
                                        self.removeFile(position,start_blocks,bm_blocks,bm_inodes,block_unpack2[1]-1)
                                        block_unpack2[0] = bytes("",'utf-8')
                                        block_unpack2[1] = -1
                                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                        f.write(struct.pack(format_b_folder,*block_unpack2))
                                        return
                                    else:
                                        index_block = block_unpack2[1]-1
                                        block_unpack2[0] = bytes("",'utf-8')
                                        block_unpack2[1] = -1
                                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                        f.write(struct.pack(format_b_folder,*block_unpack2))
                                        self.removeFolder(bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,index_block,folder)
                            

                                    
                                elif block_unpack2[2].decode('utf-8').rstrip("\x00") == folder:
                                    f.seek(start_inodes+(struct.calcsize(format_i)*(block_unpack2[3]-1)))
                                    position = start_inodes+(struct.calcsize(format_i)*(block_unpack2[3]-1))
                                    inoderemove_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                                    typeInode = inoderemove_unpack[22]
                                    if typeInode.decode('utf-8') == '1':
                                        self.removeFile(position,start_blocks,bm_blocks,bm_inodes,block_unpack2[3]-1)
                                        block_unpack2[2] = bytes("",'utf-8')
                                        block_unpack2[3] = -1
                                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                        f.write(struct.pack(format_b_folder,*block_unpack2))
                                        return
                                    else:
                                        index_block = block_unpack2[3]-1
                                        block_unpack2[2] = bytes("",'utf-8')
                                        block_unpack2[3] = -1
                                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                        f.write(struct.pack(format_b_folder,*block_unpack2))
                                        self.removeFolder(bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,index_block,folder)
                            
                                elif block_unpack2[4].decode('utf-8').rstrip("\x00") == folder:
                                    f.seek(start_inodes+(struct.calcsize(format_i)*(block_unpack2[5]-1)))
                                    position = start_inodes+(struct.calcsize(format_i)*(block_unpack2[5]-1))
                                    inoderemove_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                                    typeInode = inoderemove_unpack[22]
                                    if typeInode.decode('utf-8') == '1':
                                        self.removeFile(position,start_blocks,bm_blocks,bm_inodes,block_unpack2[5]-1)
                                        block_unpack2[4] = bytes("",'utf-8')
                                        block_unpack2[5] = -1
                                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                        f.write(struct.pack(format_b_folder,*block_unpack2))
                                        return
                                    else:
                                        index_block = block_unpack2[5]-1
                                        block_unpack2[4] = bytes("",'utf-8')
                                        block_unpack2[5] = -1
                                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                        f.write(struct.pack(format_b_folder,*block_unpack2))
                                        self.removeFolder(bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,index_block,folder)
                            
                                elif block_unpack2[6].decode('utf-8').rstrip("\x00") == folder:
                                    #print("ENTRO")
                                    f.seek(start_inodes+(struct.calcsize(format_i)*(block_unpack2[7]-1)))
                                    position = start_inodes+(struct.calcsize(format_i)*(block_unpack2[7]-1))
                                    inoderemove_unpack = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                                    typeInode = inoderemove_unpack[22]
                                    if typeInode.decode('utf-8') == '1':
                                        self.removeFile(position,start_blocks,bm_blocks,bm_inodes,block_unpack2[7]-1)
                                        block_unpack2[6] = bytes("",'utf-8')
                                        block_unpack2[7] = -1
                                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                        f.write(struct.pack(format_b_folder,*block_unpack2))
                                        return
                                    else:
                                        index_block = block_unpack2[7]-1
                                        block_unpack2[6] = bytes("",'utf-8')
                                        block_unpack2[7] = -1
                                        f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                                        f.write(struct.pack(format_b_folder,*block_unpack2))
                                        self.removeFolder(bm_inodes,bm_blocks,start_inodes,start_blocks,inode_size,block_size,index_block,folder)
                            

                    f.seek(start_blocks+(struct.calcsize(format_b_folder)*i))
                    f.write(struct.pack(format_b,bytes("",'utf-8')))
                    f.seek(bm_blocks+i)
                    f.write(b'0')
                    inode_unpack[6+cont] = -1
            cont += 1
            f.seek(start_inodes+(struct.calcsize(format_i)*index))
            f.write(struct.pack(format_i,*inode_unpack))
            f.seek(bm_inodes+index)
            f.write(b'0')
            print("Se elimino la carpeta")
            return
        







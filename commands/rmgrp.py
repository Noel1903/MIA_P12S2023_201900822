from  commands.login import login
from commands.mount import mount
import struct

class rmgrp:
    def __init__(self,params):
        self.params = params
        self.name = ""
        self.execute()

    def execute(self):
        if self.params[0][0] == "name":
            self.name = self.params[0][1]
        else:
            print("Parametros incorrectos para el comando rmgrp.")

        log = login(None)
        id = log.getId()[len(log.getId())-1]
        userlogued = log.getUserLogued()[len(log.getUserLogued())-1]
        user = log.getUser()[len(log.getUser())-1]
        #print(id,userlogued,user)
        if userlogued and id!= "" and user =="root":
            print("Eliminando grupo")
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
            
            path_mount = part_m.path
            with open(path_mount,"rb+") as f:
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
                    inode_start = sb_unpack[15] + struct.calcsize(format_i)
                    block_start = sb_unpack[16]
                    f.seek(inode_start)
                    inode_user_unpacked = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                    #print(inode_user_unpacked)
                    i_block = inode_user_unpacked[6:22]

                    users_txt = ""
                    for i in i_block:
                        if i != -1:
                            f.seek(block_start + (struct.calcsize(format_b_folder)*(i-1)))
                            users_unpacked = struct.unpack(format_b,f.read(struct.calcsize(format_b)))
                            users_unpacked = list(users_unpacked)
                            users_txt += users_unpacked[0].decode('utf-8').rstrip("\x00")
                    new_users_txt = ""
                    
                    users_txt = users_txt.split("\n")
                    for i in users_txt:
                        content = i.split(",")
                        if len(content) == 3:
                            if content[2] == self.name:
                                content[0] = "0"
                                
                        
                        for j in content:
                            new_users_txt += j + ","
                        new_users_txt = new_users_txt[:len(new_users_txt)-1]
                        new_users_txt += "\n"
                    new_users_txt = new_users_txt[:len(new_users_txt)-1]

                    i_block = list(i_block)
                    cont = 0
                    if len(new_users_txt) <=64:
                        i = i_block[cont]
                        f.seek(block_start + (struct.calcsize(format_b_folder)*(i-1)))
                        f.write(struct.pack(format_b,new_users_txt.encode('utf-8')))
                    else:
                        while len(new_users_txt) > 64:
                            i = i_block[cont]
                            f.seek(block_start + (struct.calcsize(format_b_folder)*(i-1)))
                            f.write(struct.pack(format_b,new_users_txt[:64].encode('utf-8')))
                            new_users_txt = new_users_txt[64:]
                            cont += 1
                            i = i_block[cont]
                            f.seek(block_start + (struct.calcsize(format_b_folder)*(i-1)))
                            f.write(struct.pack(format_b,new_users_txt.encode('utf-8')))
                            
                    print("Grupo eliminado")
                elif partition2[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    f.seek(partition2[3])
                    data_sb = f.read(struct.calcsize(format_sb))
                    sb_unpack = struct.unpack(format_sb,data_sb)
                    inode_start = sb_unpack[15] + struct.calcsize(format_i)
                    block_start = sb_unpack[16]
                    f.seek(inode_start)
                    inode_user_unpacked = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                    #print(inode_user_unpacked)
                    i_block = inode_user_unpacked[6:22]

                    users_txt = ""
                    for i in i_block:
                        if i != -1:
                            f.seek(block_start + (struct.calcsize(format_b_folder)*(i-1)))
                            users_unpacked = struct.unpack(format_b,f.read(struct.calcsize(format_b)))
                            users_unpacked = list(users_unpacked)
                            users_txt += users_unpacked[0].decode('utf-8').rstrip("\x00")
                    new_users_txt = ""
                    
                    users_txt = users_txt.split("\n")
                    for i in users_txt:
                        content = i.split(",")
                        if len(content) == 3:
                            if content[2] == self.name:
                                content[0] = "0"
                                
                        
                        for j in content:
                            new_users_txt += j + ","
                        new_users_txt = new_users_txt[:len(new_users_txt)-1]
                        new_users_txt += "\n"
                    new_users_txt = new_users_txt[:len(new_users_txt)-1]

                    i_block = list(i_block)
                    cont = 0
                    if len(new_users_txt) <=64:
                        i = i_block[cont]
                        f.seek(block_start + (struct.calcsize(format_b_folder)*(i-1)))
                        f.write(struct.pack(format_b,new_users_txt.encode('utf-8')))
                    else:
                        while len(new_users_txt) > 64:
                            i = i_block[cont]
                            f.seek(block_start + (struct.calcsize(format_b_folder)*(i-1)))
                            f.write(struct.pack(format_b,new_users_txt[:64].encode('utf-8')))
                            new_users_txt = new_users_txt[64:]
                            cont += 1
                            i = i_block[cont]
                            f.seek(block_start + (struct.calcsize(format_b_folder)*(i-1)))
                            f.write(struct.pack(format_b,new_users_txt.encode('utf-8')))
                            
                    print("Grupo eliminado")
                elif partition3[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    f.seek(partition3[3])
                    data_sb = f.read(struct.calcsize(format_sb))
                    sb_unpack = struct.unpack(format_sb,data_sb)
                    inode_start = sb_unpack[15] + struct.calcsize(format_i)
                    block_start = sb_unpack[16]
                    f.seek(inode_start)
                    inode_user_unpacked = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                    #print(inode_user_unpacked)
                    i_block = inode_user_unpacked[6:22]

                    users_txt = ""
                    for i in i_block:
                        if i != -1:
                            f.seek(block_start + (struct.calcsize(format_b_folder)*(i-1)))
                            users_unpacked = struct.unpack(format_b,f.read(struct.calcsize(format_b)))
                            users_unpacked = list(users_unpacked)
                            users_txt += users_unpacked[0].decode('utf-8').rstrip("\x00")
                    new_users_txt = ""
                    
                    users_txt = users_txt.split("\n")
                    for i in users_txt:
                        content = i.split(",")
                        if len(content) == 3:
                            if content[2] == self.name:
                                content[0] = "0"
                                
                        
                        for j in content:
                            new_users_txt += j + ","
                        new_users_txt = new_users_txt[:len(new_users_txt)-1]
                        new_users_txt += "\n"
                    new_users_txt = new_users_txt[:len(new_users_txt)-1]

                    i_block = list(i_block)
                    cont = 0
                    if len(new_users_txt) <=64:
                        i = i_block[cont]
                        f.seek(block_start + (struct.calcsize(format_b_folder)*(i-1)))
                        f.write(struct.pack(format_b,new_users_txt.encode('utf-8')))
                    else:
                        while len(new_users_txt) > 64:
                            i = i_block[cont]
                            f.seek(block_start + (struct.calcsize(format_b_folder)*(i-1)))
                            f.write(struct.pack(format_b,new_users_txt[:64].encode('utf-8')))
                            new_users_txt = new_users_txt[64:]
                            cont += 1
                            i = i_block[cont]
                            f.seek(block_start + (struct.calcsize(format_b_folder)*(i-1)))
                            f.write(struct.pack(format_b,new_users_txt.encode('utf-8')))
                            
                    print("Grupo eliminado")
                elif partition4[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    f.seek(partition4[3])
                    data_sb = f.read(struct.calcsize(format_sb))
                    sb_unpack = struct.unpack(format_sb,data_sb)
                    inode_start = sb_unpack[15] + struct.calcsize(format_i)
                    block_start = sb_unpack[16]
                    f.seek(inode_start)
                    inode_user_unpacked = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                    #print(inode_user_unpacked)
                    i_block = inode_user_unpacked[6:22]

                    users_txt = ""
                    for i in i_block:
                        if i != -1:
                            f.seek(block_start + (struct.calcsize(format_b_folder)*(i-1)))
                            users_unpacked = struct.unpack(format_b,f.read(struct.calcsize(format_b)))
                            users_unpacked = list(users_unpacked)
                            users_txt += users_unpacked[0].decode('utf-8').rstrip("\x00")
                    new_users_txt = ""
                    
                    users_txt = users_txt.split("\n")
                    for i in users_txt:
                        content = i.split(",")
                        if len(content) == 3:
                            if content[2] == self.name:
                                content[0] = "0"
                                
                        
                        for j in content:
                            new_users_txt += j + ","
                        new_users_txt = new_users_txt[:len(new_users_txt)-1]
                        new_users_txt += "\n"
                    new_users_txt = new_users_txt[:len(new_users_txt)-1]

                    i_block = list(i_block)
                    cont = 0
                    if len(new_users_txt) <=64:
                        i = i_block[cont]
                        f.seek(block_start + (struct.calcsize(format_b_folder)*(i-1)))
                        f.write(struct.pack(format_b,new_users_txt.encode('utf-8')))
                    else:
                        while len(new_users_txt) > 64:
                            i = i_block[cont]
                            f.seek(block_start + (struct.calcsize(format_b_folder)*(i-1)))
                            f.write(struct.pack(format_b,new_users_txt[:64].encode('utf-8')))
                            new_users_txt = new_users_txt[64:]
                            cont += 1
                            i = i_block[cont]
                            f.seek(block_start + (struct.calcsize(format_b_folder)*(i-1)))
                            f.write(struct.pack(format_b,new_users_txt.encode('utf-8')))
                            
                    print("Grupo eliminado")
                        
                        

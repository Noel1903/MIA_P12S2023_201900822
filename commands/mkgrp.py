from  commands.login import login
from commands.mount import mount
import struct
class mkgrp:
    def __init__(self,params = None):
        self.params = params
        self.name = ""
        if params != None:
            self.execute()

    def execute(self):
        for i in self.params:
            if i[0] == "name":
                self.name = i[1]
        log = login(None)
        id = log.getId()[len(log.getId())-1]
        userlogued = log.getUserLogued()[len(log.getUserLogued())-1]
        user = log.getUser()[len(log.getUser())-1]
        print(id,userlogued,user)
        if userlogued and id!= "" and user =="root":
            print("Creando grupo")
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
                    i_block = inode_user_unpacked[6:21]
                    users_txt = ""
                    idG = 0
                    block_count = 0
                    users_txt01 = []
                    for i in i_block:
                        f.seek(block_start + ((i-1) * struct.calcsize(format_b)))
                        if i != -1:
                            #part = struct.unpack(format_b,f.read(struct.calcsize(format_b)))[0].decode('utf-8').rstrip("\x00")
                            
                            users_txt += struct.unpack(format_b,f.read(struct.calcsize(format_b)))[0].decode('utf-8').rstrip("\x00")
                            
                            
                            users_txt01 = users_txt.split("\n")
                            users_txt01 = users_txt01[:-1]
                            user = ""

                            print(users_txt01)
                            block_count = i
                        else:
                            print("block_count",block_count)
                            break
                    for j in users_txt01:
                        user = j.split(",")
                        if len(user) == 3:
                            #print(user)
                            idG = int(user[0])
                            if user[2].rstrip("\x00") == self.name:
                                print("El grupo ya existe")
                                return  
                    f.seek(block_start + ((block_count-1) * struct.calcsize(format_b)))       
                    users_txt = struct.unpack(format_b,f.read(struct.calcsize(format_b)))[0].decode('utf-8').rstrip("\x00")
                    sizeP = len(users_txt)
                    print(users_txt)
                    addGroup = str(idG+1)+",G,"+self.name+"\n"
                    if sizeP + len(addGroup)<=64:
                        users_txt += addGroup
                        users_txt = users_txt.encode('utf-8')
                        #users_txt += b"\x00" * (64 - len(users_txt))
                        f.seek(block_start + ((block_count-1) * struct.calcsize(format_b)))
                        f.write(struct.pack(format_b,users_txt))
                        print("Grupo creado")
                        f.close()
                        return
                    else:
                        addGroupN = ""
                        for i in addGroup:
                            sizeP += 1
                            if sizeP > 64:
                                addGroupN += str(i)
                            else:
                                f.seek(block_start + ((block_count-1) * struct.calcsize(format_b)))
                                
                                users_txt += i
                                users_txt02 = users_txt.encode('utf-8')
                                #users_txt02 += b"\x00" * (64 - len(users_txt))
                                f.write(struct.pack(format_b,users_txt02))

                        count  = 0
                        block_count += 1
                        f.seek(inode_start)
                        inode_user_unpacked = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                        inode_user_unpacked = list(inode_user_unpacked)
                        for i in i_block:
                            if i == -1:
                                inode_user_unpacked[6+count] = block_count
                                f.seek(inode_start)
                                f.write(struct.pack(format_i,*inode_user_unpacked))
                                f.seek(block_start + ((block_count-1) * struct.calcsize(format_b)))
                                users_txt = addGroupN
                                users_txt = users_txt.encode('utf-8')
                                #users_txt += b"\x00" * (64 - len(users_txt))
                                f.write(struct.pack(format_b,users_txt))
                                #print(inode_user_unpacked)
                                f.seek(sb_unpack[14]+block_count-1)
                                f.write(b'1')
                                print("Grupo creado")
                                f.close()
                                return
                            count += 1
                        return     
                elif partition2[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    f.seek(partition2[3])
                    data_sb = f.read(struct.calcsize(format_sb))
                    sb_unpack = struct.unpack(format_sb,data_sb)
                    inode_start = sb_unpack[15] + struct.calcsize(format_i)
                    block_start = sb_unpack[16]
                    f.seek(inode_start)
                    inode_user_unpacked = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                    #print(inode_user_unpacked)
                    i_block = inode_user_unpacked[6:21]
                    users_txt = ""
                    idG = 0
                    block_count = 0
                    users_txt01 = []
                    for i in i_block:
                        f.seek(block_start + ((i-1) * struct.calcsize(format_b)))
                        if i != -1:
                            #part = struct.unpack(format_b,f.read(struct.calcsize(format_b)))[0].decode('utf-8').rstrip("\x00")
                            
                            users_txt += struct.unpack(format_b,f.read(struct.calcsize(format_b)))[0].decode('utf-8').rstrip("\x00")
                            
                            
                            users_txt01 = users_txt.split("\n")
                            users_txt01 = users_txt01[:-1]
                            user = ""

                            print(users_txt01)
                            block_count = i
                        else:
                            print("block_count",block_count)
                            break
                    for j in users_txt01:
                        user = j.split(",")
                        if len(user) == 3:
                            #print(user)
                            idG = int(user[0])
                            if user[2].rstrip("\x00") == self.name:
                                print("El grupo ya existe")
                                return  
                    f.seek(block_start + ((block_count-1) * struct.calcsize(format_b)))       
                    users_txt = struct.unpack(format_b,f.read(struct.calcsize(format_b)))[0].decode('utf-8').rstrip("\x00")
                    sizeP = len(users_txt)
                    print(users_txt)
                    addGroup = str(idG+1)+",G,"+self.name+"\n"
                    if sizeP + len(addGroup)<=64:
                        users_txt += addGroup
                        users_txt = users_txt.encode('utf-8')
                        #users_txt += b"\x00" * (64 - len(users_txt))
                        f.seek(block_start + ((block_count-1) * struct.calcsize(format_b)))
                        f.write(struct.pack(format_b,users_txt))
                        print("Grupo creado")
                        f.close()
                        return
                    else:
                        addGroupN = ""
                        for i in addGroup:
                            sizeP += 1
                            if sizeP > 64:
                                addGroupN += str(i)
                            else:
                                f.seek(block_start + ((block_count-1) * struct.calcsize(format_b)))
                                
                                users_txt += i
                                users_txt02 = users_txt.encode('utf-8')
                                #users_txt02 += b"\x00" * (64 - len(users_txt))
                                f.write(struct.pack(format_b,users_txt02))

                        count  = 0
                        block_count += 1
                        f.seek(inode_start)
                        inode_user_unpacked = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                        inode_user_unpacked = list(inode_user_unpacked)
                        for i in i_block:
                            if i == -1:
                                inode_user_unpacked[6+count] = block_count
                                f.seek(inode_start)
                                f.write(struct.pack(format_i,*inode_user_unpacked))
                                f.seek(block_start + ((block_count-1) * struct.calcsize(format_b)))
                                users_txt = addGroupN
                                users_txt = users_txt.encode('utf-8')
                                #users_txt += b"\x00" * (64 - len(users_txt))
                                f.write(struct.pack(format_b,users_txt))
                                #print(inode_user_unpacked)
                                f.seek(sb_unpack[14]+block_count-1)
                                f.write(b'1')
                                print("Grupo creado")
                                f.close()
                                return
                            count += 1
                        return     
                elif partition3[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    f.seek(partition3[3])
                    data_sb = f.read(struct.calcsize(format_sb))
                    sb_unpack = struct.unpack(format_sb,data_sb)
                    inode_start = sb_unpack[15] + struct.calcsize(format_i)
                    block_start = sb_unpack[16]
                    f.seek(inode_start)
                    inode_user_unpacked = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                    #print(inode_user_unpacked)
                    i_block = inode_user_unpacked[6:21]
                    users_txt = ""
                    idG = 0
                    block_count = 0
                    users_txt01 = []
                    for i in i_block:
                        f.seek(block_start + ((i-1) * struct.calcsize(format_b)))
                        if i != -1:
                            #part = struct.unpack(format_b,f.read(struct.calcsize(format_b)))[0].decode('utf-8').rstrip("\x00")
                            
                            users_txt += struct.unpack(format_b,f.read(struct.calcsize(format_b)))[0].decode('utf-8').rstrip("\x00")
                            
                            
                            users_txt01 = users_txt.split("\n")
                            users_txt01 = users_txt01[:-1]
                            user = ""

                            print(users_txt01)
                            block_count = i
                        else:
                            print("block_count",block_count)
                            break
                    for j in users_txt01:
                        user = j.split(",")
                        if len(user) == 3:
                            #print(user)
                            idG = int(user[0])
                            if user[2].rstrip("\x00") == self.name:
                                print("El grupo ya existe")
                                return  
                    f.seek(block_start + ((block_count-1) * struct.calcsize(format_b)))       
                    users_txt = struct.unpack(format_b,f.read(struct.calcsize(format_b)))[0].decode('utf-8').rstrip("\x00")
                    sizeP = len(users_txt)
                    print(users_txt)
                    addGroup = str(idG+1)+",G,"+self.name+"\n"
                    if sizeP + len(addGroup)<=64:
                        users_txt += addGroup
                        users_txt = users_txt.encode('utf-8')
                        #users_txt += b"\x00" * (64 - len(users_txt))
                        f.seek(block_start + ((block_count-1) * struct.calcsize(format_b)))
                        f.write(struct.pack(format_b,users_txt))
                        print("Grupo creado")
                        f.close()
                        return
                    else:
                        addGroupN = ""
                        for i in addGroup:
                            sizeP += 1
                            if sizeP > 64:
                                addGroupN += str(i)
                            else:
                                f.seek(block_start + ((block_count-1) * struct.calcsize(format_b)))
                                
                                users_txt += i
                                users_txt02 = users_txt.encode('utf-8')
                                #users_txt02 += b"\x00" * (64 - len(users_txt))
                                f.write(struct.pack(format_b,users_txt02))

                        count  = 0
                        block_count += 1
                        f.seek(inode_start)
                        inode_user_unpacked = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                        inode_user_unpacked = list(inode_user_unpacked)
                        for i in i_block:
                            if i == -1:
                                inode_user_unpacked[6+count] = block_count
                                f.seek(inode_start)
                                f.write(struct.pack(format_i,*inode_user_unpacked))
                                f.seek(block_start + ((block_count-1) * struct.calcsize(format_b)))
                                users_txt = addGroupN
                                users_txt = users_txt.encode('utf-8')
                                #users_txt += b"\x00" * (64 - len(users_txt))
                                f.write(struct.pack(format_b,users_txt))
                                #print(inode_user_unpacked)
                                f.seek(sb_unpack[14]+block_count-1)
                                f.write(b'1')
                                print("Grupo creado")
                                f.close()
                                return
                            count += 1
                        return     
                elif partition4[5].decode('utf-8').rstrip("\x00") == part_m.name_partition:
                    f.seek(partition4[3])
                    data_sb = f.read(struct.calcsize(format_sb))
                    sb_unpack = struct.unpack(format_sb,data_sb)
                    inode_start = sb_unpack[15] + struct.calcsize(format_i)
                    block_start = sb_unpack[16]
                    f.seek(inode_start)
                    inode_user_unpacked = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                    #print(inode_user_unpacked)
                    i_block = inode_user_unpacked[6:21]
                    users_txt = ""
                    idG = 0
                    block_count = 0
                    users_txt01 = []
                    for i in i_block:
                        f.seek(block_start + ((i-1) * struct.calcsize(format_b)))
                        if i != -1:
                            #part = struct.unpack(format_b,f.read(struct.calcsize(format_b)))[0].decode('utf-8').rstrip("\x00")
                            
                            users_txt += struct.unpack(format_b,f.read(struct.calcsize(format_b)))[0].decode('utf-8').rstrip("\x00")
                            
                            
                            users_txt01 = users_txt.split("\n")
                            users_txt01 = users_txt01[:-1]
                            user = ""

                            print(users_txt01)
                            block_count = i
                        else:
                            print("block_count",block_count)
                            break
                    for j in users_txt01:
                        user = j.split(",")
                        if len(user) == 3:
                            #print(user)
                            idG = int(user[0])
                            if user[2].rstrip("\x00") == self.name:
                                print("El grupo ya existe")
                                return  
                    f.seek(block_start + ((block_count-1) * struct.calcsize(format_b)))       
                    users_txt = struct.unpack(format_b,f.read(struct.calcsize(format_b)))[0].decode('utf-8').rstrip("\x00")
                    sizeP = len(users_txt)
                    print(users_txt)
                    addGroup = str(idG+1)+",G,"+self.name+"\n"
                    if sizeP + len(addGroup)<=64:
                        users_txt += addGroup
                        users_txt = users_txt.encode('utf-8')
                        #users_txt += b"\x00" * (64 - len(users_txt))
                        f.seek(block_start + ((block_count-1) * struct.calcsize(format_b)))
                        f.write(struct.pack(format_b,users_txt))
                        print("Grupo creado")
                        f.close()
                        return
                    else:
                        addGroupN = ""
                        for i in addGroup:
                            sizeP += 1
                            if sizeP > 64:
                                addGroupN += str(i)
                            else:
                                f.seek(block_start + ((block_count-1) * struct.calcsize(format_b)))
                                
                                users_txt += i
                                users_txt02 = users_txt.encode('utf-8')
                                #users_txt02 += b"\x00" * (64 - len(users_txt))
                                f.write(struct.pack(format_b,users_txt02))

                        count  = 0
                        block_count += 1
                        f.seek(inode_start)
                        inode_user_unpacked = struct.unpack(format_i,f.read(struct.calcsize(format_i)))
                        inode_user_unpacked = list(inode_user_unpacked)
                        for i in i_block:
                            if i == -1:
                                inode_user_unpacked[6+count] = block_count
                                f.seek(inode_start)
                                f.write(struct.pack(format_i,*inode_user_unpacked))
                                f.seek(block_start + ((block_count-1) * struct.calcsize(format_b)))
                                users_txt = addGroupN
                                users_txt = users_txt.encode('utf-8')
                                #users_txt += b"\x00" * (64 - len(users_txt))
                                f.write(struct.pack(format_b,users_txt))
                                #print(inode_user_unpacked)
                                f.seek(sb_unpack[14]+block_count-1)
                                f.write(b'1')
                                print("Grupo creado")
                                f.close()
                                return
                            count += 1
                        return                
                    
        return
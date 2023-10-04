from commands.mount import mount
import struct
class login:

    userlogued = [False]
    id_disk = []
    userlog = []
    def __init__(self,params = None):
        self.params = params
        if params != None:
            self.execute()
            self.userlogued = False
            
            self.user = ""
            self.password = ""
            self.id = ""

    def setUserLogued(self):
        self.userlogued = [False]

    def getUser(self):
        return self.userlog

    def getUserLogued(self):
        return self.userlogued
    
    def getId(self):
        return self.id_disk

    def execute(self):
        for i in self.params:
            if i[0] == "user":
                self.user = i[1]
            elif i[0] == "pass":
                self.password = str(i[1])
            elif i[0] == "id":
                self.id = i[1]

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
            if i.part_id.rstrip("\x00") == self.id:
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
                    f.seek(block_start + ((i-1) * struct.calcsize(format_b)))
                    if i != -1:
                        users_txt += struct.unpack(format_b,f.read(struct.calcsize(format_b)))[0].decode('utf-8').rstrip("\x00")
                users_txt = users_txt.split("\n")
                users_txt = users_txt[1:-1]
                exist = False
                for i in users_txt:
                    user = i.split(",")
                    if len(user) == 5:
                        #print(user[3],self.user,user[4],self.password)
                        if user[3].rstrip("\x00") == self.user and user[4].rstrip("\x00") == self.password:
                            #print("Login de ",self.user,"exitoso")
                            self.userlogued[0] = True
                            self.userlog.append(self.user)
                            self.id_disk.append(self.id)
                            f.close()
                            return {"status","true"}
                if exist == False:
                    #print("Usuario o contraseña incorrectos")
                    f.close()
                    return {"status","false"}                   
                f.close()
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
                    f.seek(block_start + ((i-1) * struct.calcsize(format_b)))
                    if i != -1:
                        users_txt += struct.unpack(format_b,f.read(struct.calcsize(format_b)))[0].decode('utf-8').rstrip("\x00")
                users_txt = users_txt.split("\n")
                users_txt = users_txt[:-1]
                exist = False
                for i in users_txt:
                    user = i.split(",")
                    if len(user) == 5:
                        #print(user[3],self.user,user[4],self.password)
                        if user[3].rstrip("\x00") == self.user and user[4].rstrip("\x00") == self.password:
                            print("Login de ",self.user,"exitoso")
                            self.userlogued[0] = True
                            self.userlog.append(self.user)
                            self.id_disk.append(self.id)
                            f.close()
                            return
                if exist == False:
                    print("Usuario o contraseña incorrectos")
                    f.close()
                    return                    
                f.close()
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
                    f.seek(block_start + ((i-1) * struct.calcsize(format_b)))
                    if i != -1:
                        users_txt += struct.unpack(format_b,f.read(struct.calcsize(format_b)))[0].decode('utf-8').rstrip("\x00")
                users_txt = users_txt.split("\n")
                users_txt = users_txt[1:-1]
                exist = False
                for i in users_txt:
                    user = i.split(",")
                    if len(user) == 5:
                        #print(user[3],self.user,user[4],self.password)
                        if user[3].rstrip("\x00") == self.user and user[4].rstrip("\x00") == self.password:
                            print("Login de ",self.user,"exitoso")
                            self.userlogued = True
                            f.close()
                            return
                if exist == False:
                    print("Usuario o contraseña incorrectos")
                    f.close()
                    return                    
                f.close()
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
                    f.seek(block_start + ((i-1) * struct.calcsize(format_b)))
                    if i != -1:
                        users_txt += struct.unpack(format_b,f.read(struct.calcsize(format_b)))[0].decode('utf-8').rstrip("\x00")
                users_txt = users_txt.split("\n")
                users_txt = users_txt[1:-1]
                exist = False
                for i in users_txt:
                    user = i.split(",")
                    if len(user) == 5:
                        #print(user[3],self.user,user[4],self.password)
                        if user[3].rstrip("\x00") == self.user and user[4].rstrip("\x00") == self.password:
                            print("Login de ",self.user,"exitoso")
                            self.userlogued = True
                            f.close()
                            return
                if exist == False:
                    print("Usuario o contraseña incorrectos")
                    f.close()
                    return                    
                f.close()
            return
        

   


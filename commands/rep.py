from commands.mount import mount
import struct,os,sys,subprocess
class rep:

    def __init__(self,params):
        self.params = params
        self.name = ""
        self.path = ""
        self.id = ""
        self.route = ""
        self.path_mount = ""
        self.nameDisk = ""
        self.execute()

    def execute(self):
        for i in self.params:
            if i[0] == "name":
                self.name = i[1].lower()
            elif i[0] == "path":
                self.path = i[1].replace(" ",r"\ ")
            elif i[0] == "id":
                self.id = i[1]
            elif i[0] == "route":
                self.route = i[1]
            else:
                print("Error: parametro invalido " + i[0])
                return
        
        if self.name == "":
            print("Error: falta parametro name")
            return
        if self.path == "":
            print("Error: falta parametro path")
            return
        if self.id == "":
            print("Error: falta parametro id")
            return
        
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
        
        self.path_mount = part_m.path
        self.nameDisk = part_m.nameDisk
        
        if self.name == "mbr":
            self.repMBR()
        elif self.name == "disk":
            self.repDisk()
        elif self.name == "inode":
            self.repInode(part_m.name_partition)
        elif self.name == "block":
            self.repBlock(part_m.name_partition)
        elif self.name == "bm_inode":
            self.repBM_Inode(part_m.name_partition)
        elif self.name == "bm_block":
            self.repBM_Block(part_m.name_partition)
        elif self.name == "tree":
            self.repTree(part_m.name_partition)


    def repMBR(self):
        report = ""
        report += "digraph G{\n"
        report += "node[shape=plaintext]\n"
        report += "graph[label=<\n"
        report += "<table border='1' cellborder='1' cellspacing='0'>\n"
        format_mbr = "I I I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
        format_ebr = "c c I I i 16s"
        with open(self.path_mount, "rb+") as f:
            f.seek(0)
            mbr_pack = f.read(struct.calcsize(format_mbr))
            mbr_unpack = struct.unpack(format_mbr,mbr_pack)
            report += "<tr><td colspan='2' bgcolor='#9F4AFF'><b>MBR</b></td></tr>\n"
            report += "<tr><td><b>mbr_tamaño</b></td><td>" + str(mbr_unpack[0]) + "</td></tr>\n"
            report += "<tr><td><b>mbr_fecha_creacion</b></td><td>" + str(mbr_unpack[1]) + "</td></tr>\n"
            report += "<tr><td><b>mbr_disk_signature</b></td><td>" + str(mbr_unpack[2]) + "</td></tr>\n"
            partition1 = mbr_unpack[4:10]
            partition2 = mbr_unpack[10:16]
            partition3 = mbr_unpack[16:22]
            partition4 = mbr_unpack[22:28]
            report += "<tr><td colspan='2' bgcolor='#9F4AFF'><b>Particion 1</b></td></tr>\n"
            report += "<tr><td><b>part_status</b></td><td>" + str(partition1[0].decode('utf-8')) + "</td></tr>\n"
            report += "<tr><td><b>part_type</b></td><td>" + str(partition1[1].decode('utf-8')) + "</td></tr>\n"
            report += "<tr><td><b>part_fit</b></td><td>" + str(partition1[2].decode('utf-8')) + "</td></tr>\n"
            report += "<tr><td><b>part_start</b></td><td>" + str(partition1[3]) + "</td></tr>\n"
            report += "<tr><td><b>part_size</b></td><td>" + str(partition1[4]) + "</td></tr>\n"
            report += "<tr><td><b>part_name</b></td><td>" + str(partition1[5].decode('utf-8').rstrip("\x00")) + "</td></tr>\n"
            if str(partition1[1].decode('utf-8')) == "e":
                f.seek(partition1[3])
                ebr_pack = f.read(struct.calcsize(format_ebr))
                ebr_unpack = struct.unpack(format_ebr,ebr_pack)
                next_part = partition1[3]
                while next_part != -1:
                    f.seek(next_part)
                    data_ebr = f.read(struct.calcsize(format_ebr))
                    ebr_unpack = struct.unpack(format_ebr,data_ebr)
                    report += "<tr><td colspan='2' bgcolor='#FF8000'><b>EBR</b></td></tr>\n"
                    report += "<tr><td><b>part_status</b></td><td>" + str(ebr_unpack[0].decode('utf-8')) + "</td></tr>\n"
                    report += "<tr><td><b>part_fit</b></td><td>" + str(ebr_unpack[1].decode('utf-8')) + "</td></tr>\n"
                    report += "<tr><td><b>part_start</b></td><td>" + str(ebr_unpack[2]) + "</td></tr>\n"
                    report += "<tr><td><b>part_size</b></td><td>" + str(ebr_unpack[3]) + "</td></tr>\n"
                    report += "<tr><td><b>part_next</b></td><td>" + str(ebr_unpack[4]) + "</td></tr>\n"
                    report += "<tr><td><b>part_name</b></td><td>" + str(ebr_unpack[5].decode('utf-8').rstrip("\x00")) + "</td></tr>\n"
                    next_part = ebr_unpack[4]

            report += "<tr><td colspan='2' bgcolor='#9F4AFF'><b>Particion 2</b></td></tr>\n"
            report += "<tr><td><b>part_status</b></td><td>" + str(partition2[0].decode('utf-8')) + "</td></tr>\n"
            report += "<tr><td><b>part_type</b></td><td>" + str(partition2[1].decode('utf-8')) + "</td></tr>\n"
            report += "<tr><td><b>part_fit</b></td><td>" + str(partition2[2].decode('utf-8')) + "</td></tr>\n"
            report += "<tr><td><b>part_start</b></td><td>" + str(partition2[3]) + "</td></tr>\n"
            report += "<tr><td><b>part_size</b></td><td>" + str(partition2[4]) + "</td></tr>\n"
            report += "<tr><td><b>part_name</b></td><td>" + str(partition2[5].decode('utf-8').rstrip("\x00")) + "</td></tr>\n"
            if str(partition2[1].decode('utf-8')) == "e":
                f.seek(partition2[3])
                ebr_pack = f.read(struct.calcsize(format_ebr))
                ebr_unpack = struct.unpack(format_ebr,ebr_pack)
                next_part = partition2[3]
                while next_part != -1:
                    f.seek(next_part)
                    data_ebr = f.read(struct.calcsize(format_ebr))
                    ebr_unpack = struct.unpack(format_ebr,data_ebr)
                    report += "<tr><td colspan='2' bgcolor='#FF8000'><b>EBR</b></td></tr>\n"
                    report += "<tr><td><b>part_status</b></td><td>" + str(ebr_unpack[0].decode('utf-8')) + "</td></tr>\n"
                    report += "<tr><td><b>part_fit</b></td><td>" + str(ebr_unpack[1].decode('utf-8')) + "</td></tr>\n"
                    report += "<tr><td><b>part_start</b></td><td>" + str(ebr_unpack[2]) + "</td></tr>\n"
                    report += "<tr><td><b>part_size</b></td><td>" + str(ebr_unpack[3]) + "</td></tr>\n"
                    report += "<tr><td><b>part_next</b></td><td>" + str(ebr_unpack[4]) + "</td></tr>\n"
                    report += "<tr><td><b>part_name</b></td><td>" + str(ebr_unpack[5].decode('utf-8').rstrip("\x00")) + "</td></tr>\n"
                    next_part = ebr_unpack[4]

            report += "<tr><td colspan='2' bgcolor='#9F4AFF'><b>Particion 3</b></td></tr>\n"
            report += "<tr><td><b>part_status</b></td><td>" + str(partition3[0].decode('utf-8')) + "</td></tr>\n"
            report += "<tr><td><b>part_type</b></td><td>" + str(partition3[1].decode('utf-8')) + "</td></tr>\n"
            report += "<tr><td><b>part_fit</b></td><td>" + str(partition3[2].decode('utf-8')) + "</td></tr>\n"
            report += "<tr><td><b>part_start</b></td><td>" + str(partition3[3]) + "</td></tr>\n"
            report += "<tr><td><b>part_size</b></td><td>" + str(partition3[4]) + "</td></tr>\n"
            report += "<tr><td><b>part_name</b></td><td>" + str(partition3[5].decode('utf-8').rstrip("\x00")) + "</td></tr>\n"
            if str(partition3[1].decode('utf-8')) == "e":
                f.seek(partition3[3])
                ebr_pack = f.read(struct.calcsize(format_ebr))
                ebr_unpack = struct.unpack(format_ebr,ebr_pack)
                next_part = partition3[3]
                while next_part != -1:
                    f.seek(next_part)
                    data_ebr = f.read(struct.calcsize(format_ebr))
                    ebr_unpack = struct.unpack(format_ebr,data_ebr)
                    report += "<tr><td colspan='2' bgcolor='#FF8000'><b>EBR</b></td></tr>\n"
                    report += "<tr><td><b>part_status</b></td><td>" + str(ebr_unpack[0].decode('utf-8')) + "</td></tr>\n"
                    report += "<tr><td><b>part_fit</b></td><td>" + str(ebr_unpack[1].decode('utf-8')) + "</td></tr>\n"
                    report += "<tr><td><b>part_start</b></td><td>" + str(ebr_unpack[2]) + "</td></tr>\n"
                    report += "<tr><td><b>part_size</b></td><td>" + str(ebr_unpack[3]) + "</td></tr>\n"
                    report += "<tr><td><b>part_next</b></td><td>" + str(ebr_unpack[4]) + "</td></tr>\n"
                    report += "<tr><td><b>part_name</b></td><td>" + str(ebr_unpack[5].decode('utf-8').rstrip("\x00")) + "</td></tr>\n"
                    next_part = ebr_unpack[4]
            report += "<tr><td colspan='2' bgcolor='#9F4AFF'><b>Particion 4</b></td></tr>\n"
            report += "<tr><td><b>part_status</b></td><td>" + str(partition4[0].decode('utf-8')) + "</td></tr>\n"
            report += "<tr><td><b>part_type</b></td><td>" + str(partition4[1].decode('utf-8')) + "</td></tr>\n"
            report += "<tr><td><b>part_fit</b></td><td>" + str(partition4[2].decode('utf-8')) + "</td></tr>\n"
            report += "<tr><td><b>part_start</b></td><td>" + str(partition4[3]) + "</td></tr>\n"
            report += "<tr><td><b>part_size</b></td><td>" + str(partition4[4]) + "</td></tr>\n"
            report += "<tr><td><b>part_name</b></td><td>" + str(partition4[5].decode('utf-8').rstrip("\x00")) + "</td></tr>\n"
            if str(partition4[1].decode('utf-8')) == "e":
                f.seek(partition4[3])
                ebr_pack = f.read(struct.calcsize(format_ebr))
                ebr_unpack = struct.unpack(format_ebr,ebr_pack)
               
                next_part = partition4[3]
                while next_part != -1:
                    f.seek(next_part)
                    data_ebr = f.read(struct.calcsize(format_ebr))
                    ebr_unpack = struct.unpack(format_ebr,data_ebr)
                    report += "<tr><td colspan='2' bgcolor='#FF8000'><b>EBR</b></td></tr>\n"
                    report += "<tr><td><b>part_status</b></td><td>" + str(ebr_unpack[0].decode('utf-8')) + "</td></tr>\n"
                    report += "<tr><td><b>part_fit</b></td><td>" + str(ebr_unpack[1].decode('utf-8')) + "</td></tr>\n"
                    report += "<tr><td><b>part_start</b></td><td>" + str(ebr_unpack[2]) + "</td></tr>\n"
                    report += "<tr><td><b>part_size</b></td><td>" + str(ebr_unpack[3]) + "</td></tr>\n"
                    report += "<tr><td><b>part_next</b></td><td>" + str(ebr_unpack[4]) + "</td></tr>\n"
                    report += "<tr><td><b>part_name</b></td><td>" + str(ebr_unpack[5].decode('utf-8').rstrip("\x00")) + "</td></tr>\n"
                    next_part = ebr_unpack[4]
            report += "</table>\n"
            report += ">];\n"
            report += "}\n"
            f.close()

        dot_file = '/home/noel/Documentos/USAC2023/Archivos/MIA_P12S2023_201900822/reports/'+self.nameDisk+'_mbr.dot'
        with open(dot_file, "w") as f:
            f.write(report)
            f.close()
        subprocess.run(['dot','-Tpng',dot_file,'-o',self.path],check=True)
        print("Reporte generado con exito")
        return


    def repDisk(self):

        report = ""
        repo = ""
        report += "digraph G{\n"
        report += "node[shape=plaintext]\n"
        report += "graph[label=<\n"
        report += "<table border='1' cellborder='1' cellspacing='2' color='orange'>\n"
        report += "<tr><td rowspan='3'>MBR</td>\n"
        format_mbr = "I I I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
        format_ebr = "c c I I i 16s"
        with open(self.path_mount, "rb+") as f:
            f.seek(0)
            mbr_pack = f.read(struct.calcsize(format_mbr))
            mbr_unpack = struct.unpack(format_mbr,mbr_pack)
            partition1 = mbr_unpack[4:10]
            partition2 = mbr_unpack[10:16]
            partition3 = mbr_unpack[16:22]
            partition4 = mbr_unpack[22:28]
            count = 0
            percentage01 = partition1[4] * 100 / mbr_unpack[0]
            percentage02 = partition2[4] * 100 / mbr_unpack[0]
            percentage03 = partition3[4] * 100 / mbr_unpack[0]
            percentage04 = partition4[4] * 100 / mbr_unpack[0]


            if str(partition1[1].decode('utf-8')) == "e":
                repo += "<tr>"
                f.seek(partition1[3])
                ebr_pack = f.read(struct.calcsize(format_ebr))
                ebr_unpack = struct.unpack(format_ebr,ebr_pack)
                next_part = partition1[3]
                while next_part != -1:
                    f.seek(next_part)
                    data_ebr = f.read(struct.calcsize(format_ebr))
                    ebr_unpack = struct.unpack(format_ebr,data_ebr)
                    percentage = ebr_unpack[3] * 100 / mbr_unpack[0]
                    repo += "<td>Ebr</td>"
                    repo += "<td>Logica<br/>"+str(round(percentage,2))+"%</td>\n"
                    count += 1
                    next_part = ebr_unpack[4]
                repo += "</tr>\n"
            if str(partition2[1].decode('utf-8')) == "e":
                repo += "<tr>"
                f.seek(partition2[3])
                ebr_pack = f.read(struct.calcsize(format_ebr))
                ebr_unpack = struct.unpack(format_ebr,ebr_pack)
                next_part = partition2[3]
                while next_part != -1:
                    f.seek(next_part)
                    data_ebr = f.read(struct.calcsize(format_ebr))
                    ebr_unpack = struct.unpack(format_ebr,data_ebr)
                    percentage = ebr_unpack[3] * 100 / mbr_unpack[0]
                    repo += "<td>Ebr</td>"
                    repo += "<td>Logica<br/>"+str(round(percentage,2))+"%</td>\n"
                    count += 1
                    next_part = ebr_unpack[4]
                repo += "</tr>\n"
            if str(partition3[1].decode('utf-8')) == "e":
                repo += "<tr>"
                f.seek(partition3[3])
                ebr_pack = f.read(struct.calcsize(format_ebr))
                ebr_unpack = struct.unpack(format_ebr,ebr_pack)
                next_part = partition3[3]
                while next_part != -1:
                    f.seek(next_part)
                    data_ebr = f.read(struct.calcsize(format_ebr))
                    ebr_unpack = struct.unpack(format_ebr,data_ebr)
                    percentage = ebr_unpack[3] * 100 / mbr_unpack[0]
                    repo += "<td>Ebr</td>"
                    repo += "<td>Logica<br/>"+str(round(percentage,2))+"%</td>\n"
                    count += 1
                    next_part = ebr_unpack[4]
                repo += "</tr>\n"
            if str(partition4[1].decode('utf-8')) == "e":
                repo += "<tr>"
                f.seek(partition4[3])
                ebr_pack = f.read(struct.calcsize(format_ebr))
                ebr_unpack = struct.unpack(format_ebr,ebr_pack)
                next_part = partition4[3]
                while next_part != -1:
                    f.seek(next_part)
                    data_ebr = f.read(struct.calcsize(format_ebr))
                    ebr_unpack = struct.unpack(format_ebr,data_ebr)
                    percentage = ebr_unpack[3] * 100 / mbr_unpack[0]
                    repo += "<td>Ebr</td>"
                    repo += "<td>Logica<br/>"+str(round(percentage,2))+"%</td>\n"
                    count += 1
                    next_part = ebr_unpack[4]
                repo += "</tr>\n"

            if partition1[0].decode('utf-8') == "1":
                if partition1[1].decode('utf-8') == "p":
                    report += "<td rowspan = '3'>Primaria<br/>"+str(percentage01)+"%</td>\n"
                if partition1[1].decode('utf-8') == "e":
                    report += "<td colspan = '"+str(count*2)+"'>Extendida</td>\n"
            else:
                report += "<td rowspan = '3'>Libre<br/>"+str(percentage01)+"%</td>\n"
            if partition2[0].decode('utf-8') == "1":
                if partition2[1].decode('utf-8') == "p":
                    report += "<td rowspan = '3'>Primaria<br/>"+str(percentage02)+"%</td>\n"
                if partition2[1].decode('utf-8') == "e":
                    report += "<td colspan = '"+str(count*2)+"'>Extendida</td>\n"
            else:
                report += "<td rowspan = '3'>Libre<br/>"+str(percentage02)+"%</td>\n"
            if partition3[0].decode('utf-8') == "1":
                if partition3[1].decode('utf-8') == "p":
                    report += "<td rowspan = '3'>Primaria<br/>"+str(percentage03)+"%</td>\n"
                if partition3[1].decode('utf-8') == "e":
                    report += "<td colspan = '"+str(count*2)+"'>Extendida</td>\n"
            else:
                report += "<td rowspan = '3'>Libre<br/>"+str(percentage03)+"%</td>\n"
            if partition4[0].decode('utf-8') == "1":
                if partition4[1].decode('utf-8') == "p":
                    report += "<td rowspan = '3'>Primaria<br/>"+str(percentage04)+"%</td>\n"
                if partition4[1].decode('utf-8') == "e":
                    report += "<td colspan = '"+str(count*2)+"'>Extendida</td>\n"
            else:
                report += "<td rowspan = '3'>Libre<br/>"+str(percentage04)+"%</td>\n"
            report += "</tr>\n"

            
            report += repo    

            report += "</table>\n"
            report += ">];\n"
            report += "}\n"
            f.close()
        dot_file = '/home/noel/Documentos/USAC2023/Archivos/MIA_P12S2023_201900822/reports/'+self.nameDisk+'_disk.dot'
        with open(dot_file, "w") as f:
            f.write(report)
            f.close()
        subprocess.run(['dot','-Tpng',dot_file,'-o',self.path],check=True)
        print("Reporte generado con exito")
        return
    
    def repInode(self,name_partition):
        format_mbr = "I I I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
        format_sb = "I I I I I I I I I I I I I I I I I"
        format_i = "I I I I I I 16i c I"

        with open(self.path_mount, "rb+") as f:
            f.seek(0)
            mbr_pack = f.read(struct.calcsize(format_mbr))
            mbr_unpack = struct.unpack(format_mbr,mbr_pack)
            partition1 = mbr_unpack[4:10]
            partition2 = mbr_unpack[10:16]
            partition3 = mbr_unpack[16:22]
            partition4 = mbr_unpack[22:28]

            report = ""
            report += "digraph G{\n"
            report += "node[shape=square]\nrankdir=LR\n"


            if partition1[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition1[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_inode_start = sb_unpack[13]
                inode_start = sb_unpack[15]
                size_bm_inode = sb_unpack[1]
                f.seek(bm_inode_start)
                bm_inode_pack = f.read(size_bm_inode)
                bm_inode_unpack = bm_inode_pack.decode('utf-8')
                for i in range(len(bm_inode_unpack)):
                    if bm_inode_unpack[i] != '0':
                        f.seek(inode_start + (i * struct.calcsize(format_i)))
                        inode_pack = f.read(struct.calcsize(format_i))
                        inode_unpack = struct.unpack(format_i,inode_pack)
                        inode_unpack = list(inode_unpack)
                        report += "inode"+str(i)+"[label=\"\n"
                        report += "i_uid = "+str(inode_unpack[0])+"\\ni_gid = "+str(inode_unpack[1])+"\ni_size = "+str(inode_unpack[2])+"\ni_atime = "+str(inode_unpack[3])+"\ni_ctime = "+str(inode_unpack[4])+"\ni_mtime = "+str(inode_unpack[5])+"\ni_block = ["
                        for j in range(15):
                            report += str(inode_unpack[6+j])+","
                        report += "]\ni_type = "+str(inode_unpack[21])+"\ni_perm = "+str(inode_unpack[22])+"\\n"

                        report += "\"]\n"
                for i in range(len(bm_inode_unpack)):
                    if bm_inode_unpack[i] != '0':
                        report += "inode"+str(i)+"->"
                report += "null\n"
                report += "}\n"
                f.close()
                dot_file = '/home/noel/Documentos/USAC2023/Archivos/MIA_P12S2023_201900822/reports/'+self.nameDisk+'_inode.dot'
                with open(dot_file, "w") as f:
                    f.write(report)
                    f.close()
                subprocess.run(['dot','-Tpng',dot_file,'-o',self.path],check=True)
                print("Reporte generado con exito")
                return
            elif partition2[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition2[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_inode_start = sb_unpack[13]
                inode_start = sb_unpack[15]
                size_bm_inode = sb_unpack[1]
                f.seek(bm_inode_start)
                bm_inode_pack = f.read(size_bm_inode)
                bm_inode_unpack = bm_inode_pack.decode('utf-8')
                for i in range(len(bm_inode_unpack)):
                    if bm_inode_unpack[i] != '0':
                        f.seek(inode_start + (i * struct.calcsize(format_i)))
                        inode_pack = f.read(struct.calcsize(format_i))
                        inode_unpack = struct.unpack(format_i,inode_pack)
                        inode_unpack = list(inode_unpack)
                        report += "inode"+str(i)+"[label=\"\n"
                        report += "i_uid = "+str(inode_unpack[0])+"\\ni_gid = "+str(inode_unpack[1])+"\ni_size = "+str(inode_unpack[2])+"\ni_atime = "+str(inode_unpack[3])+"\ni_ctime = "+str(inode_unpack[4])+"\ni_mtime = "+str(inode_unpack[5])+"\ni_block = ["
                        for j in range(15):
                            report += str(inode_unpack[6+j])+","
                        report += "]\ni_type = "+str(inode_unpack[21])+"\ni_perm = "+str(inode_unpack[22])+"\\n"

                        report += "\"]\n"
                for i in range(len(bm_inode_unpack)):
                    if bm_inode_unpack[i] != '0':
                        report += "inode"+str(i)+"->"
                report += "null\n"
                report += "}\n"
                f.close()
                dot_file = '/home/noel/Documentos/USAC2023/Archivos/MIA_P12S2023_201900822/reports/'+self.nameDisk+'_inode.dot'
                with open(dot_file, "w") as f:
                    f.write(report)
                    f.close()
                subprocess.run(['dot','-Tpng',dot_file,'-o',self.path],check=True)
                print("Reporte generado con exito")
                return
            elif partition3[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition3[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_inode_start = sb_unpack[13]
                inode_start = sb_unpack[15]
                size_bm_inode = sb_unpack[1]
                f.seek(bm_inode_start)
                bm_inode_pack = f.read(size_bm_inode)
                bm_inode_unpack = bm_inode_pack.decode('utf-8')
                for i in range(len(bm_inode_unpack)):
                    if bm_inode_unpack[i] != '0':
                        f.seek(inode_start + (i * struct.calcsize(format_i)))
                        inode_pack = f.read(struct.calcsize(format_i))
                        inode_unpack = struct.unpack(format_i,inode_pack)
                        inode_unpack = list(inode_unpack)
                        report += "inode"+str(i)+"[label=\"\n"
                        report += "i_uid = "+str(inode_unpack[0])+"\\ni_gid = "+str(inode_unpack[1])+"\ni_size = "+str(inode_unpack[2])+"\ni_atime = "+str(inode_unpack[3])+"\ni_ctime = "+str(inode_unpack[4])+"\ni_mtime = "+str(inode_unpack[5])+"\ni_block = ["
                        for j in range(15):
                            report += str(inode_unpack[6+j])+","
                        report += "]\ni_type = "+str(inode_unpack[21])+"\ni_perm = "+str(inode_unpack[22])+"\\n"

                        report += "\"]\n"
                for i in range(len(bm_inode_unpack)):
                    if bm_inode_unpack[i] != '0':
                        report += "inode"+str(i)+"->"
                report += "null\n"
                report += "}\n"
                f.close()
                dot_file = '/home/noel/Documentos/USAC2023/Archivos/MIA_P12S2023_201900822/reports/'+self.nameDisk+'_inode.dot'
                with open(dot_file, "w") as f:
                    f.write(report)
                    f.close()
                subprocess.run(['dot','-Tpng',dot_file,'-o',self.path],check=True)
                print("Reporte generado con exito")
                return
            elif partition4[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition4[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_inode_start = sb_unpack[13]
                inode_start = sb_unpack[15]
                size_bm_inode = sb_unpack[1]
                f.seek(bm_inode_start)
                bm_inode_pack = f.read(size_bm_inode)
                bm_inode_unpack = bm_inode_pack.decode('utf-8')
                for i in range(len(bm_inode_unpack)):
                    if bm_inode_unpack[i] != '0':
                        f.seek(inode_start + (i * struct.calcsize(format_i)))
                        inode_pack = f.read(struct.calcsize(format_i))
                        inode_unpack = struct.unpack(format_i,inode_pack)
                        inode_unpack = list(inode_unpack)
                        report += "inode"+str(i)+"[label=\"\n"
                        report += "i_uid = "+str(inode_unpack[0])+"\\ni_gid = "+str(inode_unpack[1])+"\ni_size = "+str(inode_unpack[2])+"\ni_atime = "+str(inode_unpack[3])+"\ni_ctime = "+str(inode_unpack[4])+"\ni_mtime = "+str(inode_unpack[5])+"\ni_block = ["
                        for j in range(15):
                            report += str(inode_unpack[6+j])+","
                        report += "]\ni_type = "+str(inode_unpack[21])+"\ni_perm = "+str(inode_unpack[22])+"\\n"

                        report += "\"]\n"
                for i in range(len(bm_inode_unpack)):
                    if bm_inode_unpack[i] != '0':
                        report += "inode"+str(i)+"->"
                report += "null\n"
                report += "}\n"
                f.close()
                dot_file = '/home/noel/Documentos/USAC2023/Archivos/MIA_P12S2023_201900822/reports/'+self.nameDisk+'_inode.dot'
                with open(dot_file, "w") as f:
                    f.write(report)
                    f.close()
                subprocess.run(['dot','-Tpng',dot_file,'-o',self.path],check=True)
                print("Reporte generado con exito")
                return

            
    def repBlock(self,name_partition):
        format_mbr = "I I I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
        format_sb = "I I I I I I I I I I I I I I I I I"
        format_i = "I I I I I I 15i c I"
        format_block = "64s"
        format_folder = "12s i 12s i 12s i 12s i"

        with open(self.path_mount, "rb+") as f:
            f.seek(0)
            mbr_pack = f.read(struct.calcsize(format_mbr))
            mbr_unpack = struct.unpack(format_mbr,mbr_pack)
            partition1 = mbr_unpack[4:10]
            partition2 = mbr_unpack[10:16]
            partition3 = mbr_unpack[16:22]
            partition4 = mbr_unpack[22:28]

            report = ""
            report += "digraph G{\n"
            report += "node[shape=square]\nrankdir=LR\n"
            blocks_files = []
            blocks_folders = []

            if partition1[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition1[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_inode_start = sb_unpack[13]
                inode_start = sb_unpack[15]
                block_start = sb_unpack[16]
                size_bm_inode = sb_unpack[1]
                f.seek(bm_inode_start)
                bm_inode_pack = f.read(size_bm_inode)
                bm_inode_unpack = bm_inode_pack.decode('utf-8')
                for i in range(len(bm_inode_unpack)):
                    if bm_inode_unpack[i] != '0':
                        f.seek(inode_start + (i * struct.calcsize(format_i)))
                        inode_pack = f.read(struct.calcsize(format_i))
                        inode_unpack = struct.unpack(format_i,inode_pack)
                        inode_unpack = list(inode_unpack)
                        if inode_unpack[21].decode('utf-8') == '0':
                            for j in range(15):
                                if inode_unpack[6+j] != -1:
                                    blocks_folders.append(inode_unpack[6+j])
                        elif inode_unpack[21].decode('utf-8') == '1':
                            for j in range(15):
                                if inode_unpack[6+j] != -1:
                                    blocks_files.append(inode_unpack[6+j])

                for i in range(len(blocks_folders)):
                    f.seek(block_start + ((blocks_folders[i]-1) * struct.calcsize(format_block)))
                    block_pack = f.read(struct.calcsize(format_block))
                    block_unpack = struct.unpack(format_folder,block_pack)
                    block_unpack = list(block_unpack)
                    
                    report += "block"+str(blocks_folders[i])+"[label=\"block_folder"+str(blocks_folders[i])+"\n"
                    report += "b_name = "+str(block_unpack[0].decode('utf-8').rstrip("\x00"))+"\t\tb_inode = "+str(block_unpack[1])+"\nb_name = "+str(block_unpack[2].decode('utf-8').rstrip("\x00"))+"\t\tb_inode = "+str(block_unpack[3])+"\nb_name = "+str(block_unpack[4].decode('utf-8').rstrip("\x00"))+"\t\tb_inode = "+str(block_unpack[5])+"\nb_name = "+str(block_unpack[6].decode('utf-8').rstrip("\x00"))+"\t\tb_inode = "+str(block_unpack[7])+"\"]\n"
                
                
                for i in range(len(blocks_files)):
                    f.seek(block_start + ((blocks_files[i]-1) * struct.calcsize(format_block)))
                    block_pack = f.read(struct.calcsize(format_block))
                    block_unpack = struct.unpack(format_block,block_pack)
                    block_unpack = list(block_unpack)
                    report += "block"+str(blocks_files[i])+"[label=\"block_file"+str(blocks_files[i])+"\n"
                    report += "b_content = "+str(block_unpack[0].decode('utf-8').rstrip("\x00"))+"\"]\n"
                
                max_bf = max(blocks_files)
                max_bd = max(blocks_folders)
                max_b = max(max_bf,max_bd)
                for i in range(max_b):
                    report += "block"+str(i+1)+"->"
                report += "null\n"
                report += "}\n" 
                
                f.close()
                dot_file = '/home/noel/Documentos/USAC2023/Archivos/MIA_P12S2023_201900822/reports/'+self.nameDisk+'_block.dot'
                with open(dot_file, "w") as f:
                    f.write(report)
                    f.close()
                subprocess.run(['dot','-Tpng',dot_file,'-o',self.path],check=True)
                print("Reporte generado con exito")
                return
            elif partition2[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition2[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_inode_start = sb_unpack[13]
                inode_start = sb_unpack[15]
                block_start = sb_unpack[16]
                size_bm_inode = sb_unpack[1]
                f.seek(bm_inode_start)
                bm_inode_pack = f.read(size_bm_inode)
                bm_inode_unpack = bm_inode_pack.decode('utf-8')
                for i in range(len(bm_inode_unpack)):
                    if bm_inode_unpack[i] != '0':
                        f.seek(inode_start + (i * struct.calcsize(format_i)))
                        inode_pack = f.read(struct.calcsize(format_i))
                        inode_unpack = struct.unpack(format_i,inode_pack)
                        inode_unpack = list(inode_unpack)
                        if inode_unpack[21].decode('utf-8') == '0':
                            for j in range(15):
                                if inode_unpack[6+j] != -1:
                                    blocks_folders.append(inode_unpack[6+j])
                        elif inode_unpack[21].decode('utf-8') == '1':
                            for j in range(15):
                                if inode_unpack[6+j] != -1:
                                    blocks_files.append(inode_unpack[6+j])

                for i in range(len(blocks_folders)):
                    f.seek(block_start + ((blocks_folders[i]-1) * struct.calcsize(format_block)))
                    block_pack = f.read(struct.calcsize(format_block))
                    block_unpack = struct.unpack(format_folder,block_pack)
                    block_unpack = list(block_unpack)
                    
                    report += "block"+str(blocks_folders[i])+"[label=\"block_folder"+str(blocks_folders[i])+"\n"
                    report += "b_name = "+str(block_unpack[0].decode('utf-8').rstrip("\x00"))+"\t\tb_inode = "+str(block_unpack[1])+"\nb_name = "+str(block_unpack[2].decode('utf-8').rstrip("\x00"))+"\t\tb_inode = "+str(block_unpack[3])+"\nb_name = "+str(block_unpack[4].decode('utf-8').rstrip("\x00"))+"\t\tb_inode = "+str(block_unpack[5])+"\nb_name = "+str(block_unpack[6].decode('utf-8').rstrip("\x00"))+"\t\tb_inode = "+str(block_unpack[7])+"\"]\n"
                
                
                for i in range(len(blocks_files)):
                    f.seek(block_start + ((blocks_files[i]-1) * struct.calcsize(format_block)))
                    block_pack = f.read(struct.calcsize(format_block))
                    block_unpack = struct.unpack(format_block,block_pack)
                    block_unpack = list(block_unpack)
                    report += "block"+str(blocks_files[i])+"[label=\"block_file"+str(blocks_files[i])+"\n"
                    report += "b_content = "+str(block_unpack[0].decode('utf-8').rstrip("\x00"))+"\"]\n"
                
                max_bf = max(blocks_files)
                max_bd = max(blocks_folders)
                max_b = max(max_bf,max_bd)
                for i in range(max_b):
                    report += "block"+str(i+1)+"->"
                report += "null\n"
                report += "}\n" 
                
                f.close()
                dot_file = '/home/noel/Documentos/USAC2023/Archivos/MIA_P12S2023_201900822/reports/'+self.nameDisk+'_block.dot'
                with open(dot_file, "w") as f:
                    f.write(report)
                    f.close()
                subprocess.run(['dot','-Tpng',dot_file,'-o',self.path],check=True)
                print("Reporte generado con exito")
                return
            elif partition3[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition3[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_inode_start = sb_unpack[13]
                inode_start = sb_unpack[15]
                block_start = sb_unpack[16]
                size_bm_inode = sb_unpack[1]
                f.seek(bm_inode_start)
                bm_inode_pack = f.read(size_bm_inode)
                bm_inode_unpack = bm_inode_pack.decode('utf-8')
                for i in range(len(bm_inode_unpack)):
                    if bm_inode_unpack[i] != '0':
                        f.seek(inode_start + (i * struct.calcsize(format_i)))
                        inode_pack = f.read(struct.calcsize(format_i))
                        inode_unpack = struct.unpack(format_i,inode_pack)
                        inode_unpack = list(inode_unpack)
                        if inode_unpack[21].decode('utf-8') == '0':
                            for j in range(15):
                                if inode_unpack[6+j] != -1:
                                    blocks_folders.append(inode_unpack[6+j])
                        elif inode_unpack[21].decode('utf-8') == '1':
                            for j in range(15):
                                if inode_unpack[6+j] != -1:
                                    blocks_files.append(inode_unpack[6+j])

                for i in range(len(blocks_folders)):
                    f.seek(block_start + ((blocks_folders[i]-1) * struct.calcsize(format_block)))
                    block_pack = f.read(struct.calcsize(format_block))
                    block_unpack = struct.unpack(format_folder,block_pack)
                    block_unpack = list(block_unpack)
                    
                    report += "block"+str(blocks_folders[i])+"[label=\"block_folder"+str(blocks_folders[i])+"\n"
                    report += "b_name = "+str(block_unpack[0].decode('utf-8').rstrip("\x00"))+"\t\tb_inode = "+str(block_unpack[1])+"\nb_name = "+str(block_unpack[2].decode('utf-8').rstrip("\x00"))+"\t\tb_inode = "+str(block_unpack[3])+"\nb_name = "+str(block_unpack[4].decode('utf-8').rstrip("\x00"))+"\t\tb_inode = "+str(block_unpack[5])+"\nb_name = "+str(block_unpack[6].decode('utf-8').rstrip("\x00"))+"\t\tb_inode = "+str(block_unpack[7])+"\"]\n"
                
                
                for i in range(len(blocks_files)):
                    f.seek(block_start + ((blocks_files[i]-1) * struct.calcsize(format_block)))
                    block_pack = f.read(struct.calcsize(format_block))
                    block_unpack = struct.unpack(format_block,block_pack)
                    block_unpack = list(block_unpack)
                    report += "block"+str(blocks_files[i])+"[label=\"block_file"+str(blocks_files[i])+"\n"
                    report += "b_content = "+str(block_unpack[0].decode('utf-8').rstrip("\x00"))+"\"]\n"
                
                max_bf = max(blocks_files)
                max_bd = max(blocks_folders)
                max_b = max(max_bf,max_bd)
                for i in range(max_b):
                    report += "block"+str(i+1)+"->"
                report += "null\n"
                report += "}\n" 
                
                f.close()
                dot_file = '/home/noel/Documentos/USAC2023/Archivos/MIA_P12S2023_201900822/reports/'+self.nameDisk+'_block.dot'
                with open(dot_file, "w") as f:
                    f.write(report)
                    f.close()
                subprocess.run(['dot','-Tpng',dot_file,'-o',self.path],check=True)
                print("Reporte generado con exito")
                return

            elif partition4[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition4[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_inode_start = sb_unpack[13]
                inode_start = sb_unpack[15]
                block_start = sb_unpack[16]
                size_bm_inode = sb_unpack[1]
                f.seek(bm_inode_start)
                bm_inode_pack = f.read(size_bm_inode)
                bm_inode_unpack = bm_inode_pack.decode('utf-8')
                for i in range(len(bm_inode_unpack)):
                    if bm_inode_unpack[i] != '0':
                        f.seek(inode_start + (i * struct.calcsize(format_i)))
                        inode_pack = f.read(struct.calcsize(format_i))
                        inode_unpack = struct.unpack(format_i,inode_pack)
                        inode_unpack = list(inode_unpack)
                        if inode_unpack[21].decode('utf-8') == '0':
                            for j in range(15):
                                if inode_unpack[6+j] != -1:
                                    blocks_folders.append(inode_unpack[6+j])
                        elif inode_unpack[21].decode('utf-8') == '1':
                            for j in range(15):
                                if inode_unpack[6+j] != -1:
                                    blocks_files.append(inode_unpack[6+j])

                for i in range(len(blocks_folders)):
                    f.seek(block_start + ((blocks_folders[i]-1) * struct.calcsize(format_block)))
                    block_pack = f.read(struct.calcsize(format_block))
                    block_unpack = struct.unpack(format_folder,block_pack)
                    block_unpack = list(block_unpack)
                    
                    report += "block"+str(blocks_folders[i])+"[label=\"block_folder"+str(blocks_folders[i])+"\n"
                    report += "b_name = "+str(block_unpack[0].decode('utf-8').rstrip("\x00"))+"\t\tb_inode = "+str(block_unpack[1])+"\nb_name = "+str(block_unpack[2].decode('utf-8').rstrip("\x00"))+"\t\tb_inode = "+str(block_unpack[3])+"\nb_name = "+str(block_unpack[4].decode('utf-8').rstrip("\x00"))+"\t\tb_inode = "+str(block_unpack[5])+"\nb_name = "+str(block_unpack[6].decode('utf-8').rstrip("\x00"))+"\t\tb_inode = "+str(block_unpack[7])+"\"]\n"
                
                
                for i in range(len(blocks_files)):
                    f.seek(block_start + ((blocks_files[i]-1) * struct.calcsize(format_block)))
                    block_pack = f.read(struct.calcsize(format_block))
                    block_unpack = struct.unpack(format_block,block_pack)
                    block_unpack = list(block_unpack)
                    report += "block"+str(blocks_files[i])+"[label=\"block_file"+str(blocks_files[i])+"\n"
                    report += "b_content = "+str(block_unpack[0].decode('utf-8').rstrip("\x00"))+"\"]\n"
                
                max_bf = max(blocks_files)
                max_bd = max(blocks_folders)
                max_b = max(max_bf,max_bd)
                for i in range(max_b):
                    report += "block"+str(i+1)+"->"
                report += "null\n"
                report += "}\n" 
                
                f.close()
                dot_file = '/home/noel/Documentos/USAC2023/Archivos/MIA_P12S2023_201900822/reports/'+self.nameDisk+'_block.dot'
                with open(dot_file, "w") as f:
                    f.write(report)
                    f.close()
                subprocess.run(['dot','-Tpng',dot_file,'-o',self.path],check=True)
                print("Reporte generado con exito")
                return
            
    def repBM_Inode(self,name_partition):
        format_mbr = "I I I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
        format_sb = "I I I I I I I I I I I I I I I I I"

        with open(self.path_mount, "rb+") as f:
            f.seek(0)
            mbr_pack = f.read(struct.calcsize(format_mbr))
            mbr_unpack = struct.unpack(format_mbr,mbr_pack)
            partition1 = mbr_unpack[4:10]
            partition2 = mbr_unpack[10:16]
            partition3 = mbr_unpack[16:22]
            partition4 = mbr_unpack[22:28]

            if partition1[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition1[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_inode_start = sb_unpack[13]
                size_bm_inode = sb_unpack[1]
                f.seek(bm_inode_start)
                bm_inode_pack = f.read(size_bm_inode)
                bm_inode_unpack = bm_inode_pack.decode('utf-8')
                report = ""
                for i in range(len(bm_inode_unpack)):
                    report += bm_inode_unpack[i]
                f.close()
                with open(self.path, "w") as f:
                    f.write(report)
                    f.close()
                print("Reporte generado con exito")
                return
            elif partition2[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition2[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_inode_start = sb_unpack[13]
                size_bm_inode = sb_unpack[1]
                f.seek(bm_inode_start)
                bm_inode_pack = f.read(size_bm_inode)
                bm_inode_unpack = bm_inode_pack.decode('utf-8')
                report = ""
                for i in range(len(bm_inode_unpack)):
                    report += bm_inode_unpack[i]
                f.close()
                with open(self.path, "w") as f:
                    f.write(report)
                    f.close()
                print("Reporte generado con exito")
                return
            elif partition3[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition3[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_inode_start = sb_unpack[13]
                size_bm_inode = sb_unpack[1]
                f.seek(bm_inode_start)
                bm_inode_pack = f.read(size_bm_inode)
                bm_inode_unpack = bm_inode_pack.decode('utf-8')
                report = ""
                for i in range(len(bm_inode_unpack)):
                    report += bm_inode_unpack[i]
                f.close()
                with open(self.path, "w") as f:
                    f.write(report)
                    f.close()
                print("Reporte generado con exito")
                return
            elif partition4[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition4[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_inode_start = sb_unpack[13]
                size_bm_inode = sb_unpack[1]
                f.seek(bm_inode_start)
                bm_inode_pack = f.read(size_bm_inode)
                bm_inode_unpack = bm_inode_pack.decode('utf-8')
                report = ""
                for i in range(len(bm_inode_unpack)):
                    report += bm_inode_unpack[i]
                f.close()
                with open(self.path, "w") as f:
                    f.write(report)
                    f.close()
                print("Reporte generado con exito")
                return
            
    def repBM_Block(self,name_partition):
        format_mbr = "I I I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
        format_sb = "I I I I I I I I I I I I I I I I I"
        with open(self.path_mount, "rb+") as f:
            f.seek(0)
            mbr_pack = f.read(struct.calcsize(format_mbr))
            mbr_unpack = struct.unpack(format_mbr,mbr_pack)
            partition1 = mbr_unpack[4:10]
            partition2 = mbr_unpack[10:16]
            partition3 = mbr_unpack[16:22]
            partition4 = mbr_unpack[22:28]

            if partition1[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition1[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_block_start = sb_unpack[14]
                size_bm_block = sb_unpack[2]
                f.seek(bm_block_start)
                bm_block_pack = f.read(size_bm_block)
                bm_block_unpack = bm_block_pack.decode('utf-8')
                report = ""
                for i in range(len(bm_block_unpack)):
                    report += bm_block_unpack[i]
                f.close()
                with open(self.path, "w") as f:
                    f.write(report)
                    f.close()
                print("Reporte generado con exito")
                return
            elif partition2[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition2[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_block_start = sb_unpack[14]
                size_bm_block = sb_unpack[2]
                f.seek(bm_block_start)
                bm_block_pack = f.read(size_bm_block)
                bm_block_unpack = bm_block_pack.decode('utf-8')
                report = ""
                for i in range(len(bm_block_unpack)):
                    report += bm_block_unpack[i]
                f.close()
                with open(self.path, "w") as f:
                    f.write(report)
                    f.close()
                print("Reporte generado con exito")
                return
            elif partition3[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition3[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_block_start = sb_unpack[14]
                size_bm_block = sb_unpack[2]
                f.seek(bm_block_start)
                bm_block_pack = f.read(size_bm_block)
                bm_block_unpack = bm_block_pack.decode('utf-8')
                report = ""
                for i in range(len(bm_block_unpack)):
                    report += bm_block_unpack[i]
                f.close()
                with open(self.path, "w") as f:
                    f.write(report)
                    f.close()
                print("Reporte generado con exito")
                return
            elif partition4[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition4[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_block_start = sb_unpack[14]
                size_bm_block = sb_unpack[2]
                f.seek(bm_block_start)
                bm_block_pack = f.read(size_bm_block)
                bm_block_unpack = bm_block_pack.decode('utf-8')
                report = ""
                for i in range(len(bm_block_unpack)):
                    report += bm_block_unpack[i]
                f.close()
                with open(self.path, "w") as f:
                    f.write(report)
                    f.close()
                print("Reporte generado con exito")
                return
            
    def repTree(self,name_partition):
        format_mbr = "I I I c c c c I I 16s c c c I I 16s c c c I I 16s c c c I I 16s"
        format_sb = "I I I I I I I I I I I I I I I I I"
        format_i = "I I I I I I 16i c I"
        format_block = "64s"
        format_folder = "12s i 12s i 12s i 12s i"
        format_pointers = "16i"
        blocks_files = []
        blocks_folders = []
        blocks_pointers = []
        with open(self.path_mount, "rb+") as f:
            f.seek(0)
            mbr_pack = f.read(struct.calcsize(format_mbr))
            mbr_unpack = struct.unpack(format_mbr,mbr_pack)
            partition1 = mbr_unpack[4:10]
            partition2 = mbr_unpack[10:16]
            partition3 = mbr_unpack[16:22]
            partition4 = mbr_unpack[22:28]

            if partition1[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition1[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_inode_start = sb_unpack[13]
                bm_block_start = sb_unpack[14]
                inode_start = sb_unpack[15]
                block_start = sb_unpack[16]
                size_bm_inode = sb_unpack[1]
                size_bm_block = sb_unpack[2]
                report = ""
                report += "digraph G{\n"
                report += "node[shape=none]\nrankdir=LR\n"
                reportfeet = ""
                f.seek(bm_inode_start)
                bm_inode_pack = f.read(size_bm_inode)
                bm_inode_unpack = bm_inode_pack.decode('utf-8')
                f.seek(bm_block_start)
                bm_block_pack = f.read(size_bm_block)
                bm_block_unpack = bm_block_pack.decode('utf-8')
                for i in range(len(bm_inode_unpack)):
                    if bm_inode_unpack[i] != '0':
                        f.seek(inode_start + (i * struct.calcsize(format_i)))
                        inode_pack = f.read(struct.calcsize(format_i))
                        inode_unpack = struct.unpack(format_i,inode_pack)
                        inode_unpack = list(inode_unpack)
                        report += "inode"+str(i+1)+"[label=<\n"
                        report += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\" bgcolor=\"#E850FF\">\n"
                        report += "<tr><td colspan=\"2\">Inodo "+str(i+1)+"</td></tr>\n"
                        report += "<tr><td>i_type</td><td>"+str(inode_unpack[22])+"</td></tr>\n"
                        for j in range(16):
                            report += "<tr><td>ap"+str(j)+"</td><td  port = \"cell"+str(inode_unpack[6+j])+"\">"+str(inode_unpack[6+j])+"</td></tr>\n"
                        report += "<tr><td>i_perm</td><td>"+str(inode_unpack[23])+"</td></tr>\n"
                        report += "</table>\n"
                        report += ">]\n"
                        if inode_unpack[22].decode('utf-8') == '0':
                            for j in range(16):
                                if inode_unpack[6+j] != -1:
                                    if j < 13:
                                        blocks_folders.append(inode_unpack[6+j])
                                    elif j >= 13:
                                        blocks_pointers.append(inode_unpack[6+j])
                                        f.seek(block_start + ((inode_unpack[6+j]-1) * struct.calcsize(format_block)))
                                        block_pack = f.read(struct.calcsize(format_pointers))
                                        block_unpack = struct.unpack(format_pointers,block_pack)
                                        block_unpack = list(block_unpack)
                                        for k in range(16):
                                            if block_unpack[k] != -1:
                                                blocks_folders.append(block_unpack[k])

                        elif inode_unpack[22].decode('utf-8') == '1':
                            for j in range(16):
                                if inode_unpack[6+j] != -1:
                                    if j < 13:
                                        blocks_files.append(inode_unpack[6+j])
                                    elif j >= 13:
                                        blocks_pointers.append(inode_unpack[6+j])
                                        f.seek(block_start + ((inode_unpack[6+j]-1) * struct.calcsize(format_block)))
                                        block_pack = f.read(struct.calcsize(format_pointers))
                                        block_unpack = struct.unpack(format_pointers,block_pack)
                                        block_unpack = list(block_unpack)
                                        for k in range(16):
                                            if block_unpack[k] != -1:
                                                blocks_files.append(block_unpack[k])
                        

                        for j in range(16):
                            if inode_unpack[6+j] != -1:
                                if j < 13:
                                    reportfeet += "inode"+str(i+1)+":cell"+str(inode_unpack[6+j])+"->block"+str(inode_unpack[6+j])+"\n"
                                elif j == 13:
                                    reportfeet += "inode"+str(i+1)+":cell"+str(inode_unpack[6+j])+"->pointer"+str(inode_unpack[6+j])+"\n"

                
                #print(blocks_folders)
                #print(blocks_files)
                #print(blocks_pointers)
                for i in range(len(blocks_pointers)):
                    f.seek(block_start + ((blocks_pointers[i]-1) * struct.calcsize(format_block)))
                    block_pack = f.read(struct.calcsize(format_pointers))
                    block_unpack = struct.unpack(format_pointers,block_pack)
                    block_unpack = list(block_unpack)
                    #print(block_unpack,"reportando apuntadores")
                    report += "pointer"+str(blocks_pointers[i])+"[label=<\n"
                    report += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\" bgcolor=\"#FFA850\">\n"
                    report += "<tr><td colspan=\"2\">Bloque Puntero "+str(blocks_pointers[i])+"</td></tr>\n"
                    for j in range(16):
                        report += "<tr><td>pointer"+str(j)+"</td><td port = \"cell"+str(block_unpack[j])+"\">"+str(block_unpack[j])+"</td></tr>\n"
                    report += "</table>\n"
                    report += ">]\n"
                    for j in range(16):
                        if block_unpack[j] != -1:
                            reportfeet += "pointer"+str(blocks_pointers[i])+":cell"+str(block_unpack[j])+"->block"+str(block_unpack[j])+"\n"

                for i in range(len(blocks_folders)):
                    f.seek(block_start + ((blocks_folders[i]-1) * struct.calcsize(format_block)))
                    block_pack = f.read(struct.calcsize(format_block))
                    block_unpack = struct.unpack(format_folder,block_pack)
                    block_unpack = list(block_unpack)
                    #print(block_unpack,"reportando carpetas")
                    report += "block"+str(blocks_folders[i])+"[label=<\n"
                    report += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\" bgcolor=\"#00F9CF\">\n"
                    report += "<tr><td colspan=\"2\">Bloque Carpeta "+str(blocks_folders[i])+"</td></tr>\n"
                    report += "<tr><td>"+str(block_unpack[0].decode('utf-8').rstrip("\x00"))+"</td>\n"
                    report += "<td port = \"in"+str(block_unpack[1])+"\">"+str(block_unpack[1])+"</td></tr>\n"
                    report += "<tr><td>"+str(block_unpack[2].decode('utf-8').rstrip("\x00"))+"</td>\n"
                    report += "<td port = \"in"+str(block_unpack[3])+"\">"+str(block_unpack[3])+"</td></tr>\n"
                    report += "<tr><td>"+str(block_unpack[4].decode('utf-8').rstrip("\x00"))+"</td>\n"
                    report += "<td port = \"in"+str(block_unpack[5])+"\">"+str(block_unpack[5])+"</td></tr>\n"
                    report += "<tr><td>"+str(block_unpack[6].decode('utf-8').rstrip("\x00"))+"</td>\n"
                    report += "<td port = \"in"+str(block_unpack[7])+"\">"+str(block_unpack[7])+"</td></tr>\n"
                    report += "</table>\n"
                    report += ">]\n"
                    if block_unpack[1] != -1 and block_unpack[1] != 0:
                        reportfeet += "block"+str(blocks_folders[i])+":in"+str(block_unpack[1])+"->inode"+str(block_unpack[1])+"\n"
                    if block_unpack[3] != -1 and block_unpack[3] != 0:
                        reportfeet += "block"+str(blocks_folders[i])+":in"+str(block_unpack[3])+"->inode"+str(block_unpack[3])+"\n"
                    if block_unpack[5] != -1 and block_unpack[5] != 0:
                        reportfeet += "block"+str(blocks_folders[i])+":in"+str(block_unpack[5])+"->inode"+str(block_unpack[5])+"\n"
                    if block_unpack[7] != -1 and block_unpack[7] != 0:
                        reportfeet += "block"+str(blocks_folders[i])+":in"+str(block_unpack[7])+"->inode"+str(block_unpack[7])+"\n"
                
                for i in range(len(blocks_files)):
                    f.seek(block_start + ((blocks_files[i]-1) * struct.calcsize(format_block)))
                    block_pack = f.read(struct.calcsize(format_block))
                    block_unpack = struct.unpack(format_block,block_pack)
                    block_unpack = list(block_unpack)
                    report += "block"+str(blocks_files[i])+"[label=<\n"
                    report += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\" bgcolor=\"#F9D800\">\n"
                    report += "<tr><td colspan=\"2\">Bloque Archivo "+str(blocks_files[i])+"</td></tr>\n"
                    report += "<tr><td>b_content</td><td>"+str(block_unpack[0].decode('utf-8').rstrip("\x00"))+"</td></tr>\n"
                    report += "</table>\n"
                    report += ">]\n"
                    
                report += reportfeet
                report += "}\n"
                f.close()
                dot_file = '/home/noel/Documentos/USAC2023/Archivos/MIA_P12S2023_201900822/reports/'+self.nameDisk+'_tree.dot'
                with open(dot_file, "w") as f:
                    f.write(report)
                    f.close()
                subprocess.run(['dot','-Tpng',dot_file,'-o',self.path],check=True)
                print("Reporte generado con exito")
                return
            elif partition2[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition2[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_inode_start = sb_unpack[13]
                bm_block_start = sb_unpack[14]
                inode_start = sb_unpack[15]
                block_start = sb_unpack[16]
                size_bm_inode = sb_unpack[1]
                size_bm_block = sb_unpack[2]
                report = ""
                report += "digraph G{\n"
                report += "node[shape=none]\nrankdir=LR\n"
                reportfeet = ""
                f.seek(bm_inode_start)
                bm_inode_pack = f.read(size_bm_inode)
                bm_inode_unpack = bm_inode_pack.decode('utf-8')
                f.seek(bm_block_start)
                bm_block_pack = f.read(size_bm_block)
                bm_block_unpack = bm_block_pack.decode('utf-8')
                for i in range(len(bm_inode_unpack)):
                    if bm_inode_unpack[i] != '0':
                        f.seek(inode_start + (i * struct.calcsize(format_i)))
                        inode_pack = f.read(struct.calcsize(format_i))
                        inode_unpack = struct.unpack(format_i,inode_pack)
                        inode_unpack = list(inode_unpack)
                        report += "inode"+str(i+1)+"[label=<\n"
                        report += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\" bgcolor=\"#E850FF\">\n"
                        report += "<tr><td colspan=\"2\">Inodo "+str(i+1)+"</td></tr>\n"
                        report += "<tr><td>i_type</td><td>"+str(inode_unpack[22])+"</td></tr>\n"
                        for j in range(16):
                            report += "<tr><td>ap"+str(j)+"</td><td  port = \"cell"+str(inode_unpack[6+j])+"\">"+str(inode_unpack[6+j])+"</td></tr>\n"
                        report += "<tr><td>i_perm</td><td>"+str(inode_unpack[23])+"</td></tr>\n"
                        report += "</table>\n"
                        report += ">]\n"
                        if inode_unpack[22].decode('utf-8') == '0':
                            for j in range(16):
                                if inode_unpack[6+j] != -1:
                                    blocks_folders.append(inode_unpack[6+j])
                        elif inode_unpack[22].decode('utf-8') == '1':
                            for j in range(16):
                                if inode_unpack[6+j] != -1:
                                    blocks_files.append(inode_unpack[6+j])

                        for j in range(16):
                            if inode_unpack[6+j] != -1:
                                reportfeet += "inode"+str(i+1)+":cell"+str(inode_unpack[6+j])+"->block"+str(inode_unpack[6+j])+"\n"

                for i in range(len(blocks_folders)):
                    f.seek(block_start + ((blocks_folders[i]-1) * struct.calcsize(format_block)))
                    block_pack = f.read(struct.calcsize(format_block))
                    block_unpack = struct.unpack(format_folder,block_pack)
                    block_unpack = list(block_unpack)
                    
                    report += "block"+str(blocks_folders[i])+"[label=<\n"
                    report += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\" bgcolor=\"#00F9CF\">\n"
                    report += "<tr><td colspan=\"2\">Bloque Carpeta "+str(blocks_folders[i])+"</td></tr>\n"
                    report += "<tr><td>"+str(block_unpack[0].decode('utf-8').rstrip("\x00"))+"</td>\n"
                    report += "<td port = \"in"+str(block_unpack[1])+"\">"+str(block_unpack[1])+"</td></tr>\n"
                    report += "<tr><td>"+str(block_unpack[2].decode('utf-8').rstrip("\x00"))+"</td>\n"
                    report += "<td port = \"in"+str(block_unpack[3])+"\">"+str(block_unpack[3])+"</td></tr>\n"
                    report += "<tr><td>"+str(block_unpack[4].decode('utf-8').rstrip("\x00"))+"</td>\n"
                    report += "<td port = \"in"+str(block_unpack[5])+"\">"+str(block_unpack[5])+"</td></tr>\n"
                    report += "<tr><td>"+str(block_unpack[6].decode('utf-8').rstrip("\x00"))+"</td>\n"
                    report += "<td port = \"in"+str(block_unpack[7])+"\">"+str(block_unpack[7])+"</td></tr>\n"
                    report += "</table>\n"
                    report += ">]\n"
                    if block_unpack[1] != -1 and block_unpack[1] != 0:
                        reportfeet += "block"+str(blocks_folders[i])+":in"+str(block_unpack[1])+"->inode"+str(block_unpack[1])+"\n"
                    if block_unpack[3] != -1 and block_unpack[3] != 0:
                        reportfeet += "block"+str(blocks_folders[i])+":in"+str(block_unpack[3])+"->inode"+str(block_unpack[3])+"\n"
                    if block_unpack[5] != -1 and block_unpack[5] != 0:
                        reportfeet += "block"+str(blocks_folders[i])+":in"+str(block_unpack[5])+"->inode"+str(block_unpack[5])+"\n"
                    if block_unpack[7] != -1 and block_unpack[7] != 0:
                        reportfeet += "block"+str(blocks_folders[i])+":in"+str(block_unpack[7])+"->inode"+str(block_unpack[7])+"\n"

                for i in range(len(blocks_files)):
                    f.seek(block_start + ((blocks_files[i]-1) * struct.calcsize(format_block)))
                    block_pack = f.read(struct.calcsize(format_block))
                    block_unpack = struct.unpack(format_block,block_pack)
                    block_unpack = list(block_unpack)
                    report += "block"+str(blocks_files[i])+"[label=<\n"
                    report += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\" bgcolor=\"#F9D800\">\n"
                    report += "<tr><td colspan=\"2\">Bloque Archivo "+str(blocks_files[i])+"</td></tr>\n"
                    report += "<tr><td>b_content</td><td>"+str(block_unpack[0].decode('utf-8').rstrip("\x00"))+"</td></tr>\n"
                    report += "</table>\n"
                    report += ">]\n"
                    
                report += reportfeet
                report += "}\n"
                f.close()
                dot_file = '/home/noel/Documentos/USAC2023/Archivos/MIA_P12S2023_201900822/reports/'+self.nameDisk+'_tree.dot'
                with open(dot_file, "w") as f:
                    f.write(report)
                    f.close()
                subprocess.run(['dot','-Tpng',dot_file,'-o',self.path],check=True)
                print("Reporte generado con exito")
                return
            elif partition3[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition3[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_inode_start = sb_unpack[13]
                bm_block_start = sb_unpack[14]
                inode_start = sb_unpack[15]
                block_start = sb_unpack[16]
                size_bm_inode = sb_unpack[1]
                size_bm_block = sb_unpack[2]
                report = ""
                report += "digraph G{\n"
                report += "node[shape=none]\nrankdir=LR\n"
                reportfeet = ""
                f.seek(bm_inode_start)
                bm_inode_pack = f.read(size_bm_inode)
                bm_inode_unpack = bm_inode_pack.decode('utf-8')
                f.seek(bm_block_start)
                bm_block_pack = f.read(size_bm_block)
                bm_block_unpack = bm_block_pack.decode('utf-8')
                for i in range(len(bm_inode_unpack)):
                    if bm_inode_unpack[i] != '0':
                        f.seek(inode_start + (i * struct.calcsize(format_i)))
                        inode_pack = f.read(struct.calcsize(format_i))
                        inode_unpack = struct.unpack(format_i,inode_pack)
                        inode_unpack = list(inode_unpack)
                        report += "inode"+str(i+1)+"[label=<\n"
                        report += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\" bgcolor=\"#E850FF\">\n"
                        report += "<tr><td colspan=\"2\">Inodo "+str(i+1)+"</td></tr>\n"
                        report += "<tr><td>i_type</td><td>"+str(inode_unpack[22])+"</td></tr>\n"
                        for j in range(16):
                            report += "<tr><td>ap"+str(j)+"</td><td  port = \"cell"+str(inode_unpack[6+j])+"\">"+str(inode_unpack[6+j])+"</td></tr>\n"
                        report += "<tr><td>i_perm</td><td>"+str(inode_unpack[23])+"</td></tr>\n"
                        report += "</table>\n"
                        report += ">]\n"
                        if inode_unpack[22].decode('utf-8') == '0':
                            for j in range(16):
                                if inode_unpack[6+j] != -1:
                                    blocks_folders.append(inode_unpack[6+j])
                        elif inode_unpack[22].decode('utf-8') == '1':
                            for j in range(16):
                                if inode_unpack[6+j] != -1:
                                    blocks_files.append(inode_unpack[6+j])

                        for j in range(16):
                            if inode_unpack[6+j] != -1:
                                reportfeet += "inode"+str(i+1)+":cell"+str(inode_unpack[6+j])+"->block"+str(inode_unpack[6+j])+"\n"

                for i in range(len(blocks_folders)):
                    f.seek(block_start + ((blocks_folders[i]-1) * struct.calcsize(format_block)))
                    block_pack = f.read(struct.calcsize(format_block))
                    block_unpack = struct.unpack(format_folder,block_pack)
                    block_unpack = list(block_unpack)
                    
                    report += "block"+str(blocks_folders[i])+"[label=<\n"
                    report += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\" bgcolor=\"#00F9CF\">\n"
                    report += "<tr><td colspan=\"2\">Bloque Carpeta "+str(blocks_folders[i])+"</td></tr>\n"
                    report += "<tr><td>"+str(block_unpack[0].decode('utf-8').rstrip("\x00"))+"</td>\n"
                    report += "<td port = \"in"+str(block_unpack[1])+"\">"+str(block_unpack[1])+"</td></tr>\n"
                    report += "<tr><td>"+str(block_unpack[2].decode('utf-8').rstrip("\x00"))+"</td>\n"
                    report += "<td port = \"in"+str(block_unpack[3])+"\">"+str(block_unpack[3])+"</td></tr>\n"
                    report += "<tr><td>"+str(block_unpack[4].decode('utf-8').rstrip("\x00"))+"</td>\n"
                    report += "<td port = \"in"+str(block_unpack[5])+"\">"+str(block_unpack[5])+"</td></tr>\n"
                    report += "<tr><td>"+str(block_unpack[6].decode('utf-8').rstrip("\x00"))+"</td>\n"
                    report += "<td port = \"in"+str(block_unpack[7])+"\">"+str(block_unpack[7])+"</td></tr>\n"
                    report += "</table>\n"
                    report += ">]\n"
                    if block_unpack[1] != -1 and block_unpack[1] != 0:
                        reportfeet += "block"+str(blocks_folders[i])+":in"+str(block_unpack[1])+"->inode"+str(block_unpack[1])+"\n"
                    if block_unpack[3] != -1 and block_unpack[3] != 0:
                        reportfeet += "block"+str(blocks_folders[i])+":in"+str(block_unpack[3])+"->inode"+str(block_unpack[3])+"\n"
                    if block_unpack[5] != -1 and block_unpack[5] != 0:
                        reportfeet += "block"+str(blocks_folders[i])+":in"+str(block_unpack[5])+"->inode"+str(block_unpack[5])+"\n"
                    if block_unpack[7] != -1 and block_unpack[7] != 0:
                        reportfeet += "block"+str(blocks_folders[i])+":in"+str(block_unpack[7])+"->inode"+str(block_unpack[7])+"\n"

                for i in range(len(blocks_files)):
                    f.seek(block_start + ((blocks_files[i]-1) * struct.calcsize(format_block)))
                    block_pack = f.read(struct.calcsize(format_block))
                    block_unpack = struct.unpack(format_block,block_pack)
                    block_unpack = list(block_unpack)
                    report += "block"+str(blocks_files[i])+"[label=<\n"
                    report += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\" bgcolor=\"#F9D800\">\n"
                    report += "<tr><td colspan=\"2\">Bloque Archivo "+str(blocks_files[i])+"</td></tr>\n"
                    report += "<tr><td>b_content</td><td>"+str(block_unpack[0].decode('utf-8').rstrip("\x00"))+"</td></tr>\n"
                    report += "</table>\n"
                    report += ">]\n"
                    
                report += reportfeet
                report += "}\n"
                f.close()
                dot_file = '/home/noel/Documentos/USAC2023/Archivos/MIA_P12S2023_201900822/reports/'+self.nameDisk+'_tree.dot'
                with open(dot_file, "w") as f:
                    f.write(report)
                    f.close()
                subprocess.run(['dot','-Tpng',dot_file,'-o',self.path],check=True)
                print("Reporte generado con exito")
                return
            elif partition4[5].decode('utf-8').rstrip("\x00") == name_partition:
                f.seek(partition1[3])
                sb_pack = f.read(struct.calcsize(format_sb))
                sb_unpack = struct.unpack(format_sb,sb_pack)
                bm_inode_start = sb_unpack[13]
                bm_block_start = sb_unpack[14]
                inode_start = sb_unpack[15]
                block_start = sb_unpack[16]
                size_bm_inode = sb_unpack[1]
                size_bm_block = sb_unpack[2]
                report = ""
                report += "digraph G{\n"
                report += "node[shape=none]\nrankdir=LR\n"
                reportfeet = ""
                f.seek(bm_inode_start)
                bm_inode_pack = f.read(size_bm_inode)
                bm_inode_unpack = bm_inode_pack.decode('utf-8')
                f.seek(bm_block_start)
                bm_block_pack = f.read(size_bm_block)
                bm_block_unpack = bm_block_pack.decode('utf-8')
                for i in range(len(bm_inode_unpack)):
                    if bm_inode_unpack[i] != '0':
                        f.seek(inode_start + (i * struct.calcsize(format_i)))
                        inode_pack = f.read(struct.calcsize(format_i))
                        inode_unpack = struct.unpack(format_i,inode_pack)
                        inode_unpack = list(inode_unpack)
                        report += "inode"+str(i+1)+"[label=<\n"
                        report += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\" bgcolor=\"#E850FF\">\n"
                        report += "<tr><td colspan=\"2\">Inodo "+str(i+1)+"</td></tr>\n"
                        report += "<tr><td>i_type</td><td>"+str(inode_unpack[22])+"</td></tr>\n"
                        for j in range(16):
                            report += "<tr><td>ap"+str(j)+"</td><td  port = \"cell"+str(inode_unpack[6+j])+"\">"+str(inode_unpack[6+j])+"</td></tr>\n"
                        report += "<tr><td>i_perm</td><td>"+str(inode_unpack[23])+"</td></tr>\n"
                        report += "</table>\n"
                        report += ">]\n"
                        if inode_unpack[22].decode('utf-8') == '0':
                            for j in range(16):
                                if inode_unpack[6+j] != -1:
                                    blocks_folders.append(inode_unpack[6+j])
                        elif inode_unpack[22].decode('utf-8') == '1':
                            for j in range(16):
                                if inode_unpack[6+j] != -1:
                                    blocks_files.append(inode_unpack[6+j])

                        for j in range(16):
                            if inode_unpack[6+j] != -1:
                                reportfeet += "inode"+str(i+1)+":cell"+str(inode_unpack[6+j])+"->block"+str(inode_unpack[6+j])+"\n"

                for i in range(len(blocks_folders)):
                    f.seek(block_start + ((blocks_folders[i]-1) * struct.calcsize(format_block)))
                    block_pack = f.read(struct.calcsize(format_block))
                    block_unpack = struct.unpack(format_folder,block_pack)
                    block_unpack = list(block_unpack)
                    
                    report += "block"+str(blocks_folders[i])+"[label=<\n"
                    report += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\" bgcolor=\"#00F9CF\">\n"
                    report += "<tr><td colspan=\"2\">Bloque Carpeta "+str(blocks_folders[i])+"</td></tr>\n"
                    report += "<tr><td>"+str(block_unpack[0].decode('utf-8').rstrip("\x00"))+"</td>\n"
                    report += "<td port = \"in"+str(block_unpack[1])+"\">"+str(block_unpack[1])+"</td></tr>\n"
                    report += "<tr><td>"+str(block_unpack[2].decode('utf-8').rstrip("\x00"))+"</td>\n"
                    report += "<td port = \"in"+str(block_unpack[3])+"\">"+str(block_unpack[3])+"</td></tr>\n"
                    report += "<tr><td>"+str(block_unpack[4].decode('utf-8').rstrip("\x00"))+"</td>\n"
                    report += "<td port = \"in"+str(block_unpack[5])+"\">"+str(block_unpack[5])+"</td></tr>\n"
                    report += "<tr><td>"+str(block_unpack[6].decode('utf-8').rstrip("\x00"))+"</td>\n"
                    report += "<td port = \"in"+str(block_unpack[7])+"\">"+str(block_unpack[7])+"</td></tr>\n"
                    report += "</table>\n"
                    report += ">]\n"
                    if block_unpack[1] != -1 and block_unpack[1] != 0:
                        reportfeet += "block"+str(blocks_folders[i])+":in"+str(block_unpack[1])+"->inode"+str(block_unpack[1])+"\n"
                    if block_unpack[3] != -1 and block_unpack[3] != 0:
                        reportfeet += "block"+str(blocks_folders[i])+":in"+str(block_unpack[3])+"->inode"+str(block_unpack[3])+"\n"
                    if block_unpack[5] != -1 and block_unpack[5] != 0:
                        reportfeet += "block"+str(blocks_folders[i])+":in"+str(block_unpack[5])+"->inode"+str(block_unpack[5])+"\n"
                    if block_unpack[7] != -1 and block_unpack[7] != 0:
                        reportfeet += "block"+str(blocks_folders[i])+":in"+str(block_unpack[7])+"->inode"+str(block_unpack[7])+"\n"

                for i in range(len(blocks_files)):
                    f.seek(block_start + ((blocks_files[i]-1) * struct.calcsize(format_block)))
                    block_pack = f.read(struct.calcsize(format_block))
                    block_unpack = struct.unpack(format_block,block_pack)
                    block_unpack = list(block_unpack)
                    report += "block"+str(blocks_files[i])+"[label=<\n"
                    report += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\" bgcolor=\"#F9D800\">\n"
                    report += "<tr><td colspan=\"2\">Bloque Archivo "+str(blocks_files[i])+"</td></tr>\n"
                    report += "<tr><td>b_content</td><td>"+str(block_unpack[0].decode('utf-8').rstrip("\x00"))+"</td></tr>\n"
                    report += "</table>\n"
                    report += ">]\n"
                    
                report += reportfeet
                report += "}\n"
                f.close()
                dot_file = '/home/noel/Documentos/USAC2023/Archivos/MIA_P12S2023_201900822/reports/'+self.nameDisk+'_tree.dot'
                with open(dot_file, "w") as f:
                    f.write(report)
                    f.close()
                subprocess.run(['dot','-Tpng',dot_file,'-o',self.path],check=True)
                print("Reporte generado con exito")
                return
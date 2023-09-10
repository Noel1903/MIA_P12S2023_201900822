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
        format_i = "I I I I I I 15i c I"

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







            



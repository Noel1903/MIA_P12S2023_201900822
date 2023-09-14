import os
import sys
# Obtener la ruta completa del directorio padre
dir_padre = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Agregar el directorio padre al sys.path
sys.path.append(dir_padre)
#new_limit = 5000  # Set the desired recursion limit
#sys.setrecursionlimit(new_limit)

from commands.mkdisk import mkdisk
from commands.rmdisk import rmdisk
from commands.fdisk import fdisk
from commands.mount import mount
from commands.unmount import unmount
from commands.mkfs import mkfs
from commands.login import login
from commands.mkgrp import mkgrp
from commands.mkusr import mkusr
from commands.mkdir import mkdir
from commands.mkfile import mkfile
from commands.rep import rep
from commands.pause import pause
from commands.logout import logout
from commands.cat import cat
from commands.rename import rename
from commands.rmgrp import rmgrp
from commands.rmusr import rmusr
#reserved words
reserved = {
    'mkdisk' : 'MKDISK',
    'rmdisk' : 'RMDISK',
    'fdisk' : 'FDISK',
    'mount' : 'MOUNT',
    'unmount' : 'UNMOUNT',
    'size' : 'SIZE',
    'path' : 'PATH',
    'unit' : 'UNIT',
    'fit' : 'FIT',
    'name' : 'NAME',
    'type' : 'TYPE',
    'delete' : 'DELETE',
    'add' : 'ADD',
    'id': 'ID_PARAM',
    'mkfs' : 'MKFS',
    'fs' : 'FS',
    'login' : 'LOGIN',
    'user' : 'USER',
    'pass' : 'PASS',
    'logout' : 'LOGOUT',
    'mkgrp' : 'MKGRP',
    'mkusr' : 'MKUSR',
    'grp' : 'GRP',
    'r'     : 'R',
    'mkdir' : 'MKDIR',
    'mkfile' : 'MKFILE',
    'cont' : 'CONT',
    'rep' : 'REP',
    'ruta' : 'RUTA',
    'pause': 'PAUSE',
    'cat': 'CAT',
    'file': 'FILE',
    'rename': 'RENAME',
    'rmgrp': 'RMGRP',
    'rmusr': 'RMUSR',
}

#Tokens
tokens = [
    'SEPARATOR',#-
    'ASSIGN',#=
    'FILEN',
    'EXTENSION',
    'PATHWITHQUOTES',#"ruta"
    'PATHWITHOUTQUOTES',#ruta
    'MOUNTNAME',#221Disco1
    'NUMBER',
    'NEGATIVE',
    'ID',
    'STRING',
] + list(reserved.values())

t_SEPARATOR = r'-'
t_ASSIGN = r'='


def t_FILEN(t):
    r'file\d+'
    t.value = t.value 
    return t

def t_EXTENSION(t):
    r'([a-zA-Z0-9])+\.[a-zA-Z0-9]+'
    t.value = t.value 
    return t

def t_PATHWITHQUOTES(t):
    r'\".*\"'
    t.value = t.value[1:-1]
    return t

def t_PATHWITHOUTQUOTES(t):
    r'(\/[^ "/\n]+(\.[a-zA-Z0-9]+)?)+'
    return t


def t_MOUNTNAME(t):
    r'[0-9]+([a-zA-Z_][a-zA-Z_0-9]*)'
    t.type = reserved.get(t.value,'MOUNTNAME')
    return t

def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t   

def t_NEGATIVE(t):
    r'-[0-9]+'
    t.value = int(t.value)
    return t 

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(),'ID')
    return t

def t_STRING(t):
    r'\".*\"'
    t.value = t.value[1:-1]
    return t




#Ignore
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_line_comm(t):
    r'\#.*'
    t.lexer.lineno += 1

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()
#sintactico empieza aqui
def p_init(t):
    'init : commandsI'
    t[0] = t[1]

def p_commands(t):
    '''commandsI : commandsI command
                | command'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]
    
def p_command(t):
    '''command : mkdisk_block
               | rmdisk_block
               | fdisk_block
               | mount_block
               | unmount_block
               | mkfs_block
               | login_block
               | logout_block
               | mkgrp_block
               | usr_block
               | mkdir_block
               | mkfile_block
               | rep_block
               | pause_block
               | cat_block
               | rename_block
               | rmgrp_block
               | rmusr_block'''
    t[0] = t[1]

def p_rmusr_block(t):
    'rmusr_block : RMUSR rmusr_params'
    t[0] = rmusr(t[2])

def p_rmusr_params(t):
    '''rmusr_params : rmusr_params rmusr_param
                    | rmusr_param'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else: 
        t[0] = [t[1]]

def p_rmusr_param(t):
    '''rmusr_param : SEPARATOR USER ASSIGN ID
                   | SEPARATOR USER ASSIGN STRING'''
    if t[2] == "user":
        t[0] = ["user", t[4]]

def p_rmgrp_block(t):
    'rmgrp_block : RMGRP rmgrp_params'
    t[0] = rmgrp(t[2])

def p_rmgrp_params(t):
    '''rmgrp_params : rmgrp_params rmgrp_param
                    | rmgrp_param'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_rmgrp_param(t):
    '''rmgrp_param : SEPARATOR NAME ASSIGN ID
                   | SEPARATOR NAME ASSIGN STRING'''
    if t[2] == "name":
        t[0] = ["name", t[4]]

def p_pause_block(t):
    'pause_block : PAUSE'
    t[0] = pause(t[1])

def p_logout_block(t):
    'logout_block : LOGOUT'
    t[0] = logout(t[1])

def p_mkdisk_block(t):
    'mkdisk_block : MKDISK mkdisk_params'
    t[0] = mkdisk(t[2])
    #t[0] = t[1]

def p_rmdisk_block(t):
    '''rmdisk_block : RMDISK SEPARATOR PATH ASSIGN PATHWITHQUOTES
                    | RMDISK SEPARATOR PATH ASSIGN PATHWITHOUTQUOTES'''
    t[0] = rmdisk(t[5])   

def p_mkdisk_params(t):
    '''mkdisk_params : mkdisk_params mkdisk_param
                     | mkdisk_param'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_mkdisk_param(t):
    '''mkdisk_param : SEPARATOR SIZE ASSIGN NUMBER
                    | SEPARATOR PATH ASSIGN PATHWITHQUOTES
                    | SEPARATOR PATH ASSIGN PATHWITHOUTQUOTES
                    | SEPARATOR UNIT ASSIGN ID
                    | SEPARATOR FIT ASSIGN ID'''
    if t[2] == "path":
        if t[4][0] == "\"":
            t[0] = ["path", t[4][1:-1]]
        else:
            t[0] = ["path", t[4]]
    elif t[2] == "size":
        t[0] = ["size", t[4]]
    elif t[2] == "unit":
        t[0] = ["unit", t[4]]
    elif t[2] == "fit":
        t[0] = ["fit", t[4]]

def p_fdisk_block(t):
    'fdisk_block : FDISK fdisk_params'
    t[0] = fdisk(t[2])

def p_fdisk_params(t):
    '''fdisk_params : fdisk_params fdisk_param
                    | fdisk_param'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_fdisk_param(t):
    '''fdisk_param : SEPARATOR SIZE ASSIGN NUMBER
                   | SEPARATOR PATH ASSIGN PATHWITHQUOTES
                   | SEPARATOR PATH ASSIGN PATHWITHOUTQUOTES
                   | SEPARATOR NAME ASSIGN ID
                   | SEPARATOR NAME ASSIGN PATHWITHOUTQUOTES
                   | SEPARATOR UNIT ASSIGN ID
                   | SEPARATOR TYPE ASSIGN ID
                   | SEPARATOR FIT ASSIGN ID
                   | SEPARATOR DELETE ASSIGN ID
                   | SEPARATOR ADD ASSIGN NUMBER
                   | SEPARATOR ADD ASSIGN NEGATIVE'''
    if t[2] == "path":
        t[0] = ["path", t[4]]
    elif t[2] == "size":
        t[0] = ["size", t[4]]
    elif t[2] == "name":
        t[0] = ["name", t[4]]
    elif t[2] == "unit":
        t[0] = ["unit", t[4]]
    elif t[2] == "type":
        t[0] = ["type", t[4]]
    elif t[2] == "fit":
        t[0] = ["fit", t[4]]
    elif t[2] == "delete":
        t[0] = ["delete", t[4]]
    elif t[2] == "add":
        t[0] = ["add", t[4]]  

def p_mount_block(t):
    'mount_block : MOUNT mount_params'
    t[0] = mount(t[2])

def p_mount_params(t):
    '''mount_params : mount_params mount_param
                    | mount_param'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_mount_param(t):
    '''mount_param : SEPARATOR PATH ASSIGN PATHWITHQUOTES
                   | SEPARATOR PATH ASSIGN PATHWITHOUTQUOTES
                   | SEPARATOR NAME ASSIGN ID'''
    if t[2] == "path":
        t[0] = ["path", t[4]]
    elif t[2] == "name":
        t[0] = ["name", t[4]]

def p_unmount_block(t):
    'unmount_block : UNMOUNT unmount_params'
    t[0] = unmount(t[2])

def p_unmount_params(t):
    '''unmount_params : unmount_params unmount_param
                      | unmount_param'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_unmount_param(t):
    '''unmount_param : SEPARATOR ID_PARAM ASSIGN MOUNTNAME'''
    if t[2] == "id":
        t[0] = ["id", t[4]]

def p_mkfs_block(t):
    'mkfs_block : MKFS mkfs_params'
    t[0] = mkfs(t[2])

def p_mkfs_params(t):
    '''mkfs_params : mkfs_params mkfs_param
                   | mkfs_param'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_mkfs_param(t):
    '''mkfs_param : SEPARATOR ID_PARAM ASSIGN MOUNTNAME
                  | SEPARATOR TYPE ASSIGN ID
                  | SEPARATOR FS ASSIGN MOUNTNAME'''
    if t[2] == "id":
        t[0] = ["id", t[4]]
    elif t[2] == "type":
        t[0] = ["type", t[4]]
    elif t[2] == "fs":
        t[0] = ["fs", t[4]]


def p_login_block(t):
    'login_block : LOGIN login_params'
    t[0] = login(t[2])

def p_login_params(t):
    '''login_params : login_params login_param
                    | login_param'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]
    
def p_login_param(t):
    '''login_param : SEPARATOR USER ASSIGN STRING
                   | SEPARATOR PASS ASSIGN STRING
                   | SEPARATOR PASS ASSIGN ID
                   | SEPARATOR PASS ASSIGN NUMBER
                   | SEPARATOR USER ASSIGN ID
                   | SEPARATOR ID_PARAM ASSIGN MOUNTNAME'''
    if t[2] == "user":
        t[0] = ["user", t[4]]
    elif t[2] == "pass":
        t[0] = ["pass", t[4]]
    elif t[2] == "id":
        t[0] = ["id", t[4]]


def p_logout_block(t):
    'logout_block : LOGOUT'
    t[0] = logout(t[1])

def p_mkgrp_block(t):
    'mkgrp_block : MKGRP mkgrp_params'
    t[0] = mkgrp(t[2])

def p_mkgrp_params(t):
    '''mkgrp_params : mkgrp_params mkgrp_param
                    | mkgrp_param'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_mkgrp_param(t):
    '''mkgrp_param : SEPARATOR NAME ASSIGN ID
                   | SEPARATOR NAME ASSIGN STRING'''
    if t[2] == "name":
        t[0] = ["name", t[4]]

def p_usr_block(t):
    'usr_block : MKUSR usr_params'
    t[0] = mkusr(t[2])

def p_usr_params(t):
    '''usr_params : usr_params usr_param
                  | usr_param'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_usr_param(t):
    '''usr_param : SEPARATOR USER ASSIGN STRING
                 | SEPARATOR USER ASSIGN ID
                 | SEPARATOR PASS ASSIGN ID
                 | SEPARATOR PASS ASSIGN STRING
                 | SEPARATOR PASS ASSIGN NUMBER
                 | SEPARATOR GRP ASSIGN ID
                 | SEPARATOR GRP ASSIGN STRING'''
    if t[2] == "user":
        t[0] = ["user", t[4]]
    elif t[2] == "pass":
        t[0] = ["pass", t[4]]
    elif t[2] == "grp":
        t[0] = ["grp", t[4]]

def p_mkdir_block(t):
    'mkdir_block : MKDIR mkdir_params'
    t[0] = mkdir(t[2])

def p_mkdir_params(t):
    '''mkdir_params : mkdir_params mkdir_param
                    | mkdir_param'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]
    
def p_mkdir_param(t):
    '''mkdir_param : SEPARATOR PATH ASSIGN PATHWITHQUOTES
                   | SEPARATOR PATH ASSIGN PATHWITHOUTQUOTES
                   | SEPARATOR R'''
    if t[2] == "path":
        t[0] = ["path", t[4]]
    elif t[2] == "r":
        t[0] = ["r", ""]

def p_mkfile_block(t):
    'mkfile_block : MKFILE mkfile_params'
    t[0] = mkfile(t[2])

def p_mkfile_params(t):
    '''mkfile_params : mkfile_params mkfile_param
                     | mkfile_param'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]
    
def p_mkfile_param(t):
    '''mkfile_param : SEPARATOR PATH ASSIGN PATHWITHQUOTES
                    | SEPARATOR PATH ASSIGN PATHWITHOUTQUOTES
                    | SEPARATOR CONT ASSIGN PATHWITHQUOTES
                    | SEPARATOR CONT ASSIGN PATHWITHOUTQUOTES
                    | SEPARATOR SIZE ASSIGN NUMBER'''
    if t[2] == "path":
        t[0] = ["path", t[4]]
    elif t[2] == "cont":
        t[0] = ["cont", t[4]]
    elif t[2] == "size":
        t[0] = ["size", t[4]]


def p_rep_block(t):
    'rep_block : REP rep_params'
    t[0] = rep(t[2])

def p_rep_params(t):
    '''rep_params : rep_params rep_param
                  | rep_param'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_rep_param(t):
    '''rep_param : SEPARATOR ID_PARAM ASSIGN MOUNTNAME
                 | SEPARATOR RUTA ASSIGN PATHWITHQUOTES
                 | SEPARATOR RUTA ASSIGN PATHWITHOUTQUOTES
                 | SEPARATOR PATH ASSIGN PATHWITHQUOTES
                 | SEPARATOR PATH ASSIGN PATHWITHOUTQUOTES
                 | SEPARATOR NAME ASSIGN ID
                 | SEPARATOR NAME ASSIGN STRING'''
    if t[2] == "id":
        t[0] = ["id", t[4]]
    elif t[2] == "ruta":
        t[0] = ["ruta", t[4]]
    elif t[2] == "name":
        t[0] = ["name", t[4]]
    elif t[2] == "path":
        t[0] = ["path", t[4]]

def p_cat_block(t):
    'cat_block : CAT cat_params'
    t[0] = cat(t[2])


def p_cat_params(t):
    '''cat_params : cat_params cat_param
                  | cat_param'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_cat_param(t):
    '''cat_param : SEPARATOR FILEN ASSIGN PATHWITHQUOTES
                 | SEPARATOR FILEN ASSIGN PATHWITHOUTQUOTES
                 | SEPARATOR FILEN ASSIGN PATHWITHQUOTES cat_param
                 | SEPARATOR FILEN ASSIGN PATHWITHOUTQUOTES cat_param'''
    if len(t) == 6:
        t[5].append(["path", t[4]])
        t[0] = t[5]
    else:
        t[0] = [["path", t[4]]]

def p_rename_block(t):
    'rename_block : RENAME rename_params'
    t[0] = rename(t[2])

def p_rename_params(t):
    '''rename_params : rename_params rename_param
                     | rename_param'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]
    
def p_rename_param(t):
    '''rename_param : SEPARATOR PATH ASSIGN PATHWITHQUOTES
                    | SEPARATOR PATH ASSIGN PATHWITHOUTQUOTES
                    | SEPARATOR NAME ASSIGN EXTENSION
                    | SEPARATOR NAME ASSIGN ID
                    | SEPARATOR NAME ASSIGN STRING'''
    if t[2] == "path":
        t[0] = ["path", t[4]]
    elif t[2] == "name":
        t[0] = ["name", t[4]]

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

input_text = '''#CREACION DE DISCOS
mkdisk -size=20 -unit=m -path=/home/archivos/Discos/Disco1.dsk
Mkdisk -unit=k -size=51200 -path=/home/archivos/DiscosDisco2.dsk -fit=BF
mkdisk -size=10 -path=/home/archivos/Discos/Disco3.dsk
mkdisk -size=51200 -path="/home/archivos/Discos/mis archivos/Disco4.dsk" -unit=K
mkdisk -size=20 -path="/home/archivos/Discos/mis archivos/Disco5.dsk" -unit=M -fit=WF
#Deberia dar error
mkdisk -param=x -s=30 -path=/home/archivos/archivos/fase1/Disco.dsk

#ELIMINACION DE DISCOS
#El primero deberia dar error
rmdisk -path=/home/archivos/Disco3.dsk
rmdisk -path=/home/Discos/Disco3.dsk
RMdisk -path="/home/archivos/Discos/mis archivos/Disco4.dsk"


#CREACION DE PARTICION
fdisk -type=P -unit=K -name=Part1 -size=7680 -path=/home/archivos/Discos/Disco1.dsk -fit=BF
#MOUNT
#Recuerden corroborar con los digitos de su carne
mount -path=/home/archivos/Discos/Disco1.dsk -name=Part1 #191a
#CREACION DE SISTEMA DE ARCHIVOS
mkfs -type=full -id=221Disco1 -fs=2fs

login -user=root -pass=123 -id=221Disco1
#CREACION DE GRUPOS
mkgrp -name=usuarios
mkgrp -name=adm
mkgrp -name=users
mkgrp -name=estudiantes

rmgrp -name=estudiantes
#CREACION DE USUARIOS
mkusr -user=noel -pass=123 -grp=usuarios
mkusr -user=carlos -pass=123 -grp=adm
mkusr -user=arturo -pass=dark -grp=users
rmusr -user=arturo

#CREACION DE CARPETAS
mkdir -path=/bin
mkdir -path=/boot
mkdir -path=/cdrom
mkdir -path=/dev
mkdir -path=/etc
mkfile -path=/home/archivos/user/docs/Tarea2.txt -size=100
mkfile -path=/home/archivos/user/docs/Tarea1.txt -size=30

mkusr -user=hany -pass=galletas -grp=users
mkusr -user=osmar -pass=123 -grp=users
mkusr -user=leonor -pass=123 -grp=users
cat -file1 =/home/archivos/user/docs/Tarea2.txt -file2=/home/archivos/user/docs/Tarea1.txt -file3=/users.txt
rename -path=/home/archivos/user/docs/Tarea2.txt -name=Tarea3.txt

rep -id=221Disco1 -path=/home/archivos/reports/reporte1_tree.png -name=tree

'''
              
commands = parser.parse(input_text)
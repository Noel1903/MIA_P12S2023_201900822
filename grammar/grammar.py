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
    'mkdir' : 'MKDIR'

}

#Tokens
tokens = [
    'SEPARATOR',#-
    'ASSIGN',#=
    'PATHWITHQUOTES',#"ruta"
    'PATHWITHOUTQUOTES',#ruta
    'MOUNTNAME',#221Disco1
    'NUMBER',
    'NEGATIVE',
    'ID',
    'STRING'
] + list(reserved.values())

t_SEPARATOR = r'-'
t_ASSIGN = r'='


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
               | mkdir_block'''
    t[0] = t[1]

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
    t[0] = ["logout"]

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
    '''usr_param : SEPARATOR USER ASSIGN ID
                 | SEPARATOR USER ASSIGN STRING
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

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

input_text = '''mkdisk -size = 10 -unit=K -path=/home/usuario/Disco2.dsk
              mkdisk -size = 25 -unit=k -path="/home/usuario 1/Disco1.dsk"
              rmdisk -path=/home/usuario/Disco2.dsk
              fdisk -size = 5 -unit = k -path = "/home/usuario 1/Disco1.dsk" -type = p -name = Partition1
              fdisk -size = 10 -unit = k -path = "/home/usuario 1/Disco1.dsk" -type = p -name = Partition2
              fdisk -size = 5 -unit = k -path = "/home/usuario 1/Disco1.dsk" -type = p -name = Partition3
              fdisk -size = 4 -unit = k -path = "/home/usuario 1/Disco1.dsk" -type = e -name = Partition4
              fdisk -size = 2000 -unit = b -path = "/home/usuario 1/Disco1.dsk" -type = l -name = PartitionL
              fdisk -size = 1900 -unit = b -path = "/home/usuario 1/Disco1.dsk" -type = l -name = PartitionL1
              fdisk -size = 50 -unit = b -path = "/home/usuario 1/Disco1.dsk" -type = l -name = PartitionL2
              fdisk -path= "/home/usuario 1/Disco1.dsk" -delete = full -name = PartitionL1
              fdisk -size = 1500 -unit = b -path = "/home/usuario 1/Disco1.dsk" -type = l -name = PartitionL1
              fdisk -add = -300 -unit = b -path = "/home/usuario 1/Disco1.dsk" -name = PartitionL1
              mount -path = "/home/usuario 1/Disco1.dsk" -name = Partition1
              mount -path = "/home/usuario 1/Disco1.dsk" -name = Partition2
              unmount -id = 221Disco2
              mkfs -type=full -id = 222Disco1 -fs = 2fs
              mkfs -type=full -id = 221Disco1 -fs = 2fs
              login -user=root -pass = 123 -id = 222Disco1
              mkgrp -name = usuarios
              mkgrp -name = usuarios2
              mkusr -user = usuario1 -pass = 123 -grp = usuarios
              mkdir -path = /home
              mkdir -path = /tmp
              mkdir -path = /home/usuario
              mkdir -path = /home/usuario/Documentos
              login -user=root -pass = 123 -id = 221Disco1
              mkgrp -name = usuariosejemplo'''
              
commands = parser.parse(input_text)
#fdisk -size = 10 -unit = b -path = "/home/usuario 1/Disco1.dsk" -type = l -name = PartitionL1


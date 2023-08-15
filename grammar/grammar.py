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
#reserved words
reserved = {
    'mkdisk' : 'MKDISK',
    'rmdisk' : 'RMDISK',
    'fdisk' : 'FDISK',
    'size' : 'SIZE',
    'path' : 'PATH',
    'unit' : 'UNIT',
    'fit' : 'FIT',
    'name' : 'NAME',
    'type' : 'TYPE',
    'delete' : 'DELETE',
    'add' : 'ADD',
}

#Tokens
tokens = [
    'SEPARATOR',
    'ASSIGN',
    'PATHWITHQUOTES',
    'PATHWITHOUTQUOTES',
    'NUMBER',
    'ID',
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

def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t    

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(),'ID')
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
               | fdisk_block'''
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
                   | SEPARATOR ADD ASSIGN ID'''
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

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()
input_text = '''mkdisk -size = 10 -unit=K -path=/home/usuario/Disco2.dsk
              mkdisk -size = 25 -unit=M -path="/home/usuario 1/Disco1.dsk"
              rmdisk -path=/home/usuario/Disco2.dsk
              fdisk -size = 2 -unit = k -path = "/home/usuario 1/Disco1.dsk" -type = p -name = Partition1'''
commands = parser.parse(input_text)


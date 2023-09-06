from  grammar.grammar import parser
print("Ingrese el comando path para leer el archivo")
line = input()
#execute -path=/home/usuario/example.txt
command = line.split("=")
path = command[1]

with open(path, 'r') as file:
    data = file.read()
    parser.parse(data)
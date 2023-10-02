from  grammar.grammar import parser
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def initial():
    return "Welcome to the server"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",port=4000)
'''print("Ingrese el comando path para leer el archivo")
line = input()
#execute -path=/home/usuario/example.txt
command = line.split("=")
path = command[1]

with open(path, 'r') as file:
    data = file.read()
    parser.parse(data)'''


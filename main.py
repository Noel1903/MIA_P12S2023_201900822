from  grammar.grammar import parser
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route("/api")
def initial():
    return "Welcome to the server"


@app.route("/carnet")
def carnet():
    return jsonify({"carnet": "201900822","nombre":"Osmar Noel Chacón Lemus"})

@app.route("/api/source", methods=['POST'])
def source():
    data = request.json['content']
    
    response = parser.parse(data)
    #print(response)
    consoleOut = ""
    for res in response:
        consoleOut += res.console
    data = {
        "data": consoleOut
    }
    return jsonify(data)

@app.route("/api/login", methods=['POST'])
def login():
    data = request.json['content']
    
    response = parser.parse(data)
    #print(response[0].status)
    sendData = {
        "status": response[0].status
    }
    return jsonify(sendData)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",port=3000)
'''print("Ingrese el comando path para leer el archivo")
line = input()
#execute -path=/home/usuario/example.txt
command = line.split("=")
path = command[1]

with open(path, 'r') as file:
    data = file.read()
    parser.parse(data)'''


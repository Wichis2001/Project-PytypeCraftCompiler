from flask import Flask, request
import json
from typing import Dict, List
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_cors import CORS
import sys
from compiler import parser_analyzer
from src.Symbol_Table.table import Table
from src.Symbol_Table.exceptions import Exceptions
from src.Symbol_Table.tree import Tree
from src.Instructions.function import Function
from src.Instructions.return_expr import Return
from src.Instructions.break_expr import Break
from src.Instructions.continue_expr import Continue
from src.Symbol_Table.generator import Generator

sys.setrecursionlimit(10000000)

app = Flask(__name__)
CORS(app)

@app.route('/prueba', methods = ["POST", "GET"])
def prueba():
    if request.method == "POST":
        entrada = request.data.decode("utf-8")
        entrada = json.loads(entrada)
        global tmp_val
        tmp_val = entrada["codigo"]
        return redirect(url_for("salida"))

@app.route('/salida')
def salida():
    genAux = Generator()
    genAux.cleanAll(); # Limpia todos los archivos anteriores
    generador = genAux.getInstance()
    global Table
    global tmp_val
    global Exceptions_
    table = {}
    stmts = parser_analyzer.parse(tmp_val)
    ast = Tree(stmts)
    TsGlobal = Table()
    ast.setGlobalTs(TsGlobal)
    parser_analyzer.add_natives(ast)

    for stmt in ast.getStatements():
            if isinstance(stmt, Function):
                stmt.interpret(ast, TsGlobal )

    for stmt in ast.getStatements():
        if not (isinstance(stmt, Function)):
            value = stmt.interpret(ast, TsGlobal)
            if isinstance(value, Exceptions):
                ast.setExceptions(value)

    Exceptions_ = ast.getExceptions()
    print('Tabla de Simbolos Global')
    global Simbolos
    Simbolos = ast.getGlobalTs().getTable()
    code = generador.getCode()
    return json.dumps(code)

@app.route('/errores')
def getErrores():
    global Exceptions_
    aux = []
    for x in Exceptions_:
        aux.append(x.toString())
    return {'valores': aux}

@app.route('/simbolos')
def getTable():
    global Simbolos
    Dic = []
    for x in Simbolos:
        aux = Simbolos[x].getValue()
        tipo = Simbolos[x].getType()
        fila = 1
        columna = 2
        if isinstance(aux, List):
            aux = getValues(aux)
            a = []
            a.append(str(x))
            a.append(str(aux))
            a.append('Array')
            a.append('Global')
            a.append(str(fila))
            a.append(str(columna))
            Dic.append(a)
        elif isinstance(aux, Dict):
            aux = getValues2(aux)
            a = []
            a.append(str(x))
            a.append(str(aux))
            a.append('Struct')
            a.append('Global')
            a.append(str(fila))
            a.append(str(columna))
            Dic.append(a)
        else:
            a = []
            a.append(str(x))
            a.append(str(aux))
            a.append(tipo)
            a.append('Global')
            a.append(str(fila))
            a.append(str(columna))
            Dic.append(a)
    return {'valores':Dic}

def getValues(anterior):
    actual = []
    for x in anterior:
        a = x.getValue()
        if isinstance(a, List):
            value = getValues(a)
            actual.append(value)
        elif isinstance(a, Dict):
            value = getValues2(a)
        else:
            actual.append(x.getValue())
    return actual

def getValues2(dict):
    val = '('
    for x in dict:
        a = dict[x].getValue()
        if isinstance(a, List):
            value = getValues(a)
            val += str(value) + ", "
        elif isinstance(a, Dict):
            value = getValues2(a)
            val += str(value) + ", "
        else:
            val += str(dict[x].getValue()) + ", "
    val = val[:-2]
    val += ")"
    return val

if __name__ ==  '__main__':
    app.run(host='0.0.0.0', debug = False, port=5000)

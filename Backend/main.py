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
from src.Instructions.interface import Interface
from src.Instructions.return_expr import Return
from src.Instructions.break_expr import Break
from src.Instructions.continue_expr import Continue
from graphviz import Graph
import uuid

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
    global Table
    global tmp_val
    global Exceptions_
    table = {}
    stmts = parser_analyzer.parse(tmp_val)
    global ast 
    ast = Tree(stmts)
    TsGlobal = Table()
    ast.setGlobalTs(TsGlobal)
    addNatives = parser_analyzer.add_natives(ast)

    for stmt in ast.getStatements():
        if isinstance(stmt, Function):
            result = stmt.testParams()
            if isinstance(result, Exceptions):
                ast.setExceptions(result)
            else:
                ast.setFunctions(stmt)
        if isinstance(stmt, Interface):
            value = stmt.interpret(ast, TsGlobal)
            if isinstance(value, Exceptions):
                ast.setExceptions(value)
            else:
                ast.addStruct(value)

    for stmt in ast.getStatements():
        if not (isinstance(stmt, Function)):
            value = stmt.interpret(ast, TsGlobal)
            if isinstance(value, Exceptions):
                ast.setExceptions(value)
            if isinstance(value, Return):
                err = Exceptions("Semantico", "Return fuera de ciclo", stmt.row, stmt.column)
                ast.setExcepciones(err)
            if isinstance(value, Break):
                err = Exceptions("Semantico", "Break fuera de ciclo", stmt.row, stmt.column)
                ast.setExcepciones(err)
            if isinstance(value, Continue):
                err = Exceptions("Semantico", "Continue fuera de ciclo", stmt.row, stmt.column)
                ast.setExcepciones(err)
    Exceptions_ = ast.getExceptions()
    print('Tabla de Simbolos Global')
    global Simbolos
    Simbolos = ast.getGlobalTs().getTable()
    console = ast.getConsole()
    return json.dumps(console)

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
        fila = Simbolos[x].getRow()
        columna = Simbolos[x].getColumn()
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

@app.route('/graficar')
def getGraph():
    global ast 
    try:
        if len(ast.getExceptions()) > 0:
            return {'Error': 'There are errors in the code'}
        dot = Graph(filename='./static/ast.gv')
        dot.attr(splines='false')
        dot.node_attr.update(
            shape='box',
            stype='filled',
            fontname='Comic Sans Ms',
            color='black',
            fontcolor='black'
        )
        dot.edge_attr.update(color='red')
        graph_stmt(ast.getStatements(), dot)
        dot.render()
    except:
        return {'Error': "Can't parse code", 'Valor': ast.getExceptions()}
    else:
        return {'url': 'http://localhost:5000/static/ast.gv.pdf'}
        
        
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

def graph_stmt(stmt_list, root):
    stmts_id = str(uuid.uuid4())
    root.node(stmts_id, "AST")
    prevId = stmts_id
    
    for stmt in stmt_list:
        stmt_id = stmt.graph(root)
        root.edge(prevId, stmt_id)
        prevId = stmt_id
        
    return stmts_id

if __name__ ==  '__main__':
    app.run(host='0.0.0.0', debug = False, port=5000)


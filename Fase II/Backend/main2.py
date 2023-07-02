""" from flask import Flask
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/saluedo', methods = ['GET'])
def saludo():
    return "Hola Mundo" """
    
from compiler import parser_analyzer
from src.Symbol_Table.table import Table
from src.Symbol_Table.exceptions import Exceptions
from src.Symbol_Table.tree import Tree
from src.Instructions.function import Function
from src.Instructions.return_expr import Return
from src.Symbol_Table.generator import Generator
import sys
sys.setrecursionlimit(10000000)
global table
table = {}
entrada = '''
let val1:number = 1;
let val2:number = 10;
let val3:number = 2021.2020;

console.log("Probando declaracion de variables \\n");
console.log(val1, " ", val2, " ", val3);
console.log("---------------------------------");

val1 = val1 + 41 - 123 * 4 / (2 + 2 * 2) - (10 + (125 % 5)) * 2 ^ 2;
val2 = 11 * (11 % (12 + -10)) + 22 / 2;
val3 = 2 ^ (5 * 12 ^ 2) + 25 / 5;
console.log("Probando asignación de variables y aritmeticas");
console.log(val1, " ", val2, " ", val3);
console.log("---------------------------------");
'''
genAux = Generator()
genAux.cleanAll(); # Limpia todos los archivos anteriores
generador = genAux.getInstance()

stmts = parser_analyzer.parse(entrada)
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

#global Symbol
#Symbol = ast.getGlobalTs().getTable()
print(ast.getFunctions(), 'yuhuuuuuuuuuuuuuuuuuuuuuuuuu')
print (generador.getCode())
print('\n')
for err in ast.getExceptions():
    print(err.toString())
#console = str(ast.getConsole())
#print(TsGlobal.getTable())
#print('Console :', console)

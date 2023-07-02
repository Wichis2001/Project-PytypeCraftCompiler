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
from src.Instructions.interface import Interface
import uuid
import sys
sys.setrecursionlimit(10000000)

global table
table = {}
entrada = '''
let array = [32, 21, 7, 89, 56, 909, 109, 2];

console.log("=======================================================================");
console.log("==================================IF===================================");
console.log("=======================================================================");

if (array[4] > 50){
    console.log("IF CORRECTO");
} else if (array[4] === 56) {
    console.log("IF INCORRECTO");
} else {
    console.log("IF INCORRECTO");
};

console.log("");
console.log("=======================================================================");
console.log("=============================IFs ANIDADOS==============================");
console.log("=======================================================================");
let aux:number = 10;
if (aux > 0){
    console.log("PRIMER IF CORRECTO");
    if (true && (aux === 1)){
        console.log("SEGUNDO IF INCORRECTO");
    } else if (aux > 10){
        console.log("SEGUNDO IF INCORRECTO");
    } else{
        console.log("SEGUNDO IF CORRECTO");
    };
} else if (aux <= 3){
    console.log("PRIMER IF INCORRECTO");
    if (true && (aux === 1)){
        console.log("SEGUNDO IF INCORRECTO");
    } else if (aux > 10){
        console.log("SEGUNDO IF INCORRECTO");
    } else {
        console.log("SEGUNDO IF CORRECTO");
    };
} else if (aux === array[4]){
    console.log("PRIMER IF INCORRECTO");
    if (true && (aux === 1)){
        console.log("SEGUNDO IF INCORRECTO");
    } else if (aux > 10){
        console.log("SEGUNDO IF INCORRECTO");
    } else {
        console.log("SEGUNDO IF CORRECTO");
    };
};

console.log("");
console.log("=======================================================================");
console.log("=================================WHILE=================================");
console.log("=======================================================================");

let index: number;
index = 0;
while (index >= 0) {
    if (index === 0) {
        index = index + 100;
    } else if (index > 50) {
        index = index / 2 - 25;
    } else { 
        index = (index / 2) - 1;
    }
}
console.log(index);


console.log("");
console.log("=======================================================================");
console.log("================================WHILE-2================================");
console.log("=======================================================================");

index= -2;
index = index + 1;

while (index !== 12) {
    index = index + 1;
    
    if (index === 0 || index === 1 || index === 11 || index === 12) {
        console.log("*********************************************************************************************************");
    }else if (index === 2) {
        console.log("**********  ***************  ******                 ******                 ******              **********");
    }else if (index >= 3 && index <= 5) {
        console.log("**********  ***************  ******  *********************  *************  ******  **********************");
    }else if (index === 6) {
        console.log("**********  ***************  ******                 ******                 ******  **********************");
    } else if (index >= 7 && index <= 9) {
        console.log("**********  ***************  ********************   ******  *************  ******  **********************");
    } else if (index === 10) {
        console.log("**********                   ******                 ******  *************  ******              **********");
    };
};

console.log("");
console.log("=======================================================================");
console.log("=============================TRANSFERENCIA=============================");
console.log("=======================================================================");

let a:number = -1;
while (a < 5){
    a = a + 1;
    if (a === 3){
        console.log("a");
        continue;
    } else if (a === 4){
        console.log("b");
        break;
    };
    console.log("El valor de a es: ", a, ", ");
};

console.log("Se debió imprimir");

console.log("");
console.log("=======================================================================");
console.log("==================================FOR==================================");
console.log("=======================================================================");

for (let i=0; i<=9; i++){
    let output = "";
    for (let j =0; j<10; j++){
        output = output + " ";
    };

    for (let k =0; k<10; k++ ){
        output = output + "* ";
    };


    console.log(output);

};

console.log("");
console.log("=======================================================================");
console.log("=================================FOR-2=================================");
console.log("=======================================================================");

let arr = [1,2,3,4,5,6];
for (let t of [1,2,3,4,5,6]){
    console.log(arr[t] === 1, arr[t] === 2, arr[t] === 3, arr[t] === 4, arr[t] === 5, arr[t] === 6);
};

console.log("");
console.log("=======================================================================");
console.log("=================================FOR-3=================================");
console.log("=======================================================================");
for (let e of [1,2,3,4,5,6]){
    if(length(arr) > e){
        console.log(e+arr[e],e+arr[e],e+arr[e],e+arr[e],e+arr[e],e+arr[e]);
    };
};

console.log("");
console.log("=======================================================================");
console.log("=================================FOR-4=================================");
console.log("=======================================================================");
for (let letra of "Calificacion de Intermedio"){
    console.log(letra);
};
'''

stmts = parser_analyzer.parse(entrada)
ast = Tree(stmts)
TsGlobal = Table()
ast.setGlobalTs(TsGlobal)
parser_analyzer.add_natives(ast)

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
    if not isinstance(stmt, Function) and not isinstance(stmt, Interface):
        value = stmt.interpret(ast, TsGlobal)
        if isinstance(value, Exceptions):
            ast.setExceptions(value)


#global Symbol
#Symbol = ast.getGlobalTs().getTable()
print(ast.getConsole())
for err in ast.getExceptions():
    print(err.toString())
#console = str(ast.getConsole())
#print(TsGlobal.getTable())
#print('Console :', console)
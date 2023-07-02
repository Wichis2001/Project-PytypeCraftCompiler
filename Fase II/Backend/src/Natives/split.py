from src.Instructions.function import Function
from src.Symbol_Table.exceptions import Exceptions

class Split(Function):
    
    def __init__(self, _id, params, _type, statements, row, column):
        super().__init__(_id, params, _type, statements, row, column)
        
    def interpret(self, tree, table):
        symbol_1 = table.getTableEnv('text')
        symbol_2 = table.getTableEnv('split_caracter') 
        if symbol_1 == None or symbol_2 == None:
            message = 'One of the parameters not found'
            return Exceptions('Semantyc', message, self.row, self.column)
        return symbol_1.getValue().split(symbol_2.getValue())
    
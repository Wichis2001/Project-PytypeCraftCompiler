from src.Instructions.function import Function
from src.Symbol_Table.exceptions import Exceptions

class ToFixed(Function):
    
    def __init__(self, _id, params, _type, statements, row, column):
        super().__init__(_id, params, _type, statements, row, column)
        
    def interpret(self, tree, table):
        symbol_1 = table.getTableEnv('base_number')
        symbol_2 = table.getTableEnv('fixed_number')
        if symbol_1 == None or symbol_2 == None:
            message = 'One of the parameters not found'
            return Exceptions('Semantyc', message, self.row, self.column)
        return round(symbol_1.getValue(), symbol_2.getValue())        
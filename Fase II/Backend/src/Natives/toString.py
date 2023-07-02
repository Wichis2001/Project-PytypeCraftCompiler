from src.Instructions.function import Function
from src.Symbol_Table.exceptions import Exceptions

class ToString(Function):
    
    def __init__(self, _id, params, _type, statements, row, column):
        super().__init__(_id, params, _type, statements, row, column)
        
    def interpret(self, tree, table):
        symbol = table.getTableEnv('value')
        if symbol == None:
            message = 'One of the parameters not found'
            return Exceptions('Semantyc', message, self.row, self.column)
        self._type = 'string'
        symbol.setType('string')
        return str(symbol.getValue())
    
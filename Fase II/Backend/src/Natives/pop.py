from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
import copy

class Pop(Abstract):
    
    def __init__(self, _id, row, column):
        self._id = _id
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        symbol = table.getTableEnv(self._id)
        message = 'The variable "' + self._id + '" not exist'
        if symbol != None:
            if isinstance(symbol.getValue(), Symbol):
                symbol = symbol.getValue()
            value = symbol.getValue()
            if not isinstance(value, list):
                message = 'Variable value is not iterable'
            else:
                if len(value) != 0:
                    value.pop()
                return value
        return Exceptions('Semantyc', message, self.row, self.column)
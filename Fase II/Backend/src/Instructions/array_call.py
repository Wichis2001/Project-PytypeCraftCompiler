from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol

class Array_Call(Abstract):
    
    def __init__(self, _id, locate_value, row, column):
        self._type = None
        self._id = _id
        self.locate_value = locate_value
        self.value = None
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        symbol = table.getTableEnv(self._id)
        if not isinstance(symbol.getValue(), list):
            message = 'ID: ' + self._id + ' is not an array'
            return Exceptions('Semantyc', message, self.row, self.column)
        self.value = self.searchValue(symbol.getValue(), self.locate_value)
        symbol = Symbol(self._id, 'any', self.value, self.row, self.column)
        self._type = symbol.getType()
        return self.value
        
        
    def searchValue(self, value, locate):
        for item in locate:
            if len(value) > item and isinstance(value, list):
                value = value[item]
            else:
                return Exceptions('Semantyc', 'List index out of range', self.row, self.column)
        return value
    
    def getType(self):
        return self._type
        
                 
        
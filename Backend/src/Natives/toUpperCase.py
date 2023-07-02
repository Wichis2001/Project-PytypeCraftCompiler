from src.Instructions.function import Function
from src.Symbol_Table.exceptions import Exceptions
import uuid

class ToUpperCase(Function):
    
    def __init__(self, _id, params, _type, statements, row, column):
        self._ids = None
        self.value = None
        super().__init__(_id, params, _type, statements, row, column)
        
    def interpret(self, tree, table):
        symbol = table.getTableEnv('upper_string')
        if symbol == None:
            message = 'One of the parameters not found'
            return Exceptions('Semantyc', message, self.row, self.column)
        if symbol.getValueType() != 'string':
            return Exceptions('Semantyc', 'Wrong data type', self.row, self.column)
        self._type = symbol.getType()
        self._ids = symbol.getValue()
        self.value = self._ids.upper()
        return self.value
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, 'toUpperCase')
        root.edge(_id, self._ids)
        root.edge(_id, self.value)
        return _id
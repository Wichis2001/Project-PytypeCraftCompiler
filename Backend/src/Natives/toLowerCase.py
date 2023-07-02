from src.Instructions.function import Function
from src.Symbol_Table.exceptions import Exceptions
import uuid

class ToLowerCase(Function):
    
    def __init__(self, _id, params, _type, statements, row, column):
        self.current = None
        self.value = None
        super().__init__(_id, params, _type, statements, row, column)
        
    def interpret(self, tree, table):
        symbol = table.getTableEnv('lower_string')
        if symbol == None:
            message = 'One of the parameters not found'
            return Exceptions('Semantyc', message, self.row, self.column)
        if symbol.getValueType() != 'string':
            return Exceptions('Semantyc', 'Wrong data type', self.row, self.column)
        self._type = symbol.getType()
        self.current = symbol.getValue()
        self.value = self.current.lower()
        return self.value
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, 'lower')
        root.edge(_id, self.current)
        root.edge(_id, self.value)
        return _id
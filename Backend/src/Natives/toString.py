from src.Instructions.function import Function
from src.Symbol_Table.exceptions import Exceptions
import uuid

class ToString(Function):
    
    def __init__(self, _id, params, _type, statements, row, column):
        self.current = None
        self.value = None
        super().__init__(_id, params, _type, statements, row, column)
        
    def interpret(self, tree, table):
        symbol = table.getTableEnv('value')
        if symbol == None:
            message = 'One of the parameters not found'
            return Exceptions('Semantyc', message, self.row, self.column)
        self._type = 'string'
        symbol.setType('string')
        self.current = symbol.getValue()
        self.value = str(self.current)
        return self.value
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, 'toString')
        root.edge(_id, self.current)
        root.edge(_id, self.value)
        return _id
        
    
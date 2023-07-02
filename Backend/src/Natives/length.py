from src.Instructions.function import Function
from src.Symbol_Table.exceptions import Exceptions
from src.Symbol_Table.symbol import Symbol
import uuid

class Length(Function):
    
    def __init__(self, _id, params, _type, statements, row, column):
        self.item = None
        self.value = None
        super().__init__(_id, params, _type, statements, row, column)
        
    def interpret(self, tree, table):
        symbol = table.getTableEnv('array')
        value = symbol.getValue()
        if isinstance(value, Symbol):
            value = value.getValue()
        if isinstance(value, list) or isinstance(value, str):
            self.item = value
            self.value = len(value)
            return len(value)
        else:
            message = 'Cannot calculate length of value'
            return Exceptions('Semantyc', message, self.row, self.column)
        
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, 'lenght')
        root.edge(_id, self.item)
        root.edge(_id, self.value)
        return _id
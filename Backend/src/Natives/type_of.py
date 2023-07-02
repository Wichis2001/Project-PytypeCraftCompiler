from src.Instructions.function import Function
from src.Symbol_Table.exceptions import Exceptions
from src.Symbol_Table.symbol import Symbol
import uuid

class Type_Of(Function):
    
    def __init__(self, _id, params, _type, statements, row, column):
        self.value = None
        super().__init__(_id, params, _type, statements, row, column)
        
    def interpret(self, tree, table):
        symbol = table.getTableEnv('item')
        value = symbol.getValue()
        if isinstance(value, Symbol):
            value = value.getValue()
        self.value = self.det_Value_Type(value)
        return self.value
        
    def det_Value_Type(self, value):
        if isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, (int, float)):
            return 'number'
        elif isinstance(value, str):
            return 'string'
        elif value == None:
            return 'null'
        elif isinstance(value, list):
            return 'array'
        elif isinstance(value, dict):
            return 'interface'
        else:
            return 'any'
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, 'typeof')
        root.edge(_id, 'item')
        root.edge(_id, self.value)
        return _id
        
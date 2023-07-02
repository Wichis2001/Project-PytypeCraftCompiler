from src.Instructions.function import Function
from src.Symbol_Table.exceptions import Exceptions
import uuid

class ToExponential(Function):
    
    def __init__(self, _id, params, _type, statements, row, column):
        self.values = []
        self.ret = None
        super().__init__(_id, params, _type, statements, row, column)
        
    def interpret(self, tree, table):
        symbol_1 = table.getTableEnv('base_number')
        symbol_2 = table.getTableEnv('exponential_number')
        if symbol_1 == None or symbol_2 == None:
            message = 'One of the parameters not found'
            return Exceptions('Semantyc', message, self.row, self.column)
        self.values.append(symbol_1.getValue())
        self.values.append(symbol_2.getValue())
        self.ret = "{:.{}e}".format(symbol_1.getValue(), symbol_2.getValue())
        return "{:.{}e}".format(symbol_1.getValue(), symbol_2.getValue()) 
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, 'toExponential')
        left = str(uuid.uuid4())
        root.node(left, '()')
        root.edge(left, self.values[0])
        root.edge(left, self.values[1])
        root.edge(_id, left)
        root.edge(_id, self.ret)
        return _id 
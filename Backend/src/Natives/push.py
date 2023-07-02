from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
import uuid
import copy

class Push(Abstract):
    
    def __init__(self, _id, value, row, column):
        self._id = _id
        self.value = value
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
                expr = self.value.interpret(tree, table)
                if isinstance(expr, Exceptions):
                    return expr
                expr_type = self.value.getType()
                symbol_type = symbol.getValueType()[0]
                isAnyVar = not isinstance(symbol.getType, list) and symbol.getType() == 'any'
                isAnyArray = isinstance(symbol.getType(), list) and symbol.getType()[0] == 'any'
                if expr_type == symbol_type or isAnyVar or isAnyArray:
                    value.append(expr)
                    return None
                else:
                    message = 'Cannot add "' + expr + '" to array'
        return Exceptions('Semantyc', message, self.row, self.column)
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, '.')
        root.edge(_id, self._id)
        push_id = str(uuid.uuid4())
        root.node(push_id, 'pop')
        root.edge(push_id, self.value.graph(root))
        root.edge(_id, push_id)
        return _id
    
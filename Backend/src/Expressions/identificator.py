from ..Symbol_Table.exceptions import Exceptions
from ..Abstract.abstract import Abstract
import uuid

class Identificator(Abstract):
    
    def __init__(self, _id, row, column):
        self._id = _id
        self._type = None
        self.row = row
        self.column = column
        self.value = None
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        symbol = table.getTableEnv(self._id)
        if symbol == None:
            message = 'Variable "' + self._id + '" is no defined'
            return Exceptions('Error', message, self.row, self.column)
        self._type = symbol.getValueType()
        value = symbol.getValue()
        if isinstance(value, list) or isinstance(value, dict):
            return symbol
        self.value = value
        return value
    
    def getType(self):
        return self._type
    
    def getId(self):
        return self._id 
        
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, str(self.value))
        return _id
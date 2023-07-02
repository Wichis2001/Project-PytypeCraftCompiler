from ..Abstract.abstract import Abstract
import uuid

class Primitive(Abstract):
    
    def __init__(self, _type, value, row, column):
        self._type = _type
        self.value = value
        self.row = row
        self.column = column
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        return self.value
    
    def getType(self):
        return self._type
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, str(self.value))
        return _id

from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Instructions.interface_id import Interface_Id
import uuid

class Array_Id(Abstract):
    
    def __init__(self, _type, dimension, row, column):
        self._type = _type
        self.dimension = dimension
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        if isinstance(self._type, Interface_Id):
            self._type = self._type.interpret(tree, table)
        return self._type
    
    def getDimension(self):
        return self.dimension
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, '[]')
        _type = self._type
        dim = self.dimension
        root.edge(_id, _type)
        root.edge(_id, dim)
        return _id
            
            
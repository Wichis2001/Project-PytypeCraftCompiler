from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Instructions.interface_id import Interface_Id

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
            
            
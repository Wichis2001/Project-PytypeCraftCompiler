from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
import uuid

class Interface_Id(Abstract):
    
    def __init__(self, _id, row, column):
        self._id = _id
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        struct = tree.searchStruct(self._id)
        if struct == None:
            message = '"' + self._id + '" is an undefined struct'
            return Exceptions('Semantyc', message, self.row, self.column)   
        return self._id
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, 'Id_Struct')
        root.edge(_id, self._id)
        return _id
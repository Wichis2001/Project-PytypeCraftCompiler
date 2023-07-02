from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions

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
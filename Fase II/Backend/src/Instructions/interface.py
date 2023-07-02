from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Instructions.interface_id import Interface_Id
from ..Symbol_Table.table import Table

class Interface(Abstract):
    
    def __init__(self, _id, atributes, row, column):
        self._id = _id
        self.atributes = atributes
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        values = {}
        for atribute in self.atributes:
            temp = {}
            _id = atribute['_id']
            _type = atribute['_type']
            if isinstance(_type, Interface_Id):
                _type = _type.interpret(tree, table)
            if isinstance(_type, Exceptions):
                return _type
            temp['_type'] = _type
            values[_id] = temp
        return {'_id': self._id, 'cont': values}
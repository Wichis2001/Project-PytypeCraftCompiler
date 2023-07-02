from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Instructions.interface_id import Interface_Id
from ..Symbol_Table.table import Table
import uuid

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
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        firs_atrb = self.atributes[0]['_id']
        prev_id = _id
        if len(self.atributes[1:]) > 0:
            for atrb in self.atributes:
                new_id = str(uuid.uuid4())
                root.node(new_id, ';')
                root.edge(prev_id, new_id)
                root.edge(new_id, atrb['_id'])
                prev_id = new_id
        root.node(_id, '{}')
        root.edge(_id, self._id)
        return _id
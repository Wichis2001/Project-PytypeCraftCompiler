from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
import uuid

class Interface_Atrb_Value(Abstract):
    
    def __init__(self, _id, _id_atrb, row, column):
        self._id = _id
        self._id_atrb = _id_atrb
        self._type = None
        self.value = None
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        message = 'The variable "' + self._id + '" is not defined'
        symbol = table.getTableEnv(self._id)
        if symbol != None:
            current_value = symbol.getValue() 
            current_type = None
            exist = True
            for _id in self._id_atrb:
                if isinstance(current_value, Symbol):
                    current_value = current_value.getValue()
                current_value = current_value.get(_id, None)
                if current_value == None:
                    message = f'The attribute {_id} does not exist in the struct'
                    exist = False
                    break
                else: 
                    current_type = current_value.get('_type')
                    current_value = current_value.get('value')
            if exist == True:
                self._type = current_type
                self.value = current_value
                return current_value
        return Exceptions('Semantyc', message, self.row, self.column)
    
    def getType(self):
        return self._type
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        first_element = self._id.graph(root)
        prev_id = _id
        for _ids in self._id_atrb:
            new_id = str(uuid.uuid4())
            root.node(new_id, '.')
            root.edge(prev_id, new_id)
            root.edge(new_id, _ids)
            prev_id = new_id
        new_id = str(uuid.uuid4())
        root.node(new_id, self.value)
        root.edge(prev_id, new_id)
        root.node(_id, '.')
        root.edge(_id, first_element)
        return _id
            
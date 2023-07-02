from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol

class Interface_Atrb_Value(Abstract):
    
    def __init__(self, _id, _id_atrb, row, column):
        self._id = _id
        self._id_atrb = _id_atrb
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        message = None
        symbol = table.getTableEnv(self._id)
        if symbol != None:
            current_value = symbol.getValue()
            if isinstance(current_value, Symbol):
                current_value = current_value.getValue()
            if isinstance(current_value, dict):
                existAtrb = current_value.get(self._id_atrb, None)
                if existAtrb != None:
                    return existAtrb.get('value')
                else:
                    message = 'The attribute "' + self._id_atrb + '" does not exist in the struct'
            else:
                message = 'The variable "' + symbol.getId() + '" does not store an interface instance'
        else:
            message = 'The variable "' + self._id + '" is not defined'
        return Exceptions('Semantyc', message, self.row, self.column)
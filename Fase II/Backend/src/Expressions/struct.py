from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.table import Table

class Struct(Abstract):

    def __init__(self, _id, row, column, parameters):
        self._id = _id
        self.parameters = parameters
        self.row = row
        self.column = column
        self._type = "null"
        super().__init__(row, column)

    def interpret(self, tree, table):
        struct = table.getTableEnv( self._id)
        if struct == None:
            message = 'The interface entered has not been defined "' + str( struct ) + '"'
            return Exceptions('Semantyc', message, self.row, self.column)
        keys = []
        for key in self.parameters:
            keys.append(key)
        value = self.getValues(struct.getValue(), keys)
        return value

    def getValues(self, previous, keys):
        actual = previous
        for key in keys:
            try:
                self._type = actual[(str(key))].getType()
                actual = actual[str(key)].getValue()
            except:
                message = 'The interface entered has not been defined "' + str( key ) + '"'
                return Exceptions('Semantyc', message, self.row, self.column)
        return actual

    def getType(self):
        return self._type

from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol


class Interface_Assign(Abstract):

    def __init__(self, _id, row, column, parameters, value):
        self._id = _id
        self.parameters = parameters
        self.value = value
        self._type = 'null'
        super().__init__(row, column)

    def interpret(self, tree, table):
        struct  = table.getTableEnv( self._id )
        if struct == None:
            message = 'The interface entered has not been defined "' + str( struct ) + '"'
            return Exceptions('Semantyc', message, self.row, self.column)
        else:
            value = self.value.interpret( tree, table )
            if isinstance( value, Exceptions ): return value
            keys = []
            for params in self.parameters:
                keys.append(str(params))
            symbol = Symbol(self._id, self.value._type, value, self.row, self.column)
            result = table.updateStruct( symbol, keys )
            #if isinstance( result, Exceptions ): return result
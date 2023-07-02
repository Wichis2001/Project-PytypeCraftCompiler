from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
from ..Expressions.primitive import Primitive

class Typed_Var(Abstract):
    
    def __init__(self, _id, _type, value, row, column):
        self._id = _id
        self._type = _type
        self.value = value
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        if self._type not in ['number', 'boolean', 'string', 'any', 'null']:
            if table.getTableEnv(self._type) == None:
                message = 'El tipo "' + self._type + '" no existe'
                return Exceptions('Semantyc', message, self.row, self.column)
        if table.getTableSearch(self._id) == None:
            if self.value == None:
                self.changeValueIsNone()
            expr = self.value.interpret(tree, table)
            if isinstance(expr, Exceptions):
                return expr
            isOfSomeKind = self._type in [self.value.getType(), 'any']
            isNullValue = self.value.getType() == 'null'
            isAnAnyArray = self._type == 'any[]' and isinstance(expr, list)
            isAnAnyDimArray = 'any' in self._type and self._type.count('[]') == self.value.getType().count('[]')
            isAnEmptyArray = '[]' in self._type and self.value.getType() == 'empty[]'
            if isOfSomeKind or isNullValue or isAnAnyArray or isAnEmptyArray or isAnAnyDimArray:
                symbol = Symbol(str(self._id), self._type, expr, self.row, self.column)
                result = table.setTable(symbol)
                if isinstance(result, Exceptions):
                    return result
                return None
            else:
                message = 'Distinct data type → Requires: ' + self._type + ', Sent: ' + self.value.getType() 
                return Exceptions("Semantyc:", message, self.row, self.column)
        else:
            return Exceptions("Semantyc:", 'The variable was already defined', self.row, self.column)

    def changeValueIsNone(self):
        new_value = None
        if self._type == 'number':
            new_value = 0
        elif self._type in ['string', 'any']:
            new_value = ''
        self.value = Primitive(self._type, new_value, self.row, self.column)

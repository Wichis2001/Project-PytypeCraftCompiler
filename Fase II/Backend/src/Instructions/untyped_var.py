from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
from ..Expressions.primitive import Primitive

class Untyped_Var(Abstract):
    
    def __init__(self, _id, value, row, column):
        self._id = _id
        self._type = 'any'
        self.value = value
        self.row = row
        self.column = column
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        if table.getTableSearch(self._id) == None:
            if self.value == None:
                new_value = ''
                self.value = Primitive(self._type, new_value, self.row, self.column)
            expr = self.value.interpret(tree, table)
            if isinstance(expr, Exceptions):
                return expr
            symbol = Symbol(str(self._id), self._type, expr, self.row, self.column)
            result = table.setTable(symbol)
            if isinstance(result, Exceptions):
                return result
            return None
        else:
            return Exceptions("Semantyc:", 'The variable was already defined', self.row, self.column)
             
            
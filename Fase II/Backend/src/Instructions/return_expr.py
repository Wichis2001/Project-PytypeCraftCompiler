from src.Abstract.abstract import Abstract
from src.Symbol_Table.exceptions import Exceptions
from src.Symbol_Table.table import Table

class Return(Abstract):
    
    def __init__(self, expr, row, column):
        self.expr = expr
        self.value = None
        self._type = None
        self.trueLbl = ''
        self.falseLbl = ''
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        if self.expr == None:
            message = 'Expression expected in return statement'
            return Exceptions('Semantyc', message, self.row, self.column)
        value = self.expr.interpret(tree, table)
        if isinstance(value, Exceptions):
            return value
        self._type = value.getType()
        self.value = value.getValue()
        if self._type == 'boolean':
            self.trueLbl = value.getTrueLbl()
            self.falseLbl = value.getFalseLbl()
        return self
    
    def getValue(self):
        return self.value
    
    def getType(self):
        return self._type
    
    def getTrueLbl(self):
        return self.trueLbl
    
    def getFalseLbl(self):
        return self.falseLbl
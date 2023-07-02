from src.Abstract.abstract import Abstract
from src.Symbol_Table.exceptions import Exceptions
from src.Symbol_Table.table import Table
import uuid

class Return(Abstract):
    
    def __init__(self, expr, row, column):
        self.expr = expr
        self.value = None
        self._type = None
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        if self.expr == None:
            message = 'Expression expected in return statement'
            return Exceptions('Semantyc', message, self.row, self.column)
        value = self.expr.interpret(tree, table)
        if isinstance(value, Exceptions):
            return value
        self._type = self.expr.getType()
        self.value = value
        return self
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, 'Return')
        if self.expr:
            expr = self.expr.graph(root)
            root.edge(_id, expr)
        return _id
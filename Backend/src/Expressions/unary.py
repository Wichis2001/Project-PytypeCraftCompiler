from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
import uuid

class Unary(Abstract):
    
    def __init__(self, expr, unary_op, row, column):
        self.expr = expr
        self.unary_op = unary_op
        self._type = None
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        expr = self.expr.interpret(tree, table)
        expr_type = self.expr.getType()
        op = self.unary_op
        
        if expr_type == 'boolean' and op == '!':
            self._type = 'boolean'
            return not expr
        elif expr_type == 'number' and op == '-':
            self._type = 'number'
            return - expr
        else:
            message = 'It is not possible to operate with other types of data'
            return Exceptions('Error', message, self.row, self.column)
        
    def getType(self):
        return self._type
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, self.unary_op)
        expr = self.expr.graph(root)
        root.edge(_id, expr)
        return _id
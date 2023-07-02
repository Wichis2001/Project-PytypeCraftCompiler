from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
import uuid

class Logic(Abstract):
    
    def __init__(self, left_op, right_op, logic_op, row, column):
        self.left_op = left_op
        self.right_op = right_op
        self.logic_op = logic_op
        self._type = None
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        left = self.left_op.interpret(tree, table)
        left_type = self.left_op.getType()
        right = self.right_op.interpret(tree, table)
        right_type = self.right_op.getType()
        op = self.logic_op
        
        operations = {
            '&&': lambda left, right: left and right,
            '||': lambda left, right: left or right
        }
        
        if left_type == right_type == 'boolean':
            self._type = 'boolean'
            return operations[op](left, right)
        else:
            message = 'It is not possible to operate with other types of data'
            return Exceptions('Error', message, self.row, self.column)
        
    def getType(self):
        return self._type
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, self.logic_op)
        left_op = self.left_op.graph(root)
        right_op = self.right_op.graph(root)
        root.edge(_id, left_op)
        root.edge(_id, right_op)
        return _id
        
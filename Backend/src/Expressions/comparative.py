from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
import uuid

class Comparative(Abstract):
    
    def __init__(self, left_op, right_op, comp_op, row, column):
        self.left_op = left_op
        self.right_op = right_op
        self.comp_op = comp_op
        self._type = None
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        left = self.left_op.interpret(tree, table)
        left_type = self.left_op.getType()
        right = self.right_op.interpret(tree, table)
        right_type = self.right_op.getType()
        op = self.comp_op
        operations = {
            '<': lambda left, right: left < right,
            '>': lambda left, right: left > right,
            '<=': lambda left, right: left <= right,
            '>=': lambda left, right: left >= right,
            '===': lambda left, right: left == right,
            '!==': lambda left, right: left != right
        }
        
        if left_type == right_type and left_type in ['string', 'number', 'boolean'] or left == None or right == None:
            self._type = 'boolean'
            return operations[op](left, right)
        else:
            if isinstance(left_type, list):
                left_type = ' | '.join(left_type)
            if isinstance(right_type, list):
                right_type = ' | '.join(right_type)
            message = 'It is not possible to operate with other types of data: ' + str(left_type) + ' ↔ ' + str(right_type) + f'{left}, {right}'
            return Exceptions('Error', message, self.row, self.column)
        
    def getType(self):
        return self._type
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, self.comp_op)
        left_op = self.left_op.graph(root)
        right_op = self.right_op.graph(root)
        root.edge(_id, left_op)
        root.edge(_id, right_op)
        return _id
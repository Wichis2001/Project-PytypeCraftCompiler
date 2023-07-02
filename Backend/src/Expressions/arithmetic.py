from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
import uuid

class Arithmetic(Abstract):
    
    def __init__(self, left_op, right_op, arith_op, row, column):
        self.left_op = left_op
        self.right_op = right_op
        self.arith_op = arith_op
        self._type = None
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        left = self.left_op.interpret(tree, table)
        right = self.right_op.interpret(tree, table)
        if isinstance(left, Exceptions):
            return left
        if isinstance(right, Exceptions):
            return right
        left_type = self.left_op.getType()
        right_type = self.right_op.getType()
        op = self.arith_op
        operations = {
            '+': lambda left, right: left + right,
            '-': lambda left, right: left - right,
            '*': lambda left, right: left * right,
            '^': lambda left, right: pow(left, right),
            '/': lambda left, right: 'Error: Division by zero is not possible.' if right == 0 else left / right,
            '%': lambda left, right: 'Error: Division by zero is not possible.' if right == 0 else left % right
        }
        
        if left_type == right_type == 'number':
            self._type = 'number'
            return operations[op](left, right)
        elif left_type == right_type == 'string':
            self._type = 'string'
            return left + right
        else:
            if isinstance(left_type, list):
                left_type = ' | '.join(left_type)
            if isinstance(right_type, list):
                right_type = ' | '.join(right_type)
            message = 'It is not possible to operate with other types of data ( ' + left_type + ' ' + op + ' ' + right_type + ' )'
            return Exceptions('Semantic', message, self.row, self.column)
    
    def getType(self):
        return self._type
    
    def graph(self, root):
        _id = str(uuid.uuid4)
        root.node(_id, self.arith_op)
        left_op = self.left_op.graph(root)
        right_op = self.right_op.graph(root)
        root.edge(_id, left_op)
        root.edge(_id, right_op)
        return _id
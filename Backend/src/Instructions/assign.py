from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
from ..Expressions.primitive import Primitive
import uuid

class Assign(Abstract):
    
    def __init__(self, _id, assign_op, expr, row, column):
        self._type = None
        self._id = _id
        self.assign_op = assign_op
        self.expr = expr
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        assignation = {
            '++': lambda value, expr: value + expr,
            '--': lambda value, expr: value - expr
        }
        symbol = table.getTableEnv(self._id)
        if symbol != None:
            symbol_type = symbol.getType()
            assign_op = self.assign_op
            expr = self.expr.interpret(tree, table) 
            if isinstance(expr, Exceptions):
                return expr
            expr_type = self.expr.getType()
            expr_dim = None
            if assign_op == '=':
                isArrayExpr = isinstance(expr, list)
                if isArrayExpr:
                    expr_dim = self.expr.getDimension()
                isAnyArray = False
                if isinstance(symbol_type, list):
                    isAnyArray = symbol_type[0] == 'any' and symbol_type[1] != None and expr_dim != None and expr_dim >= symbol_type[1]
                    isSameType = symbol_type[0] == expr_type and symbol_type[1] == expr_dim
                    isEmptyArray = expr_type == 'empty' and expr_dim == symbol_type[1]
                    isArray = isArrayExpr and (isAnyArray or isSameType or isEmptyArray)
                if symbol_type in [expr_type, 'any'] or expr_type == 'null' or isArray:
                    if isArrayExpr:
                        expr_type = [expr_type, expr_dim]
                    old_type = symbol.getValueType()
                    symbol.setValue(expr)
                    if old_type != expr_type:
                        symbol.setValueType(expr_type)  
                    return symbol.getValue()
                else:
                    if isinstance(expr_type, list):
                        temp = expr_type[0]
                        for i in range(expr_type[1]):
                            temp += '[]'
                        expr_type = temp
                    if isinstance(symbol_type, list):
                        temp = symbol_type[0]
                        for i in range(symbol_type[1]):
                            temp += '[]'
                        symbol_type = temp
                    message = 'Cannot assign a value of type ' + expr_type + ' to data of type ' + symbol_type  
                    return Exceptions("Semantyc", message, self.row, self.column)
            else:
                isNumber = symbol_type == expr_type == 'number'
                isAnyNumber = symbol_type == 'any' and expr_type == symbol.getValueType() == 'number'
                if isNumber or isAnyNumber:
                    previous_value = symbol.getValue()
                    symbol.setValue(assignation[assign_op](previous_value, expr))
                    return previous_value
                else:
                    message = 'Cannot perform an assignment with operation for the data type ' + symbol.getValueType()
                    return Exceptions("Semantyc", message, self.row, self.column)
        else:
            message = 'The varaible "' + self._id + '" is not defined'
            return Exceptions("Semantyc", message, self.row, self.column)
        
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, '=')
        root.edge(_id, self._id)
        root.edge(_id, self.expr.graph(root))
        return _id
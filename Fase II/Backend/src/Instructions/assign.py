from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
from ..Expressions.primitive import Primitive

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
            symbol_type = symbol.getRealType()
            assign_op = self.assign_op
            expr = self.expr.interpret(tree, table) 
            if isinstance(expr, Exceptions):
                return expr
            expr_type = self.expr.getType()
            if assign_op == '=':
                isAnAnyArray = symbol_type == 'any[]' and isinstance(expr, list)
                isAnAnyDimArray = 'any' in symbol_type and symbol_type.count('[]') == expr_type.count('[]')
                isAnEmptyArray = '[]' in symbol_type and expr_type == 'empty[]'
                if symbol_type in [expr_type, 'any'] or expr_type == 'null' or isAnAnyArray or isAnAnyDimArray or isAnEmptyArray:
                    symbol.setValue(expr)
                    return symbol.getValue()
                else:
                    message = 'Cannot assign a value of type ' + expr_type + ' to data of type ' + symbol_type  
                    return Exceptions("Semantyc", message, self.row, self.column)
            else:
                isNumber = symbol_type == expr_type == 'number'
                isAnyNumber = symbol_type == 'any' and expr_type == symbol.getType() == 'number'
                if isNumber or isAnyNumber:
                    previous_value = symbol.getValue()
                    symbol.setValue(assignation[assign_op](symbol.getValue(), expr))
                    return previous_value
                else:
                    message = 'Cannot perform an assignment with operation for the data type ' + symbol.getType()
                    return Exceptions("Semantyc", message, self.row, self.column)
        else:
            return Exceptions("Semantyc", 'The variable is not defined', self.row, self.column)
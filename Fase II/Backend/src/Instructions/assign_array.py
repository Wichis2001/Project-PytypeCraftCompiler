from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
import copy

class Assign_Array(Abstract):
    
    def __init__(self, _id, assign_op, locate, expr, row, column):
        self._id = _id
        self.assign_op = assign_op
        self.locate = locate
        self.expr = expr
        self._type = None
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        assignation = {
            '++': lambda value, expr: value + expr,
            '--': lambda value, expr: value - expr
        }
        symbol = table.getTableEnv(self._id)
        if symbol != None:
            current_value = copy.deepcopy(symbol.getValue())
            new_value = self.expr.interpret(tree, table)
            new_value_type = self.expr.getType()
            if isinstance(new_value, Exceptions):
                return new_value
            op = self.assign_op
            result = self.changeValue(current_value, self.locate, new_value, self.assign_op)
            if isinstance(result, Exceptions):
                return result
            symbol_value = Symbol('temp', 'any', result, -1, -1)
            temp_symbol = Symbol('temp', 'any', current_value, -1, -1)
            isSameType = symbol_value.getType() == new_value_type or new_value_type == 'null'
            isEmptyArray = isinstance(result, list) and new_value == []
            isAnyArray = symbol.getRealType() in ['any', 'any[]']
            isAnyDimArray = 'any' in symbol.getRealType() and symbol.getRealType().count('[]') == temp_symbol.getType().count('[]')
            if isSameType or isAnyArray or isAnyDimArray or isEmptyArray:
                symbol.setValue(current_value)
                if op == '=':
                    return new_value
                return result
            else:
                message = 'Cannot assign a value of type ' + new_value_type + ' to data of type ' + symbol_value.getType()  
                return Exceptions("Semantyc", message, self.row, self.column)
        else:
            return Exceptions("Semantyc", 'The array is not defined', self.row, self.column)
  
    def changeValue(self, _list, index, new_value, assign_op):
        assignation = {
            '++': lambda value, expr: value + expr,
            '--': lambda value, expr: value - expr
        }
        if isinstance(_list, Symbol):
            _list = _list.getValue()
        if len(_list) <= index[0]:
            return Exceptions('Semantyc', 'List index out of range', self.row, self.column)
        else:
            if len(index) == 1:
                current_value = copy.deepcopy(_list[index[0]])
                if assign_op == '=':
                    _list[index[0]] = new_value
                elif assign_op in ['++', '--'] and isinstance(current_value, (int, float)):
                    _list[index[0]] = assignation[assign_op](_list[index[0]], new_value)
                else:
                    message = 'Cannot perform an assignment with operation for the data type'
                    return Exceptions("Semantyc", message, self.row, self.column)
                return current_value
            else:
                return self.changeValue(_list[index[0]], index[1:], new_value, assign_op)
            
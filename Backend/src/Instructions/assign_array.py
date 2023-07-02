from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
from ..Expressions.primitive import Primitive
import uuid
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
        symbol = table.getTableEnv(self._id)
        new_locate = []
        for value in self.locate:
            index = self.locate.index(value)
            if not isinstance(self.locate[index], int):
                item = value.interpret(tree, table)
                if value.getType() == 'number':
                    new_locate.append(item)
                else:
                    return Exceptions('Semantyc', 'Expected digit when calling an array value', self.row, self.column)
            else:
                item = Primitive('number', self.locate[index], self.row, self.column)
                new_locate.append(item.interpret(tree, table))
        message = ''
        if symbol != None:
            if isinstance(symbol.getValue(), Symbol):
                symbol = symbol.getValue()
            if not isinstance(symbol.getValue(), list):
                message = 'The variable does not store an array'
            else:
                expr = self.expr.interpret(tree, table)
                value = copy.deepcopy(symbol.getValue())
                if symbol.getValueType()[1] < len(self.locate):
                    message = 'The array does not have that dimension'
                else:
                    result = self.changeValue(value, new_locate, expr, self.assign_op)
                    if isinstance(result, Exceptions):
                        return result
                    if self.assign_op != '=':
                        symbol.setValue(value)
                        return result
                    else:
                        _type_new_value = self.det_Type(value)
                        symbol_type = symbol.getType()
                        if _type_new_value == symbol_type:
                            symbol.setValue(value)
                        elif not isinstance(symbol_type, list) and symbol_type == 'any':
                            self._type = _type_new_value[0]
                            symbol.setValue(value)
                        elif isinstance(symbol_type, list) and symbol_type[0] == 'any' and symbol_type[1] <= _type_new_value[1]:
                            old_type = symbol.getValueType()
                            if old_type != _type_new_value:
                                symbol.setValueType(_type_new_value)
                            self._type = _type_new_value
                            symbol.setValue(value)
                        else:
                            message = 'Invalid assignation in array'
                    if message == '':
                        return expr
        else:
            message = 'The array is not defined'
        return Exceptions('Semantyc', message, self.row, self.column)
  
    def changeValue(self, _list, index, new_value, assign_op):
        assignation = {
            '++': lambda value, expr: value + expr,
            '--': lambda value, expr: value - expr
        }
        if len(_list) <= index[0]:
            return Exceptions('Semantyc', 'List index out of range', self.row, self.column)
        if isinstance(new_value, Symbol):
            new_value = new_value.getValue()
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
            
    def det_Type(self, _list):
        dimension = 1
        _type = None
        if len(_list) == 0:
            _type = 'empty'
        else:
            areEqual = True
            value_dimension = None
            dimensions = []
            for i in range(len(_list)):
                current_expr = _list[i]
                value_type = None
                if isinstance(current_expr, list):
                    value_type = self.det_Type(current_expr)
                else:
                    value_type = self.det_Value_Type(current_expr)
                value_dimension = 0 if not isinstance(current_expr, list) else value_type[1]
                dimensions.append(value_dimension)
                if _type == None:
                    _type = value_type if not isinstance(current_expr, list) else value_type[0]
                else:
                    if isinstance(value_type, list):
                        value_type = value_type[0]
                    if value_type != _type or areEqual == False:
                        _type = 'any'
            if dimension == value_dimension and areEqual == True:
                dimension += value_dimension
        return [_type, dimension]
            
    def det_Value_Type(self, value):
        if isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, (int, float)):
            return 'number'
        elif isinstance(value, str):
            return 'string'
        elif value == None:
            return 'null'
        
    def compareElements(self, _list):
        if len(_list) == 0:
            return True
        current_item = _list[0]
        for item in _list:
            if current_item != item:
                return False
        return True
    
    def getType(self):
        return self._type
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        new_id = str(uuid.uuid4())
        prev_id = new_id
        for locate in self.locate:
            cur_id = str(uuid.uuid4())
            root.node(cur_id, '[]')
            root.node(prev_id, cur_id)
            root.edge(cur_id, locate.graph(root))
            prev_id = cur_id
        root.node(new_id, '[]')
        root.edge(new_id, self._id)
        root.node(_id, '=')
        root.edge(_id, new_id)
        root.edge(_id, self.expr.graph(root))
        return _id
            
        
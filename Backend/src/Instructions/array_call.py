from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
from ..Expressions.primitive import Primitive
import uuid
import copy

class Array_Call(Abstract):
    
    def __init__(self, _id, locate_value, row, column):
        self._type = None
        self._id = _id
        self.locate_value = locate_value
        self.value = None
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        symbol = table.getTableEnv(self._id)
        if symbol == None:
            message = f'Variable "{self._id}" is not defined'
            return Exceptions('Semantyc', message, self.row, self.column)
        new_locate_value = []
        for value in self.locate_value:
            index = self.locate_value.index(value)
            if not isinstance(self.locate_value[index], int):
                item = value.interpret(tree, table)
                if value.getType() == 'number':
                    new_locate_value.append(item)
                else:
                    return Exceptions('Semantyc', 'Expected digit when calling an array value', self.row, self.column)
            else:
                item = Primitive('number', self.locate_value[index], self.row, self.column)
                new_locate_value.append(item.interpret(tree, table))
        if isinstance(symbol.getValue(), Symbol):
            symbol = symbol.getValue()
        if not isinstance(symbol.getValue(), list):
            message = 'Variable "' + self._id + '" is not an array'
            return Exceptions('Semantyc', message, self.row, self.column)
        current_value = self.searchValue(symbol.getValue(), new_locate_value)
        self.value = current_value
        if not isinstance(self.value, list):
            self._type = self.det_type(self.value)
        else:
            self._type = self.type_list(self.value)   
        return self.value
        
        
    def searchValue(self, value, locate):
        for item in locate:
            if len(value) > item and isinstance(value, list):
                value = value[item]
            else:
                return Exceptions('Semantyc', 'List index out of range', self.row, self.column)
        return value
    
    def det_type(self, value):
        if isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, (int, float)):
            return 'number'
        elif isinstance(value, str):
            return 'string'
        elif value == None:
            return 'null'
    
    def getType(self):
        return self._type
    
    def type_list(self, _list):
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
                    value_type = self.type_list(current_expr)
                else:
                    value_type = self.det_type(current_expr)
                value_dimension = 0 if not isinstance(current_expr, list) else value_type[1]
                dimensions.append(value_dimension)
                if _type == None:
                    _type = value_type if not isinstance(current_expr, list) else value_type[0]
                else:
                    areEqual = self.compareElements(dimensions)
                    if value_type != _type or areEqual == False:
                        _type = 'any'
            if dimension == value_dimension and areEqual == True:
                dimension += value_dimension
        return [_type, dimension]
    
    def compareElements(self, _list):
        if len(_list) == 0:
            return True
        current_item = _list[0]
        for item in _list:
            if current_item != item:
                return False
        return True
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        first_element = self.locate_value[0].graph(root)
        prev_id = _id
        for locate_value in self.locate_value[1:]:
           new_id = str(uuid.uuid4())
           root.node(new_id, '[]')
           root.edge(prev_id, new_id)
           root.edge(new_id, locate_value.graph(root))
           prev_id = new_id
        root.node(_id, self._id)
        root.edge(_id, first_element) 
        return _id
                 
        
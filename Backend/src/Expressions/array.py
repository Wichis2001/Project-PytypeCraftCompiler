from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
import uuid

class Array(Abstract):
    
    def __init__(self, expr_list, row, column):
        self._type = None
        self.dimension = None
        self.expr_list = expr_list
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        matriz = []
        dimension = 1
        _type = None
        if len(self.expr_list) == 0:
            _type = 'empty'
        else:
            areEqual = True
            value_dimension = None
            dimensions = []
            for i in range(len(self.expr_list)):
                current_expr = self.expr_list[i]
                value = current_expr.interpret(tree, table)
                if isinstance(value, Exceptions):
                    return value
                value_type = None
                value_dimension = None
                if isinstance(value, Symbol):
                    value_type = value.getValueType()[0]
                    value_dimension = value.getValueType()[1]
                    value = value.getValue()
                else:
                    value_type = current_expr.getType()
                    value_dimension = 0 if not isinstance(value, list) else current_expr.getDimension()
                dimensions.append(value_dimension)
                if _type == None:
                    _type = value_type
                else:
                    areEqual = self.compareElements(dimensions)
                    if value_type != _type or areEqual == False:
                        print(value_type, _type)
                        _type = 'any'
                matriz.append(value)
            if dimension == value_dimension and areEqual == True:
                dimension += value_dimension
        self._type = _type
        self.dimension = dimension
        return matriz
        
    def getType(self):
        return self._type
    
    def getDimension(self):
        return self.dimension
    
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
        root.node(_id, '[]')
        first_element = self.expr_list[0].graph(root)
        prev_id = _id
        for expr in self.expr_list[1:]:
            new_id = str(uuid.uuid4())
            root.node(new_id, ',')
            root.edge(prev_id, new_id)
            root.edge(new_id, expr.graph(root))
            prev_id = new_id
        root.node(_id, '[]')
        root.edge(_id, first_element)
        return _id
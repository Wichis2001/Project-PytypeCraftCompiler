from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
from ..Expressions.primitive import Primitive
from ..Instructions.interface_id import Interface_Id
from ..Instructions.array_id import Array_Id
import uuid
import copy

class Typed_Var(Abstract):
    
    def __init__(self, _id, _type, value, row, column):
        self._id = _id
        self._type = _type
        self.value = value
        self.dimension = None
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        isArray = isinstance(self._type, Array_Id)
        if isinstance(self._type, Interface_Id) or isArray:
            _type = self._type.interpret(tree, table)
            if isinstance(_type, Exceptions):
                return _type
            else:
                if isArray:
                    self.dimension = self._type.getDimension()
                self._type = _type
        if self.value == None:
            self.changeValueIsNone()
        expr = self.value.interpret(tree, table)
        if isinstance(expr, Exceptions):
            return expr
        temp_type = None
        if isinstance(expr, Symbol):
            temp_type = expr.getValueType()
            expr = copy.deepcopy(expr.getValue())
        expr_type = self.value.getType()
        expr_dim = None
        isArrayExpr = isinstance(expr, list)
        if isArrayExpr and not isinstance(expr_type, list):
            expr_dim = self.value.getDimension()
        if isinstance(expr_type, list):
            expr_dim = expr_type[1]
            expr_type = expr_type[0]
        isAnyArray = self._type == 'any' and expr_dim != None and self.dimension != None and expr_dim >= self.dimension
        isSameType = (self._type == expr_type and expr_dim == self.dimension) or (temp_type != None and self._type == temp_type[0] and self.dimension == temp_type[1])
        isEmptyArray = self._type == 'empty' and expr_dim == self.dimension
        isArray = isArrayExpr and (isAnyArray or isEmptyArray or isSameType)
        types = None
        if not isinstance(expr_type, list):
            types = ['any', expr_type]
        else:
            types = ['any'] + expr_type
        isNullValue = expr_type == 'null'
        if (self._type in types and self.dimension == expr_dim == None) or isNullValue or isArray:
            symbol = None
            if isArrayExpr:
                expr_type = [expr_type, expr_dim]
                self._type = expr_type
            if self._type == 'any' or self._type[0] == 'any':
                symbol = Symbol(str(self._id), self._type, expr, expr_type, self.row, self.column)
            else:
                symbol = Symbol(str(self._id), self._type, expr, self._type, self.row, self.column)
            result = table.setTable(symbol)
            if isinstance(result, Exceptions):
                return result
            return None
        else:
            if isinstance(expr_type, list):
                expr_type = ' | '.join(expr_type)
            if self.dimension != None:
                for i in range(self.dimension):
                    self._type += '[]'
            if isArrayExpr:
                for i in range(expr_dim):
                        expr_type += '[]'
            message = 'Distinct data type → Requires: ' + self._type + ', Sent: ' + expr_type
            return Exceptions("Semantyc:", message, self.row, self.column)
    
    def changeValueIsNone(self):
        new_value = None
        if self._type == 'number':
            new_value = 0
        elif self._type in ['string', 'any']:
            new_value = ''
        self.value = Primitive(self._type, new_value, self.row, self.column)

    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, 'Typed_Var')
        type_id = str(uuid.uuid4())
        _id_id = str(uuid.uuid4())
        root.node(type_id, self._type)
        root.node(_id_id, self._id)
        value = self.value.graph(root)
        root.edge(type_id, _id_id)
        root.edge(_id, type_id)
        root.edge(_id, value)
        return _id
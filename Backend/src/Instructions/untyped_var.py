from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
from ..Expressions.primitive import Primitive
import uuid

class Untyped_Var(Abstract):
    
    def __init__(self, _id, value, row, column):
        self._id = _id
        self._type = 'any'
        self.value = value
        self.row = row
        self.column = column
        self.dimension = None
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        if self.value == None:
            new_value = ''
            self.value = Primitive(self._type, new_value, self.row, self.column)
        expr = self.value.interpret(tree, table)
        if isinstance(expr, Exceptions):
            return expr
        expr_type = self.value.getType()
        if isinstance(expr, list):
                expr_dim = self.value.getDimension()
                expr_type = [expr_type, expr_dim]
        symbol = Symbol(str(self._id), self._type, expr, expr_type, self.row, self.column)
        result = table.setTable(symbol)
        if isinstance(result, Exceptions):
            return result
        return None
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, 'Untyped_Var')
        type_id = str(uuid.uuid4())
        _id_id = str(uuid.uuid4())
        root.node(type_id, self._type)
        root.node(_id_id, self._id)
        value = self.value.graph(root)
        root.edge(type_id, _id_id)
        root.edge(_id, type_id)
        root.edge(_id, value)
        return _id
             
            
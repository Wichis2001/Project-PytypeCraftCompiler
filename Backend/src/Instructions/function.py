from ..Abstract.abstract import Abstract
from ..Instructions.return_expr import Return
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.table import Table
from ..Instructions.break_expr import Break
from ..Instructions.continue_expr import Continue
from ..Instructions.interface_id import Interface_Id
from ..Instructions.array_id import Array_Id
import uuid
import copy

class Function(Abstract):
    
    def __init__(self, _id, params, _type, statements, row, column):
        self._id = _id
        self.params = params
        self.statements = statements
        self._type = _type
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        if isinstance(self._type, Interface_Id) or isinstance(self._type, Array_Id):
            _type = self._type.interpret(tree, table)
            if isinstance(_type, Exceptions):
                return _type
            else:
                if isinstance(self._type, Array_Id):
                    self._type = [_type, self._type.getDimension()]
                else:
                    self._type = _type
        env = Table(table)
        for statement in self.statements:
            value = statement.interpret(tree, env)
            if isinstance(value, Exceptions):
                return value
            if isinstance(value, Return):
                types = [None, 'any', value._type] if not isinstance(value._type, list) else [None, 'any'] + value._type
                isArrayType = isinstance(self._type, list)
                isAnyRes = isArrayType and self._type[0] == 'any' and self._type[1] <= value._type[1]
                isSameArr = isArrayType and  self._type[0] == value._type[0] and self._type[1] <= value._type[1]
                isArray = isAnyRes or isSameArr
                if self._type in types or isArray:
                    if self._type == None:
                        self._type = value._type
                    return value.value
                else:
                    return Exceptions('Semantyc', 'Different data type of the function with its return', self.row, self.column)
            if isinstance(value, Break): return value
            if isinstance(value, Continue): return value
        return None
    
    
    def testParams(self):
        params = copy.deepcopy(self.params)
        if params != None:
            for param in params:
                counter = 0
                _id = param['_id']
                for par in params:
                    if _id == par['_id']:
                        counter = counter + 1
                if counter >= 2:
                    message = 'The param name "' + _id + '" in function "' + self._id + '" is already being used in another param'
                    return Exceptions('Semantyc', message, self.row, self.column)
        return None
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, 'function')
        #Lado Izquierdo
        left_id = str(uuid.uuid4())
        root.node(left_id, '()')
        root.edge(left_id, self._id)
        if self.params != None:
            temp_id = str(uuid.uuid4())
            first = self.params[0]['_id']
            root.node(temp_id, first)
            for param in self.params[1:]:
                new_id = str(uuid.uuid4())
                root.node(new_id, ',')
                root.edge(temp_id, new_id)
                root.edge(new_id, param['_id'])
                temp_id = new_id
            root.edge(left_id, temp_id)
        #Lado Derecho
        right_id = str(uuid.uuid4())
        root.node(right_id, '{}')
        first_stmt = self.statements[0].graph(root)
        cur_id = str(uuid.uuid4())
        root.edge(right_id, cur_id)
        for stmt in self.statements[1:]:
            new_id = str(uuid.uuid4())
            root.node(new_id, ';')
            root.edge(cur_id, new_id)
            root.edge(new_id, stmt.graph(root))
            cur_id = new_id
        root.edge(_id, left_id)
        root.edge(_id, right_id)
        return _id
from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
from ..Symbol_Table.table import Table
from ..Instructions.interface_id import Interface_Id
from ..Instructions.array_id import Array_Id
import uuid

class Function_Call(Abstract):
    
    def __init__(self, _id, params, row, column):
        self._id = _id
        self.params = params
        self._type = None
        self.value = None
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        result = tree.getFunction(self._id)
        if result == None:
            message = 'The function "' + self._id + '" has not been defined.'
            return Exceptions('Semantyc', message, self.row, self.column)
        env = Table(tree.getGlobalTs())
        if result.params == None and self.params != None:
            message = 'The function "' + self._id + '" does not require parameters'
            return Exceptions('Semantyc', message, self.row, self.column)
        elif result.params != None and self.params == None:
            message = 'The function "' + self._id + '" requires params'
            return Exceptions('Semantyc', message, self.row, self.column)
        elif result.params != None and self.params != None:
            if len(self.params) == len(result.params):
                counter = 0
                for param in self.params:
                    expr = param.interpret(tree, table)
                    if isinstance(expr, Exceptions):
                        return expr
                    expr_type = None
                    temp = None
                    if isinstance(expr, Symbol):
                        temp = expr
                        expr_type = expr.getValueType()
                        expr = expr.getValue()
                    else:
                        if isinstance(expr, list):
                            expr_type = [param._type[0], param._type[1]]
                        else:
                            expr_type = param._type 
                    types = [expr_type, 'any'] if not isinstance(expr_type, list) else ['any'] + expr_type
                    if isinstance(result.params[counter]['_type'], Interface_Id):
                        result.params[counter]['_type'] = result.params[counter]['_type'].interpret(tree, table)
                    if isinstance(result.params[counter]['_type'], Array_Id):
                        temp_type = result.params[counter]['_type'].interpret(tree, table)
                        temp_dim = result.params[counter]['_type'].getDimension()
                        result.params[counter]['_type'] = [temp_type, temp_dim]
                    tempResultType = result.params[counter]['_type']
                    isArrayExpr = isinstance(expr, list)
                    isAnyArray = isArrayExpr and temp != None and temp.getType()[0] == 'any' and tempResultType[1] <= expr_type[1]
                    isSameArray = isArrayExpr and expr_type[0] == tempResultType[0] and tempResultType[1] == expr_type[1]
                    isArray = isAnyArray or isSameArray
                    if result.params[counter]['_type'] in types or isArray:
                        symbol = Symbol(str(result.params[counter]['_id']), result.params[counter]['_type'], expr, expr_type, self.row, self.column)
                        updateT = env.setTableFunction(symbol)
                        if isinstance(updateT, Exceptions):
                            return updateT
                    else:
                        message = 'Parameters with different types'
                        return Exceptions('Semantyc', message, self.row, self.column)
                    counter += 1
            else:
                message = 'You exceeded the number of params'
                if len(self.params) < len(result.params):
                    message = 'Missin params in function "' + self._id + '"'
                return Exceptions('Semantyc', message, self.row, self.column)
        value = result.interpret(tree, env)   
        if isinstance(value, Exceptions):
            return value
        if result._type == 'void' and value != None:
            return Exceptions('Semantyc', 'Function does not support return statement', self.row, self.column)
        elif not result._type in [None, 'void', 'null'] and value == None:
            print(result._id, result._type, value)
            return Exceptions('Semantyc', 'The function requires a return statement', self.row, self.column)
        self._type = result._type
        self.value = value
        return value
    
    def getType(self):
        return self._type
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, f'{self._id}()')
        #Lado Izquierdo
        if self.params != None:
            param_id = str(uuid.uuid4())
            root.node(param_id, 'Params')
            root.edge(_id, param_id)
            
            for param in self.params:
                param_n_id = param.graph(root)
                root.edge(param_id, param_n_id)
        return _id
        
        
                

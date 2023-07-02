from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
import uuid
import copy

class Interface_Assign(Abstract):
    
    def __init__(self, _id, _ids_atrb, assign_op, value, row, column):
        self._id = _id
        self._ids_atrb = _ids_atrb
        self.assign_op = assign_op
        self.value = value 
        super().__init__(row, column)

    def interpret(self, tree, table):
        message = 'The variable "' + self._id + '" is not defined'
        assignations = {
            '++': lambda value, expr: value + expr,
            '--': lambda value, expr: value - expr
        }
        expr = self.value.interpret(tree, table)
        if isinstance(expr, Exceptions):
            return expr
        expr_type = self.value.getType()
        symbol = table.getTableEnv(self._id)
        if symbol != None:
            symbol_value = symbol.getValue()
            if isinstance(symbol_value, dict): 
                symbol_type = symbol.getType()
                op = self.assign_op
                exist = True
                current_value = symbol
                current_type = None
                for _id in self._ids_atrb:
                    if isinstance(current_value, Symbol):
                        current_value = current_value.getValue()
                    current_value = current_value.get(_id, None)
                    if current_value == None:
                        message = f'The attribute {_id} does not exist in the struct'
                        exist = False
                        break
                    else: 
                        current_type = current_value.get('_type')
                        current_value = current_value.get('value')
                if op != '=':
                    if exist == True:
                        if current_type == 'number':
                            new_value = assignations[op](current_value, expr)
                            self.changeValue(symbol, self._ids_atrb, new_value, None)
                            return current_value
                        else:
                            message = f'Cannot perform an assignment with operation for the data type {current_type}'
                else:
                    if exist == True:
                        if expr_type == current_type or expr_type in current_type:
                            return self.changeValue(symbol, self._ids_atrb, expr, None)
                        else:
                            message = 'Incompatible types'
            else:
                message = 'The variable "' + symbol.getId() + '" does not store an interface instance'
        return Exceptions("Semantyc", message, self.row, self.column)
    
    def changeValue(self, struct, _list, new_value, new_type):
        if isinstance(struct, Symbol):
                struct = struct.getValue()
        if len(_list) > 1:
            struct = struct.get(_list[0])['value']
            return self.changeValue(struct, _list[1:], new_value, new_type)
        else:
            struct[_list[0]]['value'] = new_value
            if new_type != None:
                struct[_list[0]]['_type'] = new_value
            return new_value
        
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, '=')
        temp_id = str(uuid.uuid4())
        for _ids in self._ids_atrb:
            new_id = str(uuid.uuid4())
            root.node(new_id, '.')
            root.edge(temp_id, new_id)
            root.edge(new_id, _ids)
            temp_id = new_id
        root.edge(temp_id, self._id)
        root.edge(_id, temp_id)
        root.edge(_id, self.value.graph(root))
        return _id
        

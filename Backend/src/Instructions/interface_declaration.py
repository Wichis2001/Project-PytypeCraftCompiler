from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
from ..Symbol_Table.table import Table

class Interface_Declaration(Abstract):
    
    def __init__(self, _id, row, column, variables=None):
        self._id = _id
        self.variables = variables
        self._type = 'interface'
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        if self.variables :
            dict = {}
            env = Table(table)
            for variable in self.variables:
                id_var = variable._id
                type_var = variable._type
                variable = variable.interpret(tree, env)
                if isinstance(variable, Exceptions):
                    return variable
                if type_var:
                    simbolo = Symbol("", type_var, None, self.row, self.column)
                else:
                    simbolo = Symbol("", "null", self.row, self.column)
                dict[str(id_var)] = simbolo
            symbol = Symbol(str(self._id), self._type, dict, self.row, self.column)
            table.setTable(symbol)
        return None
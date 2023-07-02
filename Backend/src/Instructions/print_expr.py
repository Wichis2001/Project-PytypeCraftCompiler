from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
import uuid

class Print_Expr(Abstract):
    
    def __init__(self, expr, row, column):
        self.expr = expr
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        final_value = None
        for expr in self.expr:
            value = expr.interpret(tree, table)
            if isinstance(value, Exceptions):
                return value
            if isinstance(value, Symbol):
                value = value.getValue()
            if isinstance(value, dict):
                interface = {}
                for key, cont in value.items():
                    interface[key] = cont.get('value')
                value = interface
            if final_value == None:
                final_value = str(value)
            else:
                final_value += ' ' + str(value) 
        tree.updateConsole(final_value)
        return None
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        fist_element = self.expr[0].graph(root)
        prev_id = _id
        if len(self.expr[1:]) > 0:
            for expr in self.expr:
                new_id = str(uuid.uuid4())
                root.node(new_id, ',')
                root.edge(prev_id, new_id)
                root.edge(new_id, expr.graph(root))
                prev_id = new_id
        root.node(_id, 'console.log')
        root.edge(_id, fist_element)
        return _id
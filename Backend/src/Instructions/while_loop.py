from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.table import Table
from ..Instructions.return_expr import Return
from ..Instructions.break_expr import Break
from ..Instructions.continue_expr import Continue
import uuid

class While(Abstract):
    
    def __init__(self, conditional, bloqueWhile, row, column):
        self.conditional = conditional
        self.bloqueWhile = bloqueWhile
        super().__init__(row, column)

    def interpret(self, tree, table):
        enviroment = Table( table )
        conditional = self.conditional.interpret( tree, enviroment )
        
        if not isinstance( conditional, bool):
            message = 'No boolean expression entered in loop while "' + str( conditional ) + '"'
            return Exceptions('Semantyc', message, self.row, self.column)
        if bool( conditional ) == True:
            breakValidator = False
            continueValidator = False
            while conditional:
                newEnv = Table( enviroment )
                for instruction in self.bloqueWhile:
                    result = instruction.interpret(tree, newEnv)
                    if isinstance(result, Exceptions):
                        tree.setExceptions(result)
                    if isinstance(result, Return): 
                        return result
                    if isinstance(result, Break):
                        breakValidator = True
                        break
                    if isinstance(result, Continue):
                        continueValidator = True
                        break
                if breakValidator == True:
                    breakValidator = False
                    break
                elif continueValidator == True:
                    continueValidator = False
                    continue
                conditional = self.conditional.interpret(tree, enviroment)
                
                if not isinstance(conditional, bool):
                    message = f'No boolean expression entered in loop while "{str(conditional)}"'
                    return Exceptions('Semantyc', message, self.row, self.column)
            return None
        
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, 'while')
        #Lado Izquierdo
        left = self.conditional.graph(root)
        root.edge(_id, left)
        #Lado Derecho
        right_id = str(uuid.uuid4())
        root.node(right_id, '{}')
        first = self.bloqueWhile[0].graph(root)
        if len(self.bloqueWhile[1:]) > 0:
            prev_id = right_id
            for stmt in self.bloqueWhile[1:]:
                new_id = str(uuid.uuid4())
                root.node(new_id, ';')
                root.edge(prev_id, new_id)
                root.edge(new_id, stmt.graph(root))
                prev_id = new_id
        root.edge(right_id, first)
        root.edge(_id, right_id)
        return _id
        
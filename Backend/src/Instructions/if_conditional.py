from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.table import Table
from ..Instructions.return_expr import Return
from ..Instructions.break_expr import Break
from ..Instructions.continue_expr import Continue
import uuid

class If(Abstract):
    
    def __init__(self, conditional, bloqueIf, bloqueElse, bloqueElseif, row, column):
        self.conditional = conditional
        self.bloqueIf = bloqueIf
        self.bloqueElse = bloqueElse
        self.bloqueElseif = bloqueElseif
        super().__init__(row, column)

    def interpret(self, tree, table):
        conditional = self.conditional.interpret( tree, table )
        if not isinstance( conditional, bool):
            message = 'No boolean expression entered in condition "' + str( conditional ) + '"'
            return Exceptions('Semantyc', message, self.row, self.column)
        if bool( conditional ) == True:
            enviroment = Table( table )
            for instruction in self.bloqueIf:
                result = instruction.interpret( tree, enviroment )
                if isinstance(result, Exceptions) :
                    tree.setExceptions(result)
                if isinstance(result, Return): return result
                if isinstance(result, Break): return result
                if isinstance(result, Continue): return result
        elif self.bloqueElse != None:
            entorno = Table( table )
            for instruccion in self.bloqueElse:
                result = instruccion.interpret(tree, entorno)
                if isinstance(result, Exceptions) :
                    tree.setExceptions(result)
                if isinstance(result, Return): return result
                if isinstance(result, Break): return result
                if isinstance(result, Continue): return result
            
        elif self.bloqueElseif != None:
            result = self.bloqueElseif.interpret(tree, table)
            if isinstance(result, Exceptions) : return result
            if isinstance(result, Return): return result
            if isinstance(result, Break): return result
            if isinstance(result, Continue): return result
            
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, 'if')
        conditional = self.conditional.graph(root)
        root.edge(_id, conditional)
        temp_id = str(uuid.uuid4())
        for stmt in self.bloqueIf:
            new_id = str(uuid.uuid4())
            root.node(new_id, ';')
            root.edge(temp_id, new_id)
            root.edge(new_id, stmt.graph(root))
            temp_id = new_id
        cur_id = str(uuid.uuid4())
        root.node(cur_id, '{}')
        root.edge(cur_id, temp_id)
        root.edge(_id, cur_id)
        if self.bloqueElse != None:
            temp_id = str(uuid.uuid4())
            for stmt in self.bloqueElse:
                new_id = str(uuid.uuid4())
                root.node(new_id, ';')
                root.edge(temp_id, new_id)
                root.edge(new_id, stmt.graph(root))
                temp_id = new_id
            root.edge(cur_id, temp_id)
        if self.bloqueElseif != None:
            elif_id = self.bloqueElseif.graph(root)
            root.edge(cur_id, elif_id)
        return _id
            
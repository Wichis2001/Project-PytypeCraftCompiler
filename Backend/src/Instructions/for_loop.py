from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.table import Table
from ..Instructions.return_expr import Return
from ..Instructions.break_expr import Break
from ..Instructions.continue_expr import Continue
from ..Symbol_Table.symbol import Symbol
import uuid

class For(Abstract):

    def __init__(self, begin, conditional, increment, bloqueFor, validatorType, row, column):
        self.begin = begin
        self.conditional = conditional
        self.increment = increment
        self.bloqueFor = bloqueFor
        self.validatorType = validatorType
        super().__init__(row, column)

    def interpret(self, tree, table):
        if self.validatorType:
            newTable = Table(table)  # NUEVO ENTORNO
            begin = self.begin.interpret(tree, newTable)

            if isinstance(begin, Exceptions): return begin

            #!Validar que el tipo sea númerico
            if( self.begin._type != 'number' ):
                message = 'No number expression entered in the begin of the loop for "' + str( begin ) + '"'
                return Exceptions('Semantyc', message, self.row, self.column)

            conditional = self.conditional.interpret(tree, newTable)
            if isinstance(conditional, Exceptions): return conditional

            #!Validar que el tipo sea booleano

            if self.conditional._type != 'boolean':
                message = 'No booloean expression entered in the conditional of the loop for "' + str( begin ) + '"'
                return Exceptions('Semantyc', message, self.row, self.column)
            
            breakValidator = False;
            continueValidator = False;
            
            #? Recorriendo las instrucciones
            while conditional:
                newEnv = Table( newTable )
                for instruction in self.bloqueFor:
                    result = instruction.interpret(tree, newEnv )
                    if isinstance(result, Exceptions):
                        tree.exceptions.append(result)
                    if isinstance(result, Return): return result
                    if isinstance(result, Break):
                        breakValidator = True;
                        break
                    if isinstance(result, Continue):
                        continueValidator = True;
                        break

                newValue = self.increment.interpret(tree, newTable);
                
                if isinstance(newValue, Exceptions): return newValue
                if( breakValidator ):
                    breakValidator = False
                    break
                elif( continueValidator ):
                    continueValidator = False
                    continue


                conditional = self.conditional.interpret(tree, newTable)
                if isinstance(conditional, Exceptions): return conditional
                if self.conditional._type != 'boolean':
                    message = 'No booloean expression entered in the conditional of the loop for "' + str( begin ) + '"'
                    return Exceptions('Semantyc', message, self.row, self.column)
            return None
        else:
            newTable = Table(table)  # NUEVO ENTORNO
            begin = self.begin.interpret(tree, newTable)
            if isinstance(begin, Exceptions): return begin
            symbol = newTable.getTableEnv(self.begin._id)
            #!Validar que el tipo sea númerico
            if( self.begin._type == 'any'):
                if( not isinstance(symbol.value, int)):
                    message = 'No number expression entered in the begin of the loop for "' + str( begin ) + '"'
                    return Exceptions('Semantyc', message, self.row, self.column)
            elif( self.begin._type != 'number' ):
                if( not isinstance(symbol.value, int)):
                    message = 'No number expression entered in the begin of the loop for "' + str( begin ) + '"'
                    return Exceptions('Semantyc', message, self.row, self.column)

            conditional = self.conditional.interpret(tree, newTable)
            if isinstance(conditional, Exceptions): return conditional

            #!Validar que el tipo sea booleano

            if self.conditional._type != 'boolean':
                message = 'No booloean expression entered in the conditional of the loop for "' + str( begin ) + '"'
                return Exceptions('Semantyc', message, self.row, self.column)
            
            breakValidator = False;
            continueValidator = False;
            
            #? Recorriendo las instrucciones
            while conditional:
                newEnv = Table( newTable )
                for instruction in self.bloqueFor:
                    result = instruction.interpret(tree, newEnv )
                    if isinstance(result, Exceptions):
                        tree.exceptions.append(result)
                    if isinstance(result, Return): return result
                    if isinstance(result, Break):
                        breakValidator = True;
                        break
                    if isinstance(result, Continue):
                        continueValidator = True;
                        break

                newValue = self.increment.interpret(tree, newTable);
                if isinstance(newValue, Exceptions): return newValue

                if( breakValidator ):
                    breakValidator = False
                    break
                elif( continueValidator ):
                    continueValidator = False
                    continue

                conditional = self.conditional.interpret(tree, newTable)
                if isinstance(conditional, Exceptions): return conditional
                if self.conditional._type != 'boolean':
                    message = 'No booloean expression entered in the conditional of the loop for "' + str( begin ) + '"'
                    return Exceptions('Semantyc', message, self.row, self.column)
            return None
        
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, 'for')
        #Lado Izquierdo
        left_id = str(uuid.uuid4())
        root.node(left_id, '()')
        first_left = self.begin.graph(root)
        second_left = self.conditional.graph(root)
        tercer_left = self.increment.graph(root)
        root.edge(left_id, first_left)
        root.edge(left_id, second_left)
        root.edge(left_id, tercer_left)
        #Lado Derecho
        right_id = str(uuid.uuid4())
        root.node(right_id, '{}')
        first = self.bloqueFor[0].graph(root)
        prev_id = right_id
        if len(self.bloqueFor[1:]) > 0:
            for stmt in self.bloqueFor[1:]:
                new_id = str(uuid.uuid4())
                root.node(new_id, ';')
                root.edge(prev_id, new_id)
                root.edge(new_id, stmt.graph(root))
                prev_id = new_id
        root.edge(right_id, first)
        root.edge(_id, left_id)
        root.edge(_id, right_id)
        return _id
        
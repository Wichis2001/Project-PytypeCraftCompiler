from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.table import Table
from ..Instructions.return_expr import Return
from ..Instructions.break_expr import Break
from ..Instructions.continue_expr import Continue
from ..Symbol_Table.symbol import Symbol
import uuid

class ForOf(Abstract):

    def __init__(self, declaration, expression, bloqueForOF, row, column):
        self.declaration = declaration
        self.expression = expression
        self.bloqueForOF = bloqueForOF
        super().__init__(row, column)

    def interpret(self, tree, table):
        enviroment = Table( table )

        declaration = self.declaration.interpret( tree, enviroment )
        if isinstance(declaration, Exceptions): return declaration
        
        expression = self.expression.interpret( tree, enviroment )
        if isinstance(expression, Exceptions): return declaration
        if isinstance(expression, Symbol):
            expression = expression.getValue()
        if self.expression._type == 'string':
            
            breakValidator = False
            continueValidator = False
            if( self.declaration._type!= 'string' and self.declaration._type!= 'any'):
                    return Exceptions("Semantyc", 'The variable of declaration is not of type string', self.row, self.column)
            for value in range(len(str( expression ))):
                
                symbol = enviroment.getTableEnv(self.declaration._id)
                if symbol != None:
                    symbol.setValue(str(expression)[value])
                else:
                    return Exceptions("Semantyc", 'The variable is not defined', self.row, self.column)
                newEnv = Table( enviroment )
                for instruction in self.bloqueForOF:
                    result = instruction.interpret(tree, newEnv )
                    if isinstance(result, Exceptions):
                        tree.exceptions.append(result)
                    if isinstance(result, Return): return result
                    if isinstance(result, Break):
                        breakValidator = True
                        break
                    if isinstance(result, Continue):
                        continueValidator = True
                        break
                if( breakValidator ):
                    breakValidator = False
                    break
                elif( continueValidator ):
                    continueValidator = False
                    continue
                declaration = self.expression.interpret( tree, enviroment )
               
                # if ( declaration != tmp):
                #     message = 'Error manipulation intern iterable ForOf loop "' + str( tmp ) + '"'
                #     return Exceptions('Semantyc', message, self.row, self.column)
        elif isinstance(expression, list):
            breakValidator = False
            continueValidator = False
            if self.declaration._type != 'any' and not isinstance(self.declaration._type, list):
                return Exceptions("Semantyc", 'The variable of declaration is not of type Array', self.row, self.column)
            for item in expression:
                symbol = enviroment.getTableEnv(self.declaration._id)
                if symbol != None:
                    symbol.setValue(item)
                    symbol.setValueType(self.det_Value_Type(item))
                else:
                    return Exceptions("Semantyc", 'The variable is not defined', self.row, self.column)
                newEnv = Table( enviroment )
                for instruction in self.bloqueForOF:
                    result = instruction.interpret(tree, newEnv )
                    if isinstance(result, Exceptions):
                        tree.exceptions.append(result)
                    if isinstance(result, Return): return result
                    if isinstance(result, Break):
                        breakValidator = True
                        break
                    if isinstance(result, Continue):
                        continueValidator = True
                        break
                if( breakValidator ):
                    breakValidator = False
                    break
                elif( continueValidator ):
                    continueValidator = False
                    continue
                declaration = self.expression.interpret( tree, enviroment )
        else:
            message = 'Type ' + str( declaration ) + ' is not an array type or a string type"'
            return Exceptions('Semantyc', message, self.row, self.column)
        
    def det_Value_Type(self, value):
        if isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, (int, float)):
            return 'number'
        elif isinstance(value, str):
            return 'string'
        elif value == None:
            return 'null'
        
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, 'for')
        #Lado izquierdo
        left_id = str(uuid.uuid4())
        first_left = self.declaration.graph(root)
        second_left = self.expression.graph(root)
        root.node(left_id, 'of')
        root.edge(left_id, first_left)
        root.edge(left_id, second_left)
        #Lado derecho
        rigth_id = str(uuid.uuid4())
        root.node(rigth_id, '{}')
        first = self.bloqueForOF[0].graph(root)
        prev_id = rigth_id
        for stmt in self.bloqueForOF[1:]:
            new_id = str(uuid.uuid4())
            root.node(new_id, ';')
            root.edge(prev_id, new_id)
            root.edge(new_id, stmt.graph(root))
            prev_id = new_id
        root.edge(rigth_id, first)
        root.edge(_id, left_id)
        root.edge(_id, rigth_id)
        return _id
        
        
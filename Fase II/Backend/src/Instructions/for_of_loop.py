from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.table import Table
from ..Instructions.return_expr import Return
from ..Instructions.break_expr import Break
from ..Instructions.continue_expr import Continue
from ..Symbol_Table.symbol import Symbol

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
        if isinstance(declaration, Exceptions): return declaration
        
        if( self.expression._type == 'string'):
            
            breakValidator = False;
            continueValidator = False;
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
                        breakValidator = True;
                        break
                    if isinstance(result, Continue):
                        continueValidator = True;
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
            
        else:
            message = 'Type ' + str( declaration ) + ' is not an array type or a string type"'
            return Exceptions('Semantyc', message, self.row, self.column)
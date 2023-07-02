from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.table import Table
from ..Instructions.return_expr import Return
from ..Instructions.break_expr import Break
from ..Instructions.continue_expr import Continue
from ..Symbol_Table.generator import Generator
class If(Abstract):

    def __init__(self, conditional, bloqueIf, bloqueElse, bloqueElseif, row, column):
        self.conditional = conditional
        self.bloqueIf = bloqueIf
        self.bloqueElse = bloqueElse
        self.bloqueElseif = bloqueElseif
        super().__init__(row, column)

    def interpret(self, tree, table):
        genAux = Generator()
        generator = genAux.getInstance()

        generator.addComment('Se empieza a recorrer el condicional if')
        conditional = self.conditional.interpret( tree, table )
        if isinstance(conditional, Exceptions): return conditional
        if conditional.getType() == 'boolean':
            generator.putLabel(conditional.getTrueLbl())
            enviroment = Table( table )
            for instruction in self.bloqueIf:
                enviroment.breakLbl = table.breakLbl
                enviroment.continueLbl = table.continueLbl
                enviroment.returnLbl = table.returnLbl
                result = instruction.interpret( tree, enviroment )
                if isinstance(result, Exceptions) :
                    tree.setExceptions(result)
                if isinstance(result, Return):
                    if enviroment.returnLbl != '':
                        if result.getTrueLbl() == '':
                            generator.addComment('Se esteblece el valor que va retornar la función')
                            generator.setStack('P', result.getValue())
                            generator.addGoto( enviroment.returnLbl )
                            generator.addComment('Se culmna de establecer el valor que va retornar la función')
                        else:
                            generator.addComment('Se esteblece el valor que va retornar la función')
                            generator.putLabel(result.getTrueLbl())
                            generator.setStack('P', '1')
                            generator.addGoto( enviroment.returnLbl )
                            generator.putLabel( result.getFalseLbl() )
                            generator.setStack('P', '0')
                            generator.addGoto( enviroment.returnLbl )
                            generator.addComment('Se culmna de establecer el valor que va retornar la función')
                if isinstance(result, Break):
                    if table.breakLbl != '':
                        generator.addGoto(table.breakLbl)
                    else:
                        goOut = generator.newLabel()
                        generator.addGoto( goOut )
                        generator.putLabel( conditional.getFalseLbl())
                        generator.putLabel( goOut )
                        message = 'break statement set outside of a loop'
                        return Exceptions('Semantyc', message, self.row, self.column)
                if isinstance(result, Continue):
                    if table.continueLbl != '':
                        generator.addGoto( table.continueLbl )
                    else:
                        goOut = generator.newLabel()
                        generator.addGoto( goOut )
                        generator.putLabel( conditional.getFalseLbl())
                        generator.putLabel( goOut )
                        message = 'break statement set outside of a loop'
                        return Exceptions('Semantyc', message, self.row, self.column)
            goOut = generator.newLabel()
            generator.addGoto( goOut )
            generator.putLabel( conditional.getFalseLbl())
            if self.bloqueElse != None:
                enviroment = Table( table )
                for instruccion in self.bloqueElse:
                    enviroment.breakLbl = table.breakLbl
                    enviroment.continueLbl = table.continueLbl
                    enviroment.returnLbl = table.returnLbl
                    result = instruccion.interpret(tree, enviroment)
                    if isinstance(result, Exceptions) :
                        tree.setExceptions(result)
                    if isinstance(result, Return):
                        if enviroment.returnLbl != '':
                            if result.getTrueLbl() == '':
                                generator.addComment('Se esteblece el valor que va retornar la función')
                                generator.setStack('P', result.getValue())
                                generator.addGoto( enviroment.returnLbl )
                                generator.addComment('Se culmna de establecer el valor que va retornar la función')
                            else:
                                generator.addComment('Se esteblece el valor que va retornar la función')
                                generator.putLabel(result.getTrueLbl())
                                generator.setStack('P', '1')
                                generator.addGoto( enviroment.returnLbl )
                                generator.putLabel( result.getFalseLbl() )
                                generator.setStack('P', '0')
                                generator.addGoto( enviroment.returnLbl )
                                generator.addComment('Se culmna de establecer el valor que va retornar la función')
                    if isinstance(result, Break):
                        if table.breakLbl != '':
                            generator.addGoto(table.breakLbl)
                        else:
                            generator.putLabel( goOut )
                            message = 'break statement set outside of a loop'
                            return Exceptions('Semantyc', message, self.row, self.column)
                    if isinstance(result, Continue):
                        if table.continueLbl != '':
                            generator.addGoto( table.continueLbl )
                        else:
                            generator.putLabel( goOut )
                            message = 'break statement set outside of a loop'
                            return Exceptions('Semantyc', message, self.row, self.column)
            elif self.bloqueElseif != None:
                result = self.bloqueElseif.interpret(tree, table)
                if isinstance(result, Exceptions) : return result
            generator.putLabel( goOut )
            generator.addComment('Fin de la compilación del ciclo if')
        else:
            message = 'No boolean expression entered in condition "' + str( conditional ) + '"'
            return Exceptions('Semantyc', message, self.row, self.column)

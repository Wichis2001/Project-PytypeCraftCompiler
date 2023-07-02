from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.table import Table
from ..Instructions.return_expr import Return
from ..Instructions.break_expr import Break
from ..Instructions.continue_expr import Continue
from ..Symbol_Table.symbol import Symbol
from ..Symbol_Table.generator import Generator

class For(Abstract):

    def __init__(self, begin, conditional, increment, bloqueFor, row, column):
        self.begin = begin
        self.conditional = conditional
        self.increment = increment
        self.bloqueFor = bloqueFor
        super().__init__(row, column)

    def interpret(self, tree, table):
        genAux = Generator()
        generator = genAux.getInstance()
        generator.addComment('Se empieza a recorrer un ciclo for')
        entorno = Table(table)
        begin = self.begin.interpret(tree, table)
        if isinstance(begin, Exceptions):
            return begin

        while True:
            generator.addComment('Inicia el recorrido del ciclo For')
            newEnv = Table(table)
            Lbl0 = generator.newLabel()
            generator.putLabel(Lbl0)

            conditional = self.conditional.interpret(tree, table)
            if isinstance(conditional, Exceptions):
                tree.setExceptions( conditional )

            if conditional.getType() != 'boolean':
                message = 'No boolean expression entered in the conditional of the loop for "' + str(begin) + '"'
                return Exceptions('Semantyc', message, self.row, self.column)

            generator.putLabel(conditional.getTrueLbl())
            table.breakLbl = conditional.getFalseLbl()
            table.continueLbl = Lbl0

            for instruction in self.bloqueFor:
                entorno.breakLbl = table.breakLbl
                entorno.continueLbl = table.continueLbl
                entorno.returnLbl = table.returnLbl
                result = instruction.interpret(tree, newEnv)
                if isinstance(result, Exceptions):
                    tree.exceptions.append(result)
                if isinstance(result, Return):
                    if entorno.returnLbl != '':
                        generator.addComment('Inicializando el valor de retorno para la función')
                        if result.getTrueLbl() == '':
                            generator.setStack('P', result.getValue())
                            generator.addGoto(entorno.returnLbl)
                        else:
                            generator.putLabel(result.getTrueLbl())
                            generator.setStack('P', '1')
                            generator.addGoto(entorno.returnLbl)
                            generator.putLabel(result.getFalseLbl())
                            generator.setStack('P', '0')
                            generator.addGoto(entorno.returnLbl)
                    generator.addComment('Finalizando el valor de retorno para la función')
                if isinstance(result, Break):
                    generator.addGoto(table.breakLbl)
                if isinstance(result, Continue):
                    generator.addGoto(table.continueLbl)
            increment = self.increment.interpret(tree, entorno)
            if isinstance(increment, Exceptions):
                return increment
            print( increment.getValue(), 'ddddddddddddsfsdfsdfs')
            newEnv.breakLbl = ''
            newEnv.continueLbl = ''
            generator.addGoto(Lbl0)
            generator.putLabel(conditional.getFalseLbl())
            generator.addComment('Se finaliza el Bloque For')
            break

    def getType(self, conditional ):
        if( conditional._type == 'boolean'):
            if( bool(conditional) == True ):
               return True
            else:
                return False
        else:
            message = 'No boolean expression entered in loop while "' + str( conditional ) + '"'
            return Exceptions('Semantyc', message, self.row, self.column)

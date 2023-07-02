from ..Expressions.identificator import Identificator
from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.generator import Generator
from ..Abstract.return_ import Return
from ..Symbol_Table.symbol import Symbol
class Unary(Abstract):

    def __init__(self, expr, unary_op, row, column):
        self.expr = expr
        self.unary_op = unary_op
        self._type = 'number'
        super().__init__(row, column)

    def interpret(self, tree, table):
        op = self.unary_op
        genAux = Generator()
        generator = genAux.getInstance()
        temp=''
        
        if op == '!':
            generator.addComment("Compilacion de Expresion Relacional")
            self.checkLabels()
            self.expr.setFalseLbl(self.trueLbl)
            self.expr.setTrueLbl(self.falseLbl)
            lblNot = self.expr.interpret( tree, table )
            if isinstance(lblNot, Exception): return lblNot
            if lblNot.getType() != 'boolean':
                return Exceptions("Semantyc", "The boolean expression entered is invalid: ", self.fila, self.colum)

            lbltrue = lblNot.getTrueLbl()
            lblfalse = lblNot.getFalseLbl()
            lblNot.setTrueLbl(lblfalse)
            lblNot.setFalseLbl(lbltrue)
            self._type = 'boolean'

            return lblNot
        else:
            symbol = table.getTableEnv(self.expr)
            if( symbol!=None ):
                expr= symbol
            else:
                expr = self.expr.interpret( tree, table )
                if isinstance(expr, Exceptions):
                    return expr
            expr_type = expr.getType()
            if expr_type == 'number':
                if symbol!=None:
                    if op == '-':
                        temp = generator.addTemp()
                        generator.getStack( temp, expr.position )
                        temp2 = generator.addTemp()
                        generator.addExp( temp2, '0', temp, op )
                        self._type = 'number'
                        return Return(temp2, self._type, True)
                    elif op == '++':
                        temp = generator.addTemp()
                        generator.getStack( temp, expr.position )
                        temp2 = generator.addTemp()
                        generator.addExp(temp2, '1', temp, '+')
                        generator.setStack( expr.position, temp2)
                        self._type = 'number'
                        return Return(temp, self._type, True)
                    elif op == '--':
                        temp = generator.addTemp()
                        generator.getStack( temp, expr.position )
                        temp2 = generator.addTemp()
                        generator.addExp( temp2, '-1', temp, '+' )
                        generator.setStack( expr.position, temp2)
                        self._type = 'number'
                        return Return(temp, self._type, True)
                else:
                    if op == '-':
                        temp = generator.addTemp()
                        generator.addExp( temp, '0', expr.getValue(), op )
                        self._type = 'number'
                        return Return(temp, self._type, True)
            else:
                message = 'It is not possible to operate with other types of data'
                return Exceptions('Error', message, self.row, self.column)

    def getType(self):
        return self._type

    def checkLabels(self):
        genAux = Generator()
        generador = genAux.getInstance()
        if self.trueLbl == '':
            self.trueLbl = generador.newLabel()
        if self.falseLbl == '':
            self.falseLbl = generador.newLabel()
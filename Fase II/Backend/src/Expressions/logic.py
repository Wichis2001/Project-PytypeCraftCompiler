from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.generator import Generator
from ..Abstract.return_ import Return

class Logic(Abstract):

    def __init__(self, left_op, right_op, logic_op, row, column):
        self.left_op = left_op
        self.right_op = right_op
        self.logic_op = logic_op
        self._type = None
        super().__init__(row, column)

    def interpret(self, tree, table):
        genAux = Generator()
        generator = genAux.getInstance()
        generator.addComment("Compilacion de Expresion Relacional")

        op = self.logic_op
        self.checkLabels()
        lblAndOr = ''
        if op == '&&':
            lblAndOr =  generator.newLabel()
            self.left_op.setTrueLbl(lblAndOr)
            self.right_op.setTrueLbl(self.trueLbl)
            self.left_op.falseLbl = self.right_op.falseLbl = self.falseLbl

        elif op == '||':
            self.left_op.setTrueLbl(self.trueLbl)
            self.right_op.setTrueLbl(self.trueLbl)
            lblAndOr =  generator.newLabel()
            self.left_op.setFalseLbl(lblAndOr)
            self.right_op.setFalseLbl(self.falseLbl)

        leftTest = self.left_op.interpret( tree, table)
        if isinstance(leftTest, Exceptions): return leftTest
        if leftTest._type != 'boolean':
            message = 'It is not possible to operate with other types of data'
            return Exceptions('Error', message, self.row, self.column)

        generator.putLabel(lblAndOr)
        rightTest = self.right_op.interpret( tree, table )
        if isinstance(rightTest, Exceptions): return rightTest

        if rightTest._type != 'boolean':
            message = 'It is not possible to operate with other types of data'
            return Exceptions('Error', message, self.row, self.column)
        generator.addComment("FINALIZO EXPRESION LOGICA")
        self._type = 'boolean'
        generator.addSpace()
        ret = Return(None, self._type, False)
        ret.setTrueLbl(self.trueLbl)
        ret.setFalseLbl(self.falseLbl)
        return ret

    def getType(self):
        return self._type

    def checkLabels(self):
        genAux = Generator()
        generador = genAux.getInstance()
        if self.trueLbl == '':
            self.trueLbl = generador.newLabel()
        if self.falseLbl == '':
            self.falseLbl = generador.newLabel()
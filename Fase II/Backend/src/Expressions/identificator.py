from ..Symbol_Table.exceptions import Exceptions
from ..Abstract.abstract import Abstract
from ..Symbol_Table.generator import Generator
from ..Abstract.return_ import Return
class Identificator(Abstract):

    def __init__(self, _id, row, column):
        self._id = _id
        self._type = None
        self.row = row
        self.column = column
        super().__init__(row, column)

    def interpret(self, tree, table):
        genAux = Generator()
        generator = genAux.getInstance()

        generator.addComment('Generating build access')
        symbol = table.getTableEnv(self._id)
        if symbol == None:
            generator.addComment('Terminating compilation due to variable access error')
            message = 'Variable "' + self._id + '" is no defined'
            return Exceptions('Error', message, self.row, self.column)
        self._type = symbol.getType()

        #!Almacenamos la variable
        temp = generator.addTemp()

        #!Obtenemos la posicioón en la que se encuentra la variable en el stack
        tempPos = symbol.position
        if not symbol.isGlobal:
            tempPos = generator.addTemp()
            generator.addExp( tempPos, 'P', symbol.position, '+')
        generator.getStack( temp, tempPos)

        if self._type != 'boolean':
            generator.addComment('Terminating build access')
            generator.addSpace()
            return Return( temp, self._type, True)

        if self.trueLbl == '':
            self.trueLbl = generator.newLabel()
        if self.falseLbl == '':
            self.falseLbl = generator.newLabel()

        generator.addIf( temp, '1', '==', self.trueLbl)
        generator.addGoto(self.falseLbl)

        generator.addComment('Terminating build acces')
        generator.addSpace()

        ret = Return( temp, 'boolean', True)
        ret.setTrueLbl(self.trueLbl)
        ret.setFalseLbl(self.falseLbl)
        return ret

    def getType(self):
        return self._type

    def getId(self):
        return self._id

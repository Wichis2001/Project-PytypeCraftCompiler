from ..Abstract.abstract import Abstract
from ..Symbol_Table.generator import Generator
from ..Abstract.return_ import Return

class Primitive(Abstract):

    def __init__(self, _type, value, row, column):
        self._type = _type
        self.value = value
        self.typeAux = ''
        super().__init__(row, column)

    def interpret(self, tree, table):
        genAux = Generator()
        generator = genAux.getInstance()
        if self._type == 'number':
            return Return(str(self.value), self._type, False)
        elif( self._type == 'string' ):
            temporal = generator.addTemp()
            generator.addAsign(temporal, 'H')

            for char in str(self.value):
                generator.setHeap('H', ord(char))
                generator.nextHeap()

            generator.setHeap('H', '-1')
            generator.nextHeap()

            return Return(temporal, self._type, True)
        elif self._type == 'boolean':
            if self.trueLbl == '':
                self.trueLbl = generator.newLabel()
            if self.falseLbl == '':
                self.falseLbl = generator.newLabel()

            if self.value:
                generator.addGoto(self.trueLbl)
                generator.addComment("GOTO PARA EVITAR ERROR DE GO")
                generator.addGoto(self.falseLbl)
            else:
                generator.addGoto(self.falseLbl)
                generator.addComment("GOTO PARA EVITAR ERROR DE GO")
                generator.addGoto(self.trueLbl)

            ret = Return(self.value, self._type, False)
            ret.trueLbl = self.trueLbl
            ret.falseLbl = self.falseLbl
            return ret

    def getType(self):
        return self._type

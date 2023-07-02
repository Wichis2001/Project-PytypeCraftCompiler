from ..Abstract.abstract import Abstract
from ..Symbol_Table.symbol import Symbol
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.generator import Generator


class Var_Declaration(Abstract):

    def __init__(self, _id, _type, value, row, column):
        self._id = _id
        self._type = _type
        self.value = value
        self.find = True
        self.ghost = -1
        super().__init__(row, column)

    def interpret(self, tree, table):
        genAux = Generator()
        generator = genAux.getInstance()
        if self.value != None:
            if self._type != None:
                generator.addComment('Compile for variable value')
                value = self.value.interpret(tree, table)
                if isinstance(value, Exceptions): return value
                if str(self._type == str(self.value._type)):
                    inHeap = value.getType() == 'string'
                    symbol = table.setTable(self._id, value.getType(), inHeap, self.find)
                else:
                    generator.addComment('Error → data type different from the declared variable type')
                    result = Exceptions('Semantyc', 'Data type different from the typed', self.row, self.column)
                    return result
                tempPos = symbol.position
                if not symbol.isGlobal:
                    tempPos = generator.addTemp()
                    generator.addExp(tempPos, 'P', symbol.position, '+')
                if value.getType() == 'boolean':
                    tempLbl = generator.newLabel()
                    generator.putLabel(value.trueLbl)
                    generator.setStack(tempPos, '1')

                    generator.addGoto(tempLbl)
                    generator.putLabel(value.falseLbl)
                    generator.setStack(tempPos, '0')
                    generator.putLabel(tempLbl)
                else:
                    generator.setStack(tempPos, value.value)
                generator.addComment('End of compilation for variable value')
                generator.addSpace()
            else:
                generator.addComment('Incilizando el valor para la variable')
                value = self.value.interpret(tree, table )
                if isinstance(value, Exceptions): return value
                symbol = table.setTable( self._id, value.getType(),(value._type == 'string'), self.find)
                
                tempPos = symbol.getPosition()
                if(not symbol.isGlobal):
                    tempPos = generator.addTemp()
                    generator.addExp(tempPos, 'P', symbol.position, '+')
                if value.getType() == 'boolean':
                    tempLbl = generator.newLabel()
                    generator.putLabel(value.trueLbl)
                    generator.setStack(tempPos, '1')

                    generator.addGoto(tempLbl)
                    generator.putLabel(value.falseLbl)
                    generator.setStack(tempPos, '0')
                    generator.putLabel(tempLbl)
                else:
                    generator.setStack(tempPos, value.value)
                generator.addComment('End of compilation for variable value')
                generator.addSpace()
        else:
            generator.addComment('Incilizando el valor para la variable')
            if self._type:
                symbol = table.setTable(self._id, self._type, True)
            tempPos = symbol.getPosition()
            if not symbol.isGlobal:
                tempPos = generator.addTemp()
                generator.addExp( tempPos, 'P', symbol.position, '+')
            generator.setStack(tempPos, self.ghost)
            generator.addComment('End of compilation for variable value')
            return tempPos
from typing import List
from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
from ..Symbol_Table.generator import Generator
from ..Abstract.return_ import Return
class Array(Abstract):

    def __init__(self, _id, index, row, column):
        self._id = _id
        self.index = index
        super().__init__(row, column)

    def interpret(self, tree, table):
        genAux = Generator()
        generator = genAux.getInstance()
        generator.addComment('Accediendo al arrego ' + self._id)
        variable = ''

        if self._id:
            variable = table.getTableEnv( self._id )
            if variable == None:
                generator.addComment('Terminating compilation due to variable access error')
                message = 'Variable "' + self._id + '" is no defined'
                return Exceptions('Error', message, self.row, self.column)

        generator.fboundError()
        temp = generator.addTemp()
        tempPosition = variable.position
        if not variable.isGlobal:
            tempPosition = generator.addTemp()
            generator.addExp(tempPosition, 'P', variable.position, '+')
        generator.getStack( temp, tempPosition )
        count = 0

        _type = variable.getType()
        typeAssistant = variable.getTipoAux()
        for valueIndex in self.index:
            count+=1
            
            firsTemp = generator.addTemp()
            secondTemp = generator.addTemp()
            thirdTemp = generator.addTemp()
            
            firstLabel = generator.newLabel()
            secondLabel = generator.newLabel()
            thirdLabel = generator.newLabel()
            index = valueIndex.interpret(tree, table)
            if( 't' in index.getValue()):
                tempForData = generator.addTemp()
                generator.addExp(tempForData, index.getValue(), 1, '+')
                arrayDimension = tempForData
            else:
                arrayDimension = str(int(index.getValue())+1)
            generator.addExp(firsTemp, temp, arrayDimension, '+')
            generator.addIf(arrayDimension,'1', '<', firstLabel)
            generator.getHeap( thirdTemp, temp )
            generator.addIf(arrayDimension, thirdTemp, '>', firstLabel)
            generator.addGoto(secondLabel)
            generator.newLabel(firstLabel)
            generator.callFun('BoundsError')
            generator.addGoto(thirdLabel)
            generator.newLabel(secondLabel)
            generator.getHeap( secondTemp, firsTemp )
            generator.addGoto(thirdLabel)
            generator.newLabel(thirdLabel)
            temp = secondTemp
            if count == len(self.index):
                variable.setType(variable.getTipoAux())
            else:
                if isinstance(variable.getTipoAux(), List):
                    variable.setType(variable.getTipoAux()[0])
                    variable.setTipoAux(variable.getTipoAux()[1])
                else:
                    message = 'Error al acceder al array "' + self._id;
                    return Exceptions('Error', message, self.row, self.column)
        generator.addComment('Terminado de acceder al arreglo ' + self._id )
        res = Return( secondTemp, variable.getType(), True, 0,variable.getTipoAux())
        variable.setType( _type )
        variable.setTipoAux( typeAssistant )
    def getType(self):
        return self._type
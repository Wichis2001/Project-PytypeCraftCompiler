from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
from ..Symbol_Table.table import Table
from ..Instructions.interface_id import Interface_Id
from ..Instructions.array_id import Array_Id
from ..Symbol_Table.generator import Generator
from ..Abstract.return_ import Return
class Function_Call(Abstract):

    def __init__(self, _id, params, row, column):
        self._id = _id
        self.params = params
        self.trueLbl = ''
        self.falseLbl = ''
        super().__init__(row, column)

    def interpret(self, tree, table):
        genAux = Generator()
        generator = genAux.getInstance()
        result = tree.getFunction(self._id)

        if result != None:
            generator.addComment(f'Llamada a la funcion {self._id}')
            paramValues = []
            temps = []
            size = table.size

            for parametros in self.params:
                if isinstance(parametros, Function_Call):
                    self.guardarTemps(generator, table, temps)
                    a = parametros.interpret(tree, table)
                    if isinstance(a, Exceptions): return a
                    paramValues.append(a)
                    self.recuperarTemps(generator, table, temps)
                else:
                    value = parametros.interpret(tree, table)
                    if isinstance(value, Exceptions):
                        return value
                    paramValues.append(value)
                    temps.append(value.getValue())
            temp = generator.addTemp()
            generator.addExp(temp,'P',size+1, '+')
            aux = 0
            if len(result.getParams()) == len(paramValues):
                for param in paramValues:
                    if result.params[aux]['_type'] == param.getType():
                        aux += 1
                        generator.setStack(temp,param.getValue())
                        if aux != len(paramValues):
                            generator.addExp(temp,temp,1,'+')
                    else:
                        generator.addComment(f'Fin de la llamada a la funcion {self._id} por error, consulte la lista de errores')
                        return Exceptions("Semantico", f"El tipo de dato de los parametros no coincide con la funcion {self._id}", self.row, self.column)
            generator.newEnv(size)
            self.getFuncion(generator=generator) # Sirve para llamar a una funcion nativa
            generator.callFun(result._id)
            generator.getStack(temp,'P')
            generator.retEnv(size)
            generator.addComment(f'Fin de la llamada a la funcion {self._id}')
            generator.addSpace()

            if result.getType() != 'boolean':
                return Return(temp, result.getType(), True)
            else:
                generator.addComment('Recuperacion de booleano')
                if self.trueLbl == '':
                    self.trueLbl = generator.newLabel()
                if self.falseLbl == '':
                    self.falseLbl = generator.newLabel()
                generator.addIf(temp, 1, '==', self.trueLbl)
                generator.addGoto(self.falseLbl)
                ret = Return(temp, result.getType(), True)
                ret.trueLbl = self.trueLbl
                ret.falseLbl = self.falseLbl
                generator.addComment('Fin de recuperacion de booleano')
                return ret
        else:
            return Exceptions('Semantyc', 'No se encontro la función a llamar', self.row, self.column)

    def guardarTemps(self, generador, tabla, tmp2):
        generador.addComment('Guardando temporales')
        tmp = generador.addTemp()
        for tmp1 in tmp2:
            generador.addExp(tmp, 'P', tabla.size, '+')
            generador.setStack(tmp, tmp1)
            tabla.size += 1
        generador.addComment('Fin de guardado de temporales')
    
    def recuperarTemps(self, generador, tabla, tmp2):
        generador.addComment('Recuperando temporales')
        tmp = generador.addTemp()
        for tmp1 in tmp2:
            tabla.size -= 1
            generador.addExp(tmp, 'P', tabla.size, '+')
            generador.getStack(tmp1, tmp)
        generador.addComment('Fin de recuperacion de temporales')

    def getFuncion(self, generator):
        if self._id == 'length':
            generator.fLength()
        elif self._id == 'trunc':
            generator.fTrunc()
        elif self._id == 'float':
            generator.fFloat()
        elif self._id == 'toUpperCase':
            generator.fUpperCase()
        elif self._id == 'toLowerCase':
            generator.fLowerCase()
        return

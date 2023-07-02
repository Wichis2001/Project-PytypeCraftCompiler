class Return:
    def __init__(self, value, retType, isTemp, auxType = '', length=0, referencia = ''):
        self.value = value
        self._type = retType
        self.auxType = auxType
        self.length = length
        self.referencia = referencia
        self.isTemp = isTemp
        self.trueLbl = ''
        self.falseLbl = ''

    def getValue(self):
        return self.value

    def getType(self):
        return self._type

    def getTipoAux(self):
        return self.auxType

    def getLength(self):
        return self.length

    def getReferencia(self):
        return self.referencia

    def getTrueLbl(self):
        return self.trueLbl

    def getFalseLbl(self):
        return self.falseLbl

    def setValue(self, value):
        self.value = value

    def setType(self, tipo):
        self.type = tipo

    def setTipoAux(self, tipo):
        self.auxType = tipo

    def setLength(self, length):
        self.length = length

    def setReferencia(self, ref):
        self.referencia = ref

    def setTrueLbl(self, trueLbl):
        self.trueLbl = trueLbl

    def setFalseLbl(self, falseLbl):
        self.falseLbl = falseLbl
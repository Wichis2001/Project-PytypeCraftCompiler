class Symbol():

    def __init__(self, _id, _type, position, globalVar, inHeap):
        self._id = _id
        self._type = _type
        self.position = position
        self.isGlobal = globalVar
        self.inHeap = inHeap
        self.value = None
        self.tipoAux = ''
        self.length = 0
        self.referencia = False
        self.params = None

    def getId(self):
        return self._id

    def setId(self, _id):
        self._id = _id

    def getPosition( self ):
        return self.position

    def setPosition( self, position ):
        self.position = position

    def getInHeap(self):
        return self.inHeap

    def setInHeap(self, value):
        self.inHeap = value

    def getTipoAux(self):
        return self.tipoAux

    def setTipoAux(self, tipo):
        self.tipoAux = tipo

    def getParams(self):
        return self.params

    def setParams(self, params):
        self.params = params

    def getLength(self):
        return self.length

    def setLength(self, length):
        self.length = length

    def getReferencia(self):
        return self.referencia

    def setReferencia(self, ref):
        self.referencia = ref

    def getType(self):
        if 'any' in self._type:
            if isinstance(self.value, list):
                return self.getTypeIsList('empty', self.value)
            else:
                return self.def_type(self.value)
        else:
            return self._type

    def getRealType(self):
        return self._type

    def setType(self, _type):
        self._type = _type

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def getRow(self):
        return self.row

    def getColumn(self):
        return self.column

    def getTypeIsList(self, _type, _list):
        for element in _list:
            if isinstance(element, list):
                _type = self.getTypeIsList('empty', element)
            else:
                if _type == 'empty':
                    _type = self.def_type(element)
                else:
                    new_type = self.def_type(element)
                    if new_type != _type:
                        _type = 'any'
        _type = _type + '[]'
        return _type

    def def_type(self, value_read):
        _type = 'any'
        if isinstance(value_read, bool):
            _type = 'boolean'
        elif isinstance(value_read, (int, float)):
            _type = 'number'
        elif isinstance(value_read, str):
            _type = 'string'
        return _type
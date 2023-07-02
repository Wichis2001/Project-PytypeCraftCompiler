class Symbol():
    
    def __init__(self, _id, _type, value, value_type, row, column):
        self._id = _id
        self._type = _type
        self.value = value
        self.value_type = value_type
        self.row = row
        self.column = column
        
    def getId(self):
        return self._id
    
    def setId(self, _id):
        self._id = _id
        
    def getType(self):
        return self._type
    
    def getRealType(self):
        return self._type
    
    def setValueType(self, value_type):
        self.value_type = value_type
    
    def getValueType(self):
        return self.value_type
    
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
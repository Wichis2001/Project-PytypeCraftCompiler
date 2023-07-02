class Exceptions:
    
    def __init__(self, _type, desc, row, column):
        self._type = _type
        self.desc = desc
        self.row = row
        self.column = column
        
    def toString(self):
        return self._type + ' → ' + self.desc + ' [' + str(self.row) + ', ' + str(self.column) + '];'
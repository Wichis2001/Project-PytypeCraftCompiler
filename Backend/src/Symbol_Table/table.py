from ..Symbol_Table.exceptions import Exceptions

class Table:
    
    def __init__(self, previous_table = None):
        self.table = {}
        self.previous_table = previous_table

    def getTable(self):
        return self.table
    
    def setTable(self, symbol):
        exist = self.table.get(symbol.getId(), None)
        if exist != None:
            print(exist)
            message = 'The variable "' + exist.getId() + '" was already defined in'
            return Exceptions('Semantyc', message, exist.getRow(), exist.getColumn())
        else:
            self.table[symbol.getId()] = symbol
            return None
        
    def setTableFunction(self, symbol):
        self.table[symbol.getId()] = symbol
        
    def getTableEnv(self, _id):
        current_table = self
        while current_table != None:
            if _id in current_table.table:
                return current_table.table[_id]
            else:
                current_table = current_table.previous_table
        return None
    
    def getTableSearch(self, _id):
        if _id in self.table:
            return self.table[_id]
        return None
    
    def updateTable(self, symbol):
        current_table = self
        _id = symbol.getId()
        while current_table != None:
            if _id in current_table.table:
                current_table.table[_id].setValue(symbol.getValue())
                return None
            else:
                current_table = current_table.previous_table
        return None
    
    def updateStruct(self, simbolo, claves):
        tablaActual = self
        while tablaActual != None:
            if simbolo._id in tablaActual.table:
                actual = tablaActual.table[simbolo._id].getValue()
                x = 0
                for clave in claves:
                    if x == (len(claves)-1):
                        try:
                            actual = actual[str(clave)]
                            if actual.getType() == 'null':
                                actual.setValue(simbolo.getValue())
                                actual.setType(simbolo.getType())
                            elif actual.getType() == simbolo.getType():
                                actual.setValue(simbolo.getValue())
                                actual.setType(simbolo.getType())
                            else:
                                return Exceptions("Semantyc", "Data types do not match", simbolo.getRow(), simbolo.getColumn())
                        except:
                            return Exceptions("Semantyc", "Symbols were not found", simbolo.getRow(), simbolo.getColumn())
                    else:
                        try:
                            actual = actual[str(clave)].getValue()
                        except:
                            return Exceptions("Semantyc", "No values ​​found to assign them", simbolo.getRow(), simbolo.getColumn())
                    x += 1
                return None
            else:
                tablaActual = tablaActual.previous_table
        return Exceptions("Semantico", "Variable not found", simbolo.getRow(), simbolo.getColumn())
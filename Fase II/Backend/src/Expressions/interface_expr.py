from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions

class Interface_Expr(Abstract):
    
    def __init__(self, atributes, row, column):
        self.atributes = atributes
        self.models = None
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        if self.atributes == None:
            message = 'Empty interface expression'
            return Exceptions('Semantyc', message, self.row, self.column)
        types = []
        atributes = {}
        for atribute in self.atributes:
            temp = {}
            value_atrb = atribute['expr'].interpret(tree, table)
            if isinstance(value_atrb, Exceptions):
                return value_atrb
            type_atrb = atribute['expr'].getType()
            temp['value'] = value_atrb
            temp['_type'] = type_atrb
            atributes[atribute['_id']] = temp 
        structs = tree.getStructs()
        for key, value in structs.items():
            isEqual = True
            if len(value) == len(atributes):
                for atrb_key, atrb_value in atributes.items():
                    item = value.get(atrb_key, None)
                    if item != None:
                        item_type = item['_type']
                        atrb_type = atrb_value['_type']
                        if item_type not in ['any', atrb_type]:
                            isEqual = False
                            break
                    else:
                        isEqual = False
            else:
                isEqual = False
            if isEqual == True:
                types.append(key)
        lenTypes = len(types)
        if lenTypes > 0:
            if lenTypes == 1:
                self.models = types[0]
            else:
                self.models = types
        else:
            message = 'Missing property in expression or struct type not found'
            return Exceptions('Semantyc', message, self.row, self.column)
        return atributes
    
    def getType(self):
        return self.models       
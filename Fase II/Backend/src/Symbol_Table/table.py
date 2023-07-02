from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
class Table:

    def __init__(self, previous_table = None):
        self.table = {}
        self.previous_table = previous_table
        self.breakLbl = ''
        self.continueLbl = ''
        self.returnLbl = ''
        self.recTemps = False
        self.size = 0
        if previous_table != None:
            self.size = self.previous_table.size

    def getTable(self):
        return self.table

    def setTable(self, _id, _type, inHeap, find = True):
        if find:
            currentTable = self
            while currentTable != None:
                if _id in currentTable.table:
                    currentTable.table[_id].setType( _type )
                    currentTable.table[_id].setInHeap( inHeap )
                    return currentTable.table[_id]
                else:
                    currentTable = currentTable.previous_table
        if _id in self.table:
            self.table[_id].setType( _type )
            self.table[_id].setInHeap( inHeap )
            return self.table[_id]
        else:
            symbol = Symbol(_id, _type, self.size, self.previous_table == None, inHeap)
            self.size += 1
            self.table[_id] = symbol
            return self.table[_id]

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
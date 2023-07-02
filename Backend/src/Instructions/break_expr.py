from src.Abstract.abstract import Abstract
from src.Symbol_Table.exceptions import Exceptions
from src.Symbol_Table.table import Table
import uuid

class Break(Abstract):
    
    def __init__(self, row, column):
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        if len(table.getTable()) != 0:
            return Exceptions('Semantyc', 'Break outside of a loop', self.row, self.column)
        return self;
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, 'Break')
        return _id
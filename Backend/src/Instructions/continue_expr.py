from src.Abstract.abstract import Abstract
from src.Symbol_Table.exceptions import Exceptions
from src.Symbol_Table.table import Table
import uuid

class Continue(Abstract):
    
    def __init__(self, row, column):
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        return self;
    
    def graph(self, root):
        _id = str(uuid.uuid4())
        root.node(_id, 'Continue')
        return _id
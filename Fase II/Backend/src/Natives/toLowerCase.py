from src.Instructions.function import Function
from src.Symbol_Table.exceptions import Exceptions

class ToLowerCase(Function):
    
    def __init__(self, _id, params, _type, statements, row, column):
        super().__init__(_id, params, _type, statements, row, column)
        
    def interpret(self, tree, table):
        return
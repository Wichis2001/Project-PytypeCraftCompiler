from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
import copy

class Concat(Abstract):
    
    def __init__(self, others_arrays, row, column):
        self.others_array = others_arrays
        self._type = 'any'
        self.value = None
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        if len(self.others_array) < 2:
            return Exceptions('Semantyc', 'Missing parameters for the concat function', self.row, self.column)
        main = self.others_array[0].interpret(tree, table)
        if isinstance(main, Symbol):
            main = copy.deepcopy(main.getValue())
        if not isinstance(main, list):
            return Exceptions('Semantyc', 'This value is not an array', self.row, self.column)
        self.others_array = self.others_array[1:]
        for array in self.others_array:
            array = array.interpret(tree, table)
            if isinstance(array, Symbol):
                array = array.getValue()
            if not isinstance(array, list):
                return Exceptions('Semantyc', 'This value is not an array', self.row, self.column)
            main.extend(array)
        self.value = main
        return self.value
    
    def getType(self):
        return self._type
    
    def getDimension(self):
        return 1
            
        
        
        
from abc import ABC, abstractmethod

class Abstract(ABC):

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.trueLbl = ''
        self.falseLbl = ''

    @abstractmethod
    def interpret(self, tree, table):
        pass

    def getTrueLbl(self):
        return self.trueLbl

    def getFalseLbl(self):
        return self.falseLbl

    def setTrueLbl(self, trueLbl):
        self.trueLbl = trueLbl

    def setFalseLbl(self, falseLbl):
        self.falseLbl = falseLbl
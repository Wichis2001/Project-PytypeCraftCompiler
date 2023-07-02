class Tree:

    def __init__(self, statements):
        self.statements = statements
        self.functions = {}
        self.structs = {}
        self.exceptions = []
        self.console = ''
        self.globalTs = None
        self.interpretedTs = {}

    def getStatements(self):
        return self.statements

    def setStatements(self, statements):
        self.statements = statements

    def getFunctions( self ):
        return self.functions

    def getFunction( self, _id):
        actual = self
        if actual != None:
            if _id in self.functions.keys():
                return actual.functions[_id]
        return None

    def setFunctions(self, _id, function):
        if _id in self.functions.keys():
            return 'error'
        else:
            self.functions[_id] = function
            print(self.functions.get(_id))

    def getStruct(self, _id):
        actual = self
        if actual != None:
            if _id in actual.structs.keys():
                return actual.structs[_id]
        return None

    def setStruct(self, _id, struct):
        if _id in self.structs.keys():
            return 'error'
        else:
            self.structs[_id] = struct

    def getExceptions(self):
        return self.exceptions

    def setExceptions(self, exceptions):
        self.exceptions.append(exceptions)

    def getConsole(self):
        return self.console

    def setConsole(self, console):
        self.console - console

    def updateConsole(self, console):
        self.console += console + '\n'

    def getGlobalTs(self):
        return self.globalTs

    def setGlobalTs(self, globalTs):
        self.globalTs = globalTs

    def getInterpretedTs(self):
        return self.interpretedTs

    def setInterpretedTs(self, env, value):
        self.interpretedTs[env] = value
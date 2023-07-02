class Tree:
    
    def __init__(self, statements):
        self.statements = statements
        self.functions = []
        self.exceptions = []
        self.structs = {}
        self.console = ''
        self.globalTs = None
        self.interpretedTs = {}
        
    def getStructs(self):
        return self.structs
    
    def addStruct(self, struct):
        _id = struct.get('_id')
        cont = struct.get('cont')
        self.structs[_id] = cont
        
    def searchStruct(self, _id):  
        return self.structs.get(_id, None)
        
    def getStatements(self):
        return self.statements
    
    def setStatements(self, statements):
        self.statements = statements
        
    def getFunction(self, _id):
        for function in self.functions:
            if function._id == _id:
                return function
        return None
        
    def getFunctions(self):
        return self.functions
    
    def setFunctions(self, functions):
        self.functions.append(functions)
        
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
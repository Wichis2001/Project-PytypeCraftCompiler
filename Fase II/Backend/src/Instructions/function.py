from typing import List
from ..Abstract.abstract import Abstract
from ..Instructions.return_expr import Return
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.table import Table
from ..Symbol_Table.generator import Generator


class Function(Abstract):
    
    def __init__(self, _id, params, _type, statements, row, column):
        self._id = _id
        self.params = params
        self.statements = statements
        self._type = _type
        self.recTemp = True
        super().__init__(row, column)
        
    def interpret(self, tree, table):
        function = tree.setFunctions(self._id, self)
        
        if function == 'error':
            error = Exceptions('Semantyc', f'Ya existe la funcion {self._id}', self.row, self.column)
            return error
        
        genAux = Generator()
        generator = genAux.getInstance()
        generator.addComment(f'Compilation for the function {self._id}')
        
        env = Table(table)
        
        Lblreturn = generator.newLabel()
        env.returnLbl = Lblreturn
        env.size = 1
        
        if self.params != None:
            for param in self.params:
                if param['_type'] == 'struct':
                    symbol = env.setTable(param['_id'], param['_type'], True)
                elif not isinstance(param['_type'], List):
                    symbol = env.setTable(param['_id'], param['_type'], (param['_type'] == 'string' or param['_type'] == 'array' or param['_type'] == 'struct'))
                else:
                    symbol = env.setTable(param['_id'], param['_type'][0], True)
                    symbol.setTipoAux(param['_type'][1])
                    if param['_type'][0] == 'struct':
                        struct = tree.getStruct(param['_type'][1])
                        symbol.setParams(struct.getParams())

        generator.addBeginFunc(self._id)
        
        for statement in self.statements:
            valueInterpret = statement.interpret(tree, env)
            if isinstance(valueInterpret, Exceptions):
                tree.setExceptions(valueInterpret)
            if isinstance(valueInterpret, Return):
                if valueInterpret.getTrueLbl() == '':
                    generator.addComment('Resultado a retornar en la funcion')
                    generator.setStack('P',valueInterpret.value)
                    generator.addGoto(env.returnLbl)
                    generator.addComment('Fin del resultado a retornar')
                else:
                    generator.addComment('Resultado a retornar en la funcion')
                    generator.putLabel(valueInterpret.getTrueLbl())
                    generator.setStack('P', '1')
                    generator.addGoto(env.returnLbl)
                    generator.putLabel(valueInterpret.getFalseLbl())
                    generator.setStack('P', '0')
                    generator.addGoto(env.returnLbl)
                generator.addComment('Fin del resultado a retornar')
        generator.addGoto(Lblreturn)
        generator.putLabel(Lblreturn)
        generator.addComment(f'End of compilation for function {self._id}')
        generator.addEndFunc()
        generator.addSpace()
        return

    def getParams(self):
        return self.params

    def getType(self):
        return self._type

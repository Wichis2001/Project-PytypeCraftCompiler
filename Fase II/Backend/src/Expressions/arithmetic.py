from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Abstract.return_ import Return
from ..Abstract.instruction import Instruction
from ..Symbol_Table.generator import Generator
from ..Instructions.function_call import Function_Call
class Arithmetic(Abstract):

    def __init__(self, left_op, right_op, arith_op, row, column, prueba = False ):
        self.left_op = left_op
        self.right_op = right_op
        self.arith_op = arith_op
        self._type = None
        self.prueba = prueba
        super().__init__(row, column)

    def interpret(self, tree, table):
        genAux = Generator()
        generator = genAux.getInstance();
        temporal = ''
        operator = ''
        left = ''
        right = ''
        if self.left_op != None:
            left = self.left_op.interpret(tree, table)
            if isinstance(left, Exceptions):
                return left

        if self.right_op != None:
            if isinstance(self.right_op, Function_Call):
                print('si soy instancia')
                self.right_op.guardarTemps(generator, table, [left.getValue()])
                right = self.right_op.interpret(tree, table)
                if isinstance(right, Exceptions): return right
                self.right_op.recuperarTemps(generator, table, [left.getValue()])
            else:
                right = self.right_op.interpret(tree, table)
                if isinstance(right, Exceptions):
                    return right

        left_type = left.getType()
        right_type = right.getType()
        op = self.arith_op

        if left_type == right_type == 'number':
            if( op == '-'):
                operator = '-'
                temporal = generator.addTemp()
                generator.addExp( temporal, left.getValue(), right.getValue(), operator)
                self._type = 'number'
                return Return( temporal, self._type, True)
            elif( op == '+' ):
                operator = '+'
                temporal = generator.addTemp()
                generator.addExp( temporal, left.getValue(), right.getValue(), operator)
                self._type = 'number'
                return Return( temporal, self._type, True)
            elif( op == '*' ):
                operator = '*'
                temporal = generator.addTemp()
                print( right )
                generator.addExp( temporal, left.getValue(), right.getValue(), operator)
                self._type = 'number'
                return Return( temporal, self._type, True)
            elif( op == '/' ):
                temporal = generator.addTemp()
                label1 = generator.newLabel()
                generator.addIf(right.getValue(), '0', '!=', label1)
                error = 'Math Error \n'
                for char in error:
                    generator.addPrint('c', ord(char))
                temporal2 = generator.addTemp()
                generator.addExp(temporal2, '0', '', '')
                label2 = generator.newLabel()
                generator.addGoto( label2 )
                generator.putLabel( label1 )
                if( (right.getValue() != '0') == True ):
                    generator.addExp(temporal, left.getValue(), right.getValue(), op)
                generator.putLabel( label2 )
                self._type = 'number'
                return Return( temporal, self._type, True)
            elif( op == '%'):
                temporal = generator.addTemp()
                label1 = generator.newLabel()
                generator.addIf(right.getValue(), '0', '!=', label1)
                error = 'Math Error \n'
                for char in error:
                    generator.addPrint('c', ord(char))
                temporal2 = generator.addTemp()
                generator.addExp(temporal2, '0', '', '')
                label2 = generator.newLabel()
                generator.addGoto( label2 )
                generator.putLabel( label1 )
                if( (right.getValue() != '0') == True ):
                    generator.setImport('math')
                    generator.addModulo( temporal, left.getValue(), right.getValue())
                generator.putLabel( label2 )
                self._type = 'number'
                return Return( temporal, self._type, True)
            elif( op == '^'):
                temporal = generator.addTemp()
                generator.fPotencia()

                t5 = generator.addTemp()
                generator.addExp( t5, 'P', table.size, '+')
                generator.addExp( t5, t5, '1', '+')

                generator.setStack( t5, left.getValue())
                generator.addExp( t5, t5, '1', '+')
                generator.setStack(t5, right.getValue())

                generator.newEnv( table.size )
                generator.callFun('potencia')

                generator.getStack(temporal, 'P')

                generator.retEnv( table.size )

                self._type = 'number'
                return Return( temporal, self._type, True )
        elif left_type == right_type == 'string':
                generator.fconcatString()
                t8 = generator.addTemp()
                t9 = generator.addTemp()

                generator.addExp(t8, 'P', table.size,'+' )
                generator.addExp(t8, t8, '1', '+')

                generator.setStack(t8, left.getValue())
                generator.addExp(t8, t8, '1', '+')
                generator.setStack(t8, right.getValue())

                generator.newEnv(table.size)
                generator.callFun('concatString')
                generator.getStack(t9, 'P')
                generator.retEnv(table.size)

                self._type = 'string'
                return Return(t9, self._type, False)
        else:
            message = 'It is not possible to operate with other types of data ( ' + left_type + ' ' + op + ' ' + right_type + ' )'
            return Exceptions('Semantic', message, self.row, self.column)

    def getType(self):
        return self._type
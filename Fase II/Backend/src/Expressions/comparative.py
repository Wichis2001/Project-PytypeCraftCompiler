from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.generator import Generator
from ..Abstract.return_ import Return
from typing import List
class Comparative(Abstract):

    def __init__(self, left_op, right_op, comp_op, row, column):
        self.left_op = left_op
        self.right_op = right_op
        self.comp_op = comp_op
        self._type = None
        super().__init__(row, column)

    def interpret(self, tree, table):
        genAux = Generator()
        generator = genAux.getInstance()
        left = self.left_op.interpret(tree, table)
        if isinstance( left, Exceptions ):
            return left
        left_type = self.left_op.getType()

        right = self.right_op.interpret(tree, table)
        if isinstance( right, Exceptions ):
            return right
        right_type = self.right_op.getType()
        op = self.comp_op

        if left_type == right_type and left_type in ['string', 'number', 'boolean'] or left == None or right == None:
            result = Return(None, 'boolean', False)
            self._type = 'boolean'
            if left_type != 'boolean':
                if((left.getType() == 'number') and (right.getType() == 'number')):
                    self.checkLabels()
                    if(op == '==='):
                       op='=='
                    elif(op=='!=='):
                        op='!='
                    generator.addIf( left.getValue(), right.getValue(), op, self.getTrueLbl())
                    generator.addGoto(self.getFalseLbl())
                elif((left.getType() == 'string') and (right.getType() == 'string')):
                    if op == '===' or op == '!==':
                        generator.fcompareString()
                        paramTemp = generator.addTemp()

                        generator.addExp(paramTemp, 'P', table.size, '+')
                        generator.addExp(paramTemp, paramTemp, 1, '+')
                        generator.setStack(paramTemp, left.getValue())

                        generator.addExp(paramTemp, paramTemp, 1, '+')
                        generator.setStack(paramTemp, right.getValue())

                        generator.newEnv(table.size)
                        generator.callFun('compareString')

                        temp = generator.addTemp()
                        generator.getStack(temp, 'P')
                        generator.retEnv(table.size)

                        self.checkLabels()
                        generator.addIf(temp, self.getNum(), "==", self.trueLbl)
                        generator.addGoto(self.falseLbl)

                        result.trueLbl = self.trueLbl
                        result.falseLbl = self.falseLbl
                        return result
                    else:
                        generator.frelationalString(self.getOperador())
                        paramTemp = generator.addTemp()

                        generator.addExp(paramTemp, 'P', table.size, '+')
                        generator.addExp(paramTemp, paramTemp, '1', '+')
                        generator.setStack(paramTemp, left.getValue())

                        generator.addExp(paramTemp, paramTemp, '1', '+')
                        generator.setStack(paramTemp, right.getValue())

                        generator.newEnv(table.size)
                        if self.getOperador() == '>':
                            generator.callFun('relationalStringMayor')
                        elif self.getOperador() == '<':
                            generator.callFun('relationalStringMenor')
                        elif self.getOperador() == '>=':
                            generator.callFun('relationalStringMayorIgual')
                        elif self.getOperador() == '<=':
                            generator.callFun('relationalStringMenorIgual')

                        temp = generator.addTemp()
                        generator.getStack(temp, 'P')
                        generator.retEnv(table.size)

                        self.checkLabels()
                        generator.addIf(temp,'1', "==", self.trueLbl)
                        generator.addGoto(self.falseLbl)

                        result.trueLbl = self.trueLbl
                        result.falseLbl = self.falseLbl
                        return result
            else:
                if(op == '==='):
                    op='=='
                elif(op=='!=='):
                    op='!='
                gotoRight = generator.newLabel()
                leftTmp  = generator.addTemp()

                generator.putLabel(left.getTrueLbl())
                generator.addExp(leftTmp, '1', '','')
                generator.addGoto(gotoRight)

                generator.putLabel(left.getFalseLbl())
                generator.addExp(leftTmp, '0', '','')

                generator.putLabel(gotoRight)

                right = self.right_op.interpret(tree, table)
                if right._type != 'boolean':
                    print("Error, no se pueden comparar")
                    return Exceptions("Semantico","No se pueden comparar", self.row, self.column)

                gotoEnd = generator.newLabel()
                rightTemp = generator.addTemp()

                generator.putLabel(right.trueLbl)
                generator.addExp(rightTemp, '1', '', '')
                generator.addGoto(gotoEnd)

                generator.putLabel(right.getFalseLbl())
                generator.addExp(rightTemp, '0', '', '')
                generator.putLabel(gotoEnd)

                self.checkLabels()
                generator.addIf(leftTmp, rightTemp, op, self.trueLbl)
                generator.addGoto(self.falseLbl)

            generator.addComment('End compilation of rational expression')
            generator.addSpace()

            result.trueLbl = self.trueLbl
            result.falseLbl = self.falseLbl
            return result
        else:
            message = 'It is not possible to operate with other types of data: ' + left_type + ' ↔ ' + right_type
            return Exceptions('Error', message, self.row, self.column)

    def getNum(self):
        if self.comp_op == '===':
            return '1'
        if self.comp_op == '!==':
            return '0'

    def getOperador(self):
        if self.comp_op == '===':
            return '=='
        elif self.comp_op == '!==':
            return '!='
        elif self.comp_op == '>':
            return '>'
        elif self.comp_op == '<':
            return '<'
        elif self.comp_op == '>=':
            return '>='
        elif self.comp_op == '<=':
            return '<='
        return self.comp_op

    def checkLabels(self):
        genAux = Generator()
        generator = genAux.getInstance()
        if self.trueLbl == '':
            self.trueLbl = generator.newLabel()
        if self.falseLbl == '':
            self.falseLbl = generator.newLabel()

    def getType(self):
        return self._type
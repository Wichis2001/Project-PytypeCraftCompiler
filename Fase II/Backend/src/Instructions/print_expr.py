from ..Abstract.abstract import Abstract
from ..Symbol_Table.exceptions import Exceptions
from ..Symbol_Table.symbol import Symbol
from ..Symbol_Table.generator import Generator
from ..Abstract.return_ import Return
class Print_Expr(Abstract):

    def __init__(self, expr, row, column):
        self.expr = expr
        super().__init__(row, column)

    def interpret(self, tree, table):
        genAux = Generator()
        generator = genAux.getInstance()
        for expr in self.expr:
            value = expr.interpret(tree, table)
            if isinstance(value, Exceptions):
                return value
            if value.getType() == 'number':
                generator.addPrint('f', value.getValue())
            elif value.getType() == 'string':
                generator.fPrintString()

                paramTemp = generator.addTemp()

                generator.addExp(paramTemp, 'P', table.size, '+')
                generator.addExp(paramTemp, paramTemp, 1, '+')
                generator.setStack(paramTemp, value.getValue())

                generator.newEnv(table.size)
                generator.callFun('printString')

                temp = generator.addTemp()
                generator.getStack(temp, 'P')
                generator.retEnv(table.size)
            elif value.getType() == 'boolean':
                tempLbl = generator.newLabel()

                generator.putLabel(value.getTrueLbl())
                generator.printTrue()

                generator.addGoto(tempLbl)

                generator.putLabel(value.getFalseLbl())
                generator.printFalse()

                generator.putLabel(tempLbl)

        generator.addPrintChar( 10)
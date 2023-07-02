class Generator:

    generator = None

    def __init__( self ):

        #!Definición de Contadores
        self.count_temp = 0
        self.count_label = 0

        #!Definición de Código
        self.codigo = ''
        self.funciones = ''
        self.nativas = ''
        self.inFunciones = False
        self.inNativas = False

        #!Listado de Temporales
        self.temporales = []

        #?Listado de Nativas
        self.printString = False
        self.compareString = False
        self.boundError = False
        self.upper = False
        self.lower = False
        self.potencia = False
        self.concatString = False

        #*Listado de operadors racionales
        self.relacionales = ['>', '<', '>=', '<=']

        #*Listado de Imports
        self.imports = []
        self.imports2 = ['fmt', 'math']

    def getInstance(self):
        if Generator.generator == None:
            Generator.generator = Generator()
        return Generator.generator

    def cleanAll( self ):
        #!Limpiando Temporales y Labels
        self.count_temp = 0
        self.count_label = 0

        #!Limpiando la definicón del Código
        self.codigo = ''
        self.funciones = ''
        self.nativas = ''
        self.inFunciones = False
        self.inNativas = False
        self.concatString = False
        self.relationalString = False

        #!Limpiando el listado de Temporales
        self.temporales = []

        #?Limpiando el listado de Nativas
        self.printString = False
        self.compareString = False
        self.boundError = False
        self.upper = False
        self.lower = False
        self.potencia = False

        #*Limpiando las importaciones
        self.imports = []
        self.imports2 = ['fmt', 'math']
        Generator.generator = Generator()

    #?############
    #! IMPORTS
    #?############
    def setImport(self, lib):
        if lib in self.imports2:
            self.imports2.remove(lib)
        else:
            return
        code = f'import(\n\t"{lib}"\n)\n'

    #?############
    #! CODE
    #?############
    def getHeader(self):
        code = '/* ---- HEADER ----- */\npackage main;\n\n'
        if len(self.imports) > 0:
            for temp in self.imports:
                code += temp
        if len(self.temporales) > 0:
            code += 'var '
            for temp in self.temporales:
                code += temp + ','
            code = code[:-1]
            code += " float64;\n\n"
        code += "var P, H float64;\nvar stack[30101999] float64;\nvar heap[30101999] float64;\n\n"
        return code

    def getCode(self):
        return f'{self.getHeader()}{self.nativas}{self.funciones}\nfunc main(){{\n{self.codigo}\n}}'

    def codeIn(self, code, tab="\t"):
        if self.inNativas:
            if  self.nativas == '':
                self.nativas = self.nativas + '/* --- NATIVAS --- */\n'
            self.nativas = self.nativas + tab + code
        elif self.inFunciones:
            if self.funciones == '':
                self.funciones = self.funciones + '/* --- FUNCION --- */\n'
            self.funciones = self.funciones + tab + code
        else:
            self.codigo = self.codigo + tab + code

    def addComment(self, comment):
        self.codeIn(f'/* {comment} */\n')

    def addSpace(self):
        self.codeIn('\n')

    #?############
    #! Manejo de Temporales
    #?############
    def addTemp(self):
        temp = f't{self.count_temp}'
        self.count_temp += 1
        self.temporales.append(temp)
        return temp

    #?############
    #! Manejo de Labels
    #?############
    def newLabel(self):
        label = f'L{self.count_label}'
        self.count_label += 1
        return label

    def putLabel(self, label):
        self.codeIn(f'{label}:\n')

    def addIdent(self):
        self.codeIn("")

    #?############
    #! GoTo
    #?############
    def addGoto(self, label):
        self.codeIn(f'goto {label};\n')

    #?############
    #! Expresión If
    #?############
    def addIf(self, left, right, op, label):
        self.codeIn(f'if {left} {op} {right} {{goto {label};}}\n')

    #?############
    #! Expresiones
    #?############
    def addExp(self, result, left, right, op):
        self.codeIn(f'{result} = {left} {op} {right};\n')

    def addModulo(self, result, left, right):
        self.codeIn(f'{result} = math.Mod({left}, {right});\n')

    def addAsign(self, result, left):
        self.codeIn(f'{result} = {left};\n')

    #?############
    #! Funciones
    #?############
    def addBeginFunc(self, id):
        if not self.inNativas:
            self.inFunciones = True
        self.codeIn(f'func {id}(){{\n')

    def addEndFunc(self):
        self.codeIn('return;\n}\n');
        if(not self.inNativas):
            self.inFunciones = False

    #?############
    #! Heap
    #?############
    def getHeap(self, place, pos):
        self.codeIn(f'{place} = heap[int({pos})];\n')

    def setHeap(self, pos, value):
        self.codeIn(f'heap[int({pos})] = {value};\n')

    def nextHeap(self):
        self.codeIn('H = H + 1;\n')

    #?############
    #! Stack
    #?############
    def getStack(self, place, pos):
        self.codeIn(f'{place} = stack[int({pos})];\n')

    def setStack(self,pos, value):
        self.codeIn(f'stack[int({pos})] = {value};\n')

    #?############
    #! Environment
    #?############
    def newEnv(self, size):
        self.codeIn(f'P = P + {size};\n')

    def callFun(self, id):
        self.codeIn(f'{id}();\n')

    def retEnv(self, size):
        self.codeIn(f'P = P - {size};\n')

    #?############
    #! Instrucciones
    #?############
    def addPrint(self, type, value):
        self.setImport('fmt')
        self.codeIn(f'fmt.Printf("%{type}", {value});\n')

    def addPrintChar(self, value):
        self.setImport('fmt')
        self.codeIn(f'fmt.Printf("%c", int({value}));\n')

    def printTrue(self):
        self.setImport('fmt')
        self.addIdent()
        self.addPrint("c", 116)#*T
        self.addIdent()
        self.addPrint("c", 114)#*R
        self.addIdent()
        self.addPrint("c", 117)#*U
        self.addIdent()
        self.addPrint("c", 101)#*E

    def printFalse(self):
        self.setImport('fmt')
        self.addIdent()
        self.addPrint("c", 102)#*F
        self.addIdent()
        self.addPrint("c", 97)#*A
        self.addIdent()
        self.addPrint("c", 108)#*L
        self.addIdent()
        self.addPrint("c", 115)#*S
        self.addIdent()
        self.addPrint("c", 101)#*E

    #?############
    #! Nativas
    #?############
    def fPotencia(self):
        if self.potencia:
            return
        self.potencia = True
        self.inNativas = True
        self.addBeginFunc('potencia')

        # Labels a utilizar
        Lbl0 = self.newLabel()
        Lbl1 = self.newLabel()
        Lbl2 = self.newLabel()
        Lbl3 = self.newLabel()

        # Temporales a utilizar
        t1 = self.addTemp()
        t2 = self.addTemp()
        t3 = self.addTemp()
        t4 = self.addTemp()

        #Escritura del codigo
        self.addExp(t2, 'P', '1','+')
        self.getStack(t1, t2)
        self.addExp(t3,t1,'','')
        self.addExp(t4,t1,'','')
        self.addExp(t2,'P','2','+')
        self.getStack(t1,t2)
        self.addIf(t1,'0','==', Lbl1)
        self.putLabel(Lbl2)
        self.addIdent()
        self.addIf(t1, '1','<=',Lbl0)
        self.addIdent()
        self.addExp(t3, t3,t4,'*')
        self.addIdent()
        self.addExp(t1,t1,'1', '-')
        self.addIdent()
        self.addGoto(Lbl2)
        self.putLabel(Lbl0)
        self.addIdent()
        self.setStack('P', t3)
        self.addIdent()
        self.addGoto(Lbl3)
        self.putLabel(Lbl1)
        self.addIdent()
        self.setStack('P', '1')
        self.putLabel(Lbl3)
        self.addEndFunc()
        self.addSpace()
        self.inNativas = False

    def fconcatString(self):
        if self.concatString:
            return
        self.concatString = True
        self.inNativas = True

        self.addBeginFunc('concatString')

        returnLbl = self.newLabel()
        Lbl1 = self.newLabel()
        Lbl2 = self.newLabel()
        Lbl3 = self.newLabel()
        t3 = self.addTemp()
        t4 = self.addTemp()
        t5 = self.addTemp()
        t6 = self.addTemp()
        t7 = self.addTemp()

        self.addExp(t3, 'H', '', '')
        self.addExp(t4,'P', '1', '+')
        self.getStack(t6, t4)
        self.addExp(t5, 'P', '2', '+')

        self.putLabel(Lbl1)
        self.addIdent()

        self.getHeap(t7, t6)
        self.addIdent()

        self.addIf(t7, '-1','==', Lbl2)
        self.addIdent()
        self.setHeap('H', t7)
        self.addIdent()
        self.addExp('H', 'H','1','+')
        self.addIdent()
        self.addExp(t6,t6,'1', '+')
        self.addIdent()
        self.addGoto(Lbl1)

        self.putLabel(Lbl2)

        self.addIdent()
        self.getStack(t6,t5)

        self.putLabel(Lbl3)
        self.addIdent()
        self.getHeap(t7, t6)
        self.addIdent()
        self.addIf(t7, '-1','==', returnLbl)
        self.addIdent()
        self.setHeap('H', t7)
        self.addIdent()
        self.addExp('H', 'H','1','+')
        self.addIdent()
        self.addExp(t6,t6,'1', '+')
        self.addIdent()
        self.addGoto(Lbl3)

        self.putLabel(returnLbl)
        self.addIdent()
        self.setHeap('H', '-1')
        self.addIdent()
        self.addExp('H', 'H', '1', '+')
        self.addIdent()
        self.setStack('P', t3)
        self.addEndFunc()
        self.inNativas = False

    def fcompareString(self):
        if self.compareString:
            return
        self.compareString = True
        self.inNativas = True

        self.addBeginFunc("compareString")
        #!Label para salir de la funcion
        returnLbl = self.newLabel()

        t2 = self.addTemp()
        self.addExp(t2, 'P', '1', '+')
        t3 = self.addTemp()
        self.getStack(t3, t2)
        self.addExp(t2,t2,'1', '+')
        t4 = self.addTemp()
        self.getStack(t4, t2)

        l1 = self.newLabel()
        l2 = self.newLabel()
        l3 = self.newLabel()
        self.putLabel(l1)

        t5 = self.addTemp()
        self.addIdent()
        self.getHeap(t5,t3)

        t6 = self.addTemp()
        self.addIdent()
        self.getHeap(t6,t4)

        self.addIdent()
        self.addIf(t5,t6,'!=', l3)
        self.addIdent()
        self.addIf(t5,'-1', '==', l2)

        self.addIdent()
        self.addExp(t3, t3,'1', '+')
        self.addIdent()
        self.addExp(t4, t4,'1','+')
        self.addIdent()
        self.addGoto(l1)

        self.putLabel(l2)
        self.addIdent()
        self.setStack('P', '1')
        self.addIdent()
        self.addGoto(returnLbl)
        self.putLabel(l3)
        self.addIdent()
        self.setStack('P', '0')
        self.putLabel(returnLbl)
        self.addEndFunc()
        self.inNativas = False

    def frelationalString(self, op):
        if op in self.relacionales:
            self.relacionales.remove(op)
        else:
            return

        if op == '>':
            self.addBeginFunc('relationalStringMayor')
        elif op == '<':
            self.addBeginFunc('relationalStringMenor')
        elif op == '>=':
            self.addBeginFunc('relationalStringMayorIgual')
        elif op == '<=':
            self.addBeginFunc('relationalStringMenorIgual')


        t1 = self.addTemp()
        t2 = self.addTemp()
        t3 = self.addTemp()
        t4 = self.addTemp()
        t5 = self.addTemp()
        t6 = self.addTemp()
        t7 = self.addTemp()

        Lbl1 = self.newLabel()
        Lbl2 = self.newLabel()
        Lbl3 = self.newLabel()
        Lbl4 = self.newLabel()
        Lbl5 = self.newLabel()
        Lbl6 = self.newLabel()

        self.addExp(t1, 'P', '1','+')
        self.getStack(t2, t1)
        self.addExp(t1, t1,'1','+')
        self.getStack(t3, t1)
        self.addExp(t4,'0','','')
        self.addExp(t6,'0','','')

        self.putLabel(Lbl1)
        self.addIdent()
        self.getHeap(t5, t2)
        self.addIdent()
        self.addIf(t5, '-1','==', Lbl2)
        self.addIdent()
        self.addExp(t4, t4, t5, '+')
        self.addIdent()
        self.addExp(t2, t2,'1','+')
        self.addIdent()
        self.addGoto(Lbl1)

        self.putLabel(Lbl2)
        self.addIdent()
        self.getHeap(t7, t3)
        self.addIdent()
        self.addIf(t7,'-1','==', Lbl3)
        self.addIdent()
        self.addExp(t6, t6, t7,'+')
        self.addIdent()
        self.addExp(t3,t3,'1','+')
        self.addIdent()
        self.addGoto(Lbl2)

        self.putLabel(Lbl3)
        self.addIdent()
        self.addIf(t4, t6, op, Lbl4)
        self.addIdent()
        self.addGoto(Lbl5)

        self.putLabel(Lbl4)
        self.addIdent()
        self.setStack('P', '1')
        self.addIdent()
        self.addGoto(Lbl6)

        self.putLabel(Lbl5)
        self.addIdent()
        self.setStack('P', '0')

        self.putLabel(Lbl6)
        self.addEndFunc()
        self.addSpace()

        self.inNativas = False

    def fPrintString(self):
        self.setImport('fmt')
        if(self.printString):
            return
        self.printString = True
        self.inNativas = True

        self.addBeginFunc('printString')
        # Label para salir de la funcion
        returnLbl = self.newLabel()
        # Label para la comparacion para buscar fin de cadena
        compareLbl = self.newLabel()
        # Temporal puntero a Stack
        tempP = self.addTemp()
        # Temporal puntero a Heap
        tempH = self.addTemp()
        self.addExp(tempP, 'P', '1', '+')
        self.getStack(tempH, tempP)
        # Temporal para comparar
        tempC = self.addTemp()
        self.putLabel(compareLbl)
        self.addIdent()
        self.getHeap(tempC, tempH)
        self.addIdent()
        self.addIf(tempC, '-1', '==', returnLbl)
        self.addIdent()
        self.addPrintChar(tempC)
        self.addIdent()
        self.addExp(tempH, tempH, '1', '+')
        self.addIdent()
        self.addGoto(compareLbl)
        self.putLabel(returnLbl)
        self.addEndFunc()
        self.inNativas = False

    def fboundError(self):
        if self.boundError:
            return
        self.boundError = True
        self.inNativas = True
        self.addBeginFunc('BoundsError')
        error = "Bounds Error \n"
        for char in error:
            self.addPrint("c",ord(char))
        self.addEndFunc()
        self.addSpace()
        self.inNatives = False

    def fUpperCase(self):
        if self.upper:
            return
        self.upper = True
        self.inNativas = True

        self.addBeginFunc('toUpperCase')

        t1 = self.addTemp()
        t2 = self.addTemp()
        t3 = self.addTemp()

        Lbl0 = self.newLabel()
        Lbl1 = self.newLabel()
        Lbl2 = self.newLabel()

        self.addAsign(t1, 'H')
        self.addExp(t2, 'P', '1','+')
        self.getStack(t2, t2)
        self.putLabel(Lbl0)

        self.getHeap(t3, t2)
        self.addIf(t3, '-1', '==', Lbl2)
        self.addIf(t3, '97', '<', Lbl1)
        self.addIf(t3, '122', '>', Lbl1)
        self.addExp(t3, t3,'32', '-')
        self.putLabel(Lbl1)

        self.setHeap('H', t3)
        self.nextHeap()
        self.addExp(t2, t2, '1','+')
        self.addGoto(Lbl0)

        self.putLabel(Lbl2)
        self.setHeap('H', '-1')
        self.nextHeap()
        self.setStack('P', t1)
        self.addEndFunc()

        self.inNativas = False

    def fLowerCase(self):
        if self.lower:
            return
        self.lower = True
        self.inNativas = True

        self.addBeginFunc('toLowerCase')

        t1 = self.addTemp()
        t2 = self.addTemp()
        t3 = self.addTemp()

        Lbl0 = self.newLabel()
        Lbl1 = self.newLabel()
        Lbl2 = self.newLabel()

        self.addAsign(t1, 'H')
        self.addExp(t2, 'P', '1','+')
        self.getStack(t2, t2)
        self.putLabel(Lbl0)

        self.getHeap(t3, t2)
        self.addIf(t3, '-1', '==', Lbl2)
        self.addIf(t3, '65', '<', Lbl1)
        self.addIf(t3, '90', '>', Lbl1)
        self.addExp(t3, t3,'32', '+')
        self.putLabel(Lbl1)
    
        self.setHeap('H', t3)
        self.nextHeap()
        self.addExp(t2, t2, '1','+')
        self.addGoto(Lbl0)

        self.putLabel(Lbl2)
        self.setHeap('H', '-1')
        self.nextHeap()
        self.setStack('P', t1)
        self.addEndFunc()

        self.inNativas = False
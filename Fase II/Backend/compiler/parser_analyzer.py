'''
Analizador Sintactico

Este en un analizador sintactico utilizando Yacc de Ply

Fecha: 05/06/2023
'''
from compiler.ply import yacc
from compiler.lexer_analyzer import tokens, lexer, errores, find_column
from src.Expressions.identificator import Identificator
from src.Expressions.array import Array
from src.Instructions.array_id import Array_Id
from src.Instructions.array_call import Array_Call
from src.Instructions.assign_array import Assign_Array
from src.Expressions.primitive import Primitive
from src.Expressions.arithmetic import Arithmetic
from src.Expressions.comparative import Comparative
from src.Expressions.logic import Logic
from src.Expressions.unary import Unary
from src.Instructions.var_declaration import Var_Declaration
from src.Instructions.print_expr import Print_Expr
from src.Instructions.assign import Assign
from src.Instructions.function import Function
from src.Instructions.function_call import Function_Call
from src.Instructions.return_expr import Return
from src.Instructions.break_expr import Break
from src.Instructions.continue_expr import Continue
from src.Instructions.if_conditional import If
from src.Natives.toFixed import ToFixed
from src.Natives.toExponential import ToExponential
from src.Natives.toString import ToString
from src.Natives.toLowerCase import ToLowerCase
from src.Natives.toUpperCase import ToUpperCase
from src.Natives.split import Split
from src.Natives.concat import Concat
from src.Natives.push import Push
from src.Natives.pop import Pop
from src.Natives.length import Length
from src.Natives.type_of import Type_Of
from src.Instructions.while_loop import While
from src.Instructions.for_loop import For
from src.Instructions.for_of_loop import ForOf
from src.Expressions.interface_expr import Interface_Expr
from src.Instructions.interface_id import Interface_Id
from src.Instructions.interface_assign import Interface_Assign
from src.Expressions.interface_atrb_value import Interface_Atrb_Value
from src.Instructions.interface import Interface

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'EQUAL', 'UNEQUAL'),
    ('left', 'LESS_THAN', 'LESS_THAN_OR_EQUAL', 'GREATHER_THAN', 'GREATHER_THAN_OR_EQUAL'),
    ('left', 'PLUS', 'MINUS', 'COMMA'),
    ('left', 'MULT', 'DIV', 'MOD'),
    ('right', 'POW'),
    ('right', 'UMINUS'),
    ('right', 'INCREMENT', 'DECREMENT'),
    ('left', 'L_PAREN', 'R_PAREN')
)

def p_program(t):
    'program    :   stmt_list'
    t[0] = t[1]
    
def p_optional_semicolon(t):
    '''
    optional_semicolon  :   SEMICOLON
                        |   
    '''
    t[0] = t[1] if len(t) == 2 else ''  
    
def p_stmt_list(t):
    '''
    stmt_list   :   stmt optional_semicolon
                |   stmt_list stmt optional_semicolon
    '''
    if len(t) == 4:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]
        
def p_type_id(t):
    'type_id   :   ID'
    t[0] = Interface_Id(t[1], t.lineno(1), find_column(input, t.slice[1]))
    
def p_data_type(t):
    '''
    data_type   :   STRING_TYPE
                |   NUMBER_TYPE
                |   BOOLEAN_TYPE
    '''
    t[0] = t[1]
    
def p_bracket_list(t):
    '''
    bracket_list    :   L_BRACKET R_BRACKET
                    |   bracket_list L_BRACKET R_BRACKET
    '''
    if len(t) == 3:
        t[0] = [1, t.lineno(1), find_column(input, t.slice[1])]
    else:
        temp = t[1][0] + 1
        t[0] = [temp, t[1][1], t[1][2]]
    
def p_type_array(t):
    'type_array :   data_type bracket_list'
    t[0] = Array_Id(t[1], t[2][0], t[2][1], t[2][2])


def p_null_value(t):
    'null_value :   NULL_TYPE'
    t[0] = Primitive('null', None, t.lineno(1), find_column(input, t.slice[1]))

def p_id_value(t):
    'id_value   :   ID'
    t[0] = Identificator(t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_boolean_value(t):
    '''
    boolean_value   :   TRUE
                    |   FALSE
    '''
    value = True if t[1] == 'true' else False
    t[0] = Primitive('boolean', value, t.lineno(1), find_column(input, t.slice[1]))

def p_number_value(t):
    'number_value   :   NUMBER'
    t[0] = Primitive('number', t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_string_value(t):
    'string_value   :   STRING'
    t[0] = Primitive('string', t[1], t.lineno(1), find_column(input, t.slice[1])) 

def p_values(t):
    '''
    values  :   string_value
            |   number_value
            |   boolean_value
            |   id_value
    '''
    t[0] = t[1]

def p_atrb(t):
    '''
    atrb    :   ID
            |   ID COLON data_type
    '''
    if len(t) == 2:
        t[0] = {'_id': t[1], '_type': 'any'}
    else:
        t[0] = {'_id': t[1], '_type': t[3]}
    
def p_atrb_list(t):
    '''
    atrb_list   :   atrb SEMICOLON
                |   atrb_list atrb SEMICOLON
    '''

    if len(t) == 3:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]
        
def p_atrb_expr(t):
    '''
    atrb_expr   :   ID COLON expr
                |   ID
    '''
    if len(t) == 2:
        t[0] = {'_id': t[1], 'expr': ''}
    else:
        t[0] = {'_id': t[1], 'expr': t[3]}
    
def p_atrb_expr_list(t):
    '''
    atrb_expr_list  :   atrb_expr
                    |   atrb_expr_list COMMA atrb_expr comma_prod
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]
        
def p_comma_prod(t):
    '''
    comma_prod  :   COMMA
                |   
    '''
    t[0] = t[1] if len(t) == 2 else ''
            
def p_array_expr(t):
    '''
    array_expr  :   L_BRACKET expr_list R_BRACKET
                |   L_BRACKET R_BRACKET
    '''
    if len(t) == 3:
        t[0] = Array([], t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Array(t[2], t.lineno(1), find_column(input, t.slice[1]))
        
def p_interface_stmt(t): 
    'interface_stmt :   INTERFACE ID L_BRACE atrb_list R_BRACE'
    t[0] = Interface(t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))

    
def p_interface_assignment(t):
    '''
    interface_assignment    :   ID DOT ID ASSIGN expr
                            |   ID DOT ID INCREMENT
                            |   ID DOT ID DECREMENT
    '''
    if len(t) == 6:
        t[0] = Interface_Assign(t[1], t[3], t[4], t[5], t.lineno(1), find_column(input, t.slice[1]))
    else:
        temp = Primitive('number', 1, t.lineno(1), find_column(input, t.slice[1]))
        t[0] = Interface_Assign(t[1], t[3], t[4], temp, t.lineno(1), find_column(input, t.slice[1]))

def p_interface_atrb_value(t):
    'interface_atrb_value   :   ID DOT ID'
    t[0] = Interface_Atrb_Value(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_interface_expr(t):
    '''
    interface_expr  :   L_BRACE atrb_expr_list R_BRACE
                    |   L_BRACE R_BRACE
    '''
    if len(t) == 4:
        t[0] = Interface_Expr(t[2], t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Interface_Expr(None, t.lineno(1), find_column(input, t.slice[1]))

def assignment_parameters(t):
    '''
    assignment_parameters : assignment_parameters DOT assignment_parameter
    '''
    t[1].append(t[3])
    t[0] = t[1]

def assign_parameter(t):
    '''
    assign_parameter :  assign_parameter
                     |  ID
    '''
    t[0] = t[1]


def p_expr(t):
    '''
    expr    :   L_PAREN expr R_PAREN
            |   arith_expr
            |   logic_expr
            |   comp_expr
            |   unary_expr
            |   values
            |   func_call
            |   interface_expr
            |   assign_expr
            |   array_expr
            |   array_call
            |   concat
            |   interface_assignment
            |   interface_atrb_value
            |   NUMBER
    '''
    t[0] = t[1] if t[1] != '(' else t[2]

def p_arith_expr(t):
    '''
    arith_expr  :   expr PLUS expr
                |   expr MINUS expr
                |   expr MULT expr
                |   expr DIV expr
                |   expr POW expr
                |   expr MOD expr
    '''
    t[0] = Arithmetic(t[1], t[3], t[2], t.lineno(2), find_column(input, t.slice[2]))

def p_logic_expr(t):
    '''
    logic_expr  :   expr AND expr
                |   expr OR expr
    '''
    t[0] = Logic(t[1], t[3], t[2], t.lineno(2), find_column(input, t.slice[2]))

def p_comp_expr(t):
    '''
    comp_expr   :   expr GREATHER_THAN expr
                |   expr LESS_THAN expr
                |   expr EQUAL expr
                |   expr UNEQUAL expr
                |   expr GREATHER_THAN_OR_EQUAL expr
                |   expr LESS_THAN_OR_EQUAL expr
    '''
    t[0] = Comparative(t[1], t[3], t[2], t.lineno(2), find_column(input, t.slice[2]))
    
def p_unary_expr(t):
    '''
    unary_expr  :   NOT expr
                |   MINUS expr %prec UMINUS
    '''
    t[0] = Unary(t[2], t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expr_list(t):
    '''
    expr_list   :   expr
                |   expr_list COMMA expr
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]
    
def p_stmt(t):
    '''
    stmt    :   var_declaration
            |   func_declaration
            |   func_call
            |   assign_expr
            |   if_stmt
            |   while_stmt
            |   for_stmt
            |   for_of_stmt
            |   print_stmt
            |   interface_stmt
            |   return_stmt
            |   break_stmt
            |   continue_stmt
            |   array_call
            |   interface_assignment
            |   push
            |   pop
    '''
    t[0] = t[1]
    
def p_var_declaration(t):
    '''
    var_declaration :   LET ID COLON data_type
                    |   LET ID COLON data_type ASSIGN expr
                    |   ID ASSIGN expr
    '''
    if len(t) == 5:
        t[0] = Var_Declaration(t[2], t[4], None, t.lineno(1), find_column(input, t.slice[1]))
    elif len(t) == 7:
        t[0] = Var_Declaration(t[2], t[4], t[6], t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Var_Declaration(t[1], None, t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_param(t):
    '''
    param   :   ID
            |   ID COLON data_type
            |   LET ID
            |   LET ID COLON data_type
    '''
    if len(t) == 2:
        t[0] = {'_type': 'any', '_id': t[1]}
    elif len(t) == 3:
        t[0] = {'_type': 'any', '_id': t[2]}
    elif len(t) == 4:
        t[0] = {'_type': t[3], '_id': t[1]}
    else: 
        t[0] = {'_type': t[4], '_id': t[2]}
    
def p_param_list(t):
    '''
    param_list  :   param
                |   param_list COMMA param
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]
    

def p_func_declaration(t):
    '''
    func_declaration    :   FUNCTION ID L_PAREN R_PAREN L_BRACE stmt_list R_BRACE
                        |   FUNCTION ID L_PAREN param_list R_PAREN L_BRACE stmt_list R_BRACE
                        |   FUNCTION ID L_PAREN R_PAREN COLON data_type L_BRACE stmt_list R_BRACE
                        |   FUNCTION ID L_PAREN param_list R_PAREN COLON data_type L_BRACE stmt_list R_BRACE
                        |   FUNCTION ID L_PAREN R_PAREN COLON VOID L_BRACE stmt_list R_BRACE
                        |   FUNCTION ID L_PAREN param_list R_PAREN COLON VOID L_BRACE stmt_list R_BRACE
    '''
    if len(t) == 8:
        t[0] = Function(t[2], None, None, t[6], t.lineno(1), find_column(input, t.slice[1]))
    elif len(t) == 9:
        t[0] = Function(t[2], t[4], None, t[7], t.lineno(1), find_column(input, t.slice[1]))
    elif len(t) == 10:
        t[0] = Function(t[2], None, t[6], t[8], t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Function(t[2], t[4], t[7], t[9], t.lineno(1), find_column(input, t.slice[1]))
        
def p_param_call(t):
    'param_call :   expr'
    t[0] = t[1]
    
def p_params_call(t):
    '''
    params_call :   param_call
                |   params_call COMMA param_call
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]

def p_func_call(t):
    '''
    func_call   :   ID L_PAREN R_PAREN
                |   ID L_PAREN params_call R_PAREN
    '''
    if len(t) == 4:
        t[0] = Function_Call(t[1], None, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Function_Call(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))
        
def p_locate(t):
    '''
    locate  :   L_BRACKET expr R_BRACKET
            |   locate L_BRACKET expr R_BRACKET
    '''
    if len(t) == 4:
        t[0] = [t[2]]
    else:
        t[1].append(t[3])
        t[0] = t[1]
        
def p_array_call(t):
    'array_call :   ID locate'
    t[0] = Array_Call(t[1], t[2], t.lineno(1), find_column(input, t.slice[1]))
    
def p_assing_array(t):
    '''
    assign_array    :   ID locate ASSIGN expr
                    |   ID locate INCREMENT
                    |   ID locate DECREMENT
    '''
    if len(t) == 5:
        t[0] = Assign_Array(t[1], t[3], t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))
    else:
        tmp = Primitive('number', 1, t.lineno(1), find_column(input, t.slice[1]))
        t[0] = Assign_Array(t[1], t[3], t[2], tmp, t.lineno(1), find_column(input, t.slice[1]))
    

def p_assign_expr(t):
    '''
    assign_expr :   ID INCREMENT
                |   ID DECREMENT
                |   assign_array
    '''
    if len(t) == 3:
        t[0] = Unary(t[1], t[2], t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = t[1]

def p_if_stmt(t):
    '''
    if_stmt :   IF conditional_if
    '''
    t[0] = t[2]

def p_conditional_if(t):
    '''
    conditional_if : L_PAREN expr R_PAREN L_BRACE stmt_list R_BRACE
    '''
    t[0] = If(t[2], t[5], None, None, t.lineno(1), find_column(input, t.slice[1]))

def p_conditional_if_else(t):
    '''
    conditional_if : L_PAREN expr R_PAREN L_BRACE stmt_list R_BRACE ELSE L_BRACE stmt_list R_BRACE
    '''
    t[0] = If(t[2], t[5], t[9], None, t.lineno(1), find_column(input, t.slice[1]) )

def p_conditional_if_else_if(t):
    '''
    conditional_if : L_PAREN expr R_PAREN L_BRACE stmt_list R_BRACE ELSE IF conditional_if
    '''
    t[0] = If(t[2], t[5], None, t[9], t.lineno(1), find_column(input, t.slice[1]))
    
def p_while_stmt(t):
    '''
    while_stmt  :   WHILE L_PAREN expr R_PAREN L_BRACE stmt_list R_BRACE
    '''
    t[0] = While(t[3], t[6], t.lineno(1), find_column(input, t.slice[1]))


def p_for_stmt(t):
    '''
    for_stmt : FOR for_stmt_loop
    '''
    t[0] = t[2]

def p_for_stmt_loop_var(t):
    '''
    for_stmt_loop   :   L_PAREN var_declaration SEMICOLON expr SEMICOLON assign_expr R_PAREN L_BRACE stmt_list R_BRACE
    '''
    t[0] = For(t[2], t[4], t[6], t[9], t.lineno(1), find_column(input, t.slice[1]))

def p_for_of_stmt(t):
    '''
    for_of_stmt :   FOR L_PAREN var_declaration OF expr R_PAREN L_BRACE stmt_list R_BRACE
                |   FOR L_PAREN expr OF expr R_PAREN L_BRACE stmt_list R_BRACE
    '''
    if( len(t) == 10):
        t[0] = ForOf( t[3], t[5],  t[8], t.lineno(1), find_column(input, t.slice[1]))
    else:
        print(len(t))

def p_print_stmt(t):
    'print_stmt :   CONSOLE DOT LOG L_PAREN expr_list R_PAREN'
    t[0] = Print_Expr(t[5], t.lineno(1), find_column(input, t.slice[1]))
    

def p_return_stmt(t):
    '''
    return_stmt :   RETURN expr
                |   RETURN 
    '''
    if len(t) == 3:
        t[0] = Return(t[2], t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Return(None, t.lineno(1), find_column(input, t.slice[1]))
    
def p_break_stmt(t):
    'break_stmt    :   BREAK'
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))
    
def p_continue_stmt(t):
    'continue_stmt    :   CONTINUE'
    t[0] = Continue(t.lineno(1), find_column(input, t.slice[1]))
    
def add_natives(ast):
    stmt_list = []
    
    # _id = "toFixed"
    # params = [{'_type': 'number', '_id': 'base_number'}, {'_type': 'number', '_id': 'fixed_number'}]
    # toFixed = ToFixed(_id, params, 'number', stmt_list, -1, -1)
    # ast.setFunctions(toFixed)
    
    # _id = "toExponential"
    # params = [{'_type': 'number', '_id': 'base_number'}, {'_type': 'number', '_id': 'exponential_number'}]
    # toExponential = ToExponential(_id, params, 'number', stmt_list, -1, -1)
    # ast.setFunctions(toExponential)
    
    # _id = "toString"
    # params = [{'_type': 'any', '_id': 'value'}]
    # toString = ToString(_id, params, 'string', stmt_list, -1, -1)
    # ast.setFunctions(toString)
    
    _id = "toLowerCase"
    params = [{'_type': 'string', '_id': 'tolowercase#Param1'}]
    toLowerCase = ToLowerCase(_id, params, 'string', stmt_list, -1, -1)
    ast.setFunctions('toLowerCase', toLowerCase)
    
    _id = "toUpperCase"
    params = [{'_type': 'string', '_id': 'touppercase#Param1'}]
    toUpperCase = ToUpperCase(_id, params, 'string', stmt_list, -1, -1)
    ast.setFunctions('toUpperCase', toUpperCase)
    
    # _id = 'split'
    # params = [{'_type': 'string', '_id': 'text'}, {'_type': 'string', '_id': 'split_caracter'}]
    # split = Split(_id, params, ['string', 1], stmt_list, -1, -1)
    # ast.setFunctions(split)
    
    # _id = 'length'
    # params = [{'_type': 'any', '_id': 'array'}]
    # length = Length(_id, params, 'number', stmt_list, -1, -1)
    # ast.setFunctions(length)
    
    # _id = 'typeof'
    # params = [{'_type': 'any', '_id': 'item'}]
    # type_op = Type_Of(_id, params, None, stmt_list, -1, -1)
    # ast.setFunctions(type_op)
    
def p_concat(t):
    'concat :   CONCAT L_PAREN expr_list R_PAREN'
    t[0] = Concat(t[3], t.lineno(1), find_column(input, t.slice[1]))
    
def p_push(t):
    'push   :   ID DOT PUSH L_PAREN expr R_PAREN'
    t[0] = Push(t[1], t[5], t.lineno(1), find_column(input, t.slice[1]))
    
def p_pop(t):
    'pop    :   ID DOT POP L_PAREN R_PAREN'
    t[0] = Pop(t[1], t.lineno(1), find_column(input, t.slice[1]))
    
def p_error(t):
    if t is not None:
        if t.type == 'error':
            print(" Error Léxico en '%s'" % t.value)
        else:
            print(" Error Sintáctico en '%s'" % t.value)
        parser.errok()
    else:
        print("Error sintactico, fín de archivo no esperado")

def parse(inp):
    global errores
    global parser
    errores = []
    parser = yacc.yacc()
    global input
    input = inp
    lexer.lineno = 1
    return parser.parse(inp)

#entrada = 'let x = 1531'

def test_lexer(lexer):
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)

# lexer.input(entrada)
# test_lexer(lexer)
#instrucciones = parse(entrada)




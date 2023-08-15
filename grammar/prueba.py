import ply.lex as lex
import ply.yacc as yacc

# Definición de tokens
reserved= {
    'if': 'IF',
}
tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
] + list(reserved.values())

# Expresiones regulares para tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ignore = ' \t'  # Ignorar espacios en blanco

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print(f"Caracter inesperado: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

# Reglas de gramática
def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]

def p_factor(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_error(p):
    print("Error de sintaxis:", p)

parser = yacc.yacc()

# Prueba del parser
input_text = '2 + 3 * 4 - 5 / 1'
result = parser.parse(input_text)
print("Resultado:", result)

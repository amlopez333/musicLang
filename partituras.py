#Tarea proyecto
#Andres Lopez-B43885
#Gramatica para crear partituras

#lista global para guardar los elementos de la partitura retornados por la produccion
listaValores = []

#imports
import ply.yacc as yacc
import ply.lex as lex
#metodos para crear el XML
import crearXml 



#lexer

tokens = ('id', 'm', 'cl', 't', 'n', 'dr', 'd')


def t_id(t):
    r'P[1-9]+'
    return t

def t_m(t):
    r'Com[1-9]+[0-9]*'
    t.value = t.value[3:]
    return t

def t_cl(t):
    r'Clef[1-7]'
    if(t.value[4]=="2"):
        t.value = "G2";
    return t

def t_t(t):
    r'([1-9])/(4|8|16)'
    return t

def t_n(t):
    r'([A-G]|R)[1-9]'
    return t

def t_dr(t):
    r'[1-4][whqes]'
    return t

def t_d(t):
    r'(d)'
    return t


t_ignore = " \t"

def t_error(t):
    print("Error lexico")
    t.lexer.skip(1)

def t_newline(t):
    r'\n'
    t.lexer.lineno += t.value.count("\n")
#crear lexer
lexer = lex.lex()


#parser
#Estas son las producciones
#Se deja un espacio entre simbolos por claridad

# S­>A

# A­>id m cl K t B 

# K­>k | ε 

# B­>n dr C D | ε

# C­>d | ε 

# D­>id m B | ε
#
def p_S(p):
    'S : A'
    

#para obtener los componentes en orden, se recorre
#la lista que contiene los tokens de la produccion
#del final hacia el principio. Esto para poder crear
#el XML en el orden apropiado.
    
def p_A(p):
    'A : id m cl t B'
    for x in range(len(p)-1, 0, -1):
        if(p[x] != None) :
            listaValores.insert(0,p[x])
   
def p_empty(p):
    'empty :'
    pass


       
def p_B(p):
    '''B : n dr C D
         | empty'''
    for x in range(len(p)-1, 0, -1):
        if (p[x] != None):
            listaValores.insert(0,p[x])
    
def p_D(p):
    '''D : id m B
         | empty'''
    for x in range(len(p)-1, 0, -1):
        if (p[x] != None):
            listaValores.insert(0,p[x])
    
def p_C(p):
    '''C : d 
         | empty'''
    for x in range(len(p)-1, 0, -1):
        if(p[x] != None) :
            listaValores.insert(0,p[x])
    
def p_error(p):
    print("Error de sintaxis")
   
    
#crear analizador sintactico
parser = yacc.yacc()
#funcion que crea la partitura
#recibe el nombre del archivo en el que se desea guardar
#la partitura.
def crearPartitura(fileName):
    scorePartWise = crearXml.setScorePartWise()
    partList = crearXml.setPartList(scorePartWise)
    idParte = listaValores.pop(0)
    crearXml.setScorePart(idParte, partList)
    part = crearXml.setPart(idParte, scorePartWise)
    currentId = idParte
    com = listaValores.pop(0)
    currentCom = com
    measure = crearXml.setMeasure(com, part)
    attributes = crearXml.setAttributes(measure)
    cl = listaValores.pop(0)
    time = listaValores.pop(0)
    crearXml.setTime(time, attributes)
    crearXml.setClef(cl, attributes)
    creatingXml = True
    while(len(listaValores)>0):
        
        nota = listaValores.pop(0)
        dur = listaValores.pop(0)
        crearXml.crearXml(measure, nota, dur)
        if(len(listaValores)>0):
            idParte = listaValores.pop(0)
            com = listaValores.pop(0)
            if(currentId != idParte):
                crearXml.setScorePart(idParte,partList)
                part=crearXml.setPart(idParte,scorePartWise)
                currentId = idParte
                measure = crearXml.setMeasure(com, part)
                attributes = crearXml.setAttributes(measure)
                crearXml.setTime(time, attributes)
                crearXml.setClef(cl, attributes)
                currentCom = com
            
            if(currentCom != com):
                measure = crearXml.setMeasure(com, part)
                currentCom = com
          
    crearXml.imprimir(fileName, scorePartWise)
    print("{} creado con exito \n\n\n".format(fileName))

#Main loop 
while(True):
    modoTrabajo = input('''Digite 1 para ingresar una cadena manualmente,
2 para leer cualquier archivo, y cualquier otro valor para salir \n''')
    if(modoTrabajo == "1"):
        prueba = input("cadena> " )
        fileName = input("Digite el nombre del archivo.xml a crear> ")
        parser.parse(prueba)
        crearPartitura(fileName)
    elif(modoTrabajo == "2"):
        file = input("Digite el nombre del archivo.txt> " )
        fileName = input("Digite el nombre del archivo.xml a crear> ")
        with open(file) as f:
            mylist = f.read().splitlines()
        prueba = ''.join(mylist)
        parser.parse(prueba)
        crearPartitura(fileName)
    else:
        break




    


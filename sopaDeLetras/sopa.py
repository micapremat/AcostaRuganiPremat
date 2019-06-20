import sys
import PySimpleGUI as sg
import random
import json
import string 


def matriz(longitud, cod):
    '''Se ingresan caracteres aleatorios en la matriz'''
    matriz = []
    for row in range(longitud):
        matriz.append([])
        for col in range(longitud):
            matriz[row].append(chr(random.randrange(cod, cod + 26)))
    return matriz

def grilla():
    '''Se arma la grilla para ingresar letras y palabras en la sopa de letras'''
    archiPalabras = open('palabras.txt','r')
    palabrasArch = archiPalabras.readlines()
    misPalabras = [] #palabras a usar del archivo
    for pal in range(len(palabrasArch)):
        misPal=palabrasArch[pal].strip()
        misPalabras.append(misPal)
    archiPalabras.close()
    maxLetras = 1
    for pal in misPalabras:
        if len(pal)>maxLetras:
            maxLetras = len(pal)
    tamCelda = 50
    #cantCeldas = max((len(x) for x in misPalabras))
    longitud = maxLetras*tamCelda
    cantCeldas = longitud//tamCelda

    grafico = [
            [sg.Graph((longitud,longitud), (0,longitud), (longitud,0), key='graph', change_submits=True, drag_submits=False)],
            [sg.Text('Ayuda:',font=('Roboto',12)),sg.Listbox('',key='ayuda', size=(20,2),disabled=True)],
            [sg.Cancel('Cerrar')]
            ]

    window = sg.Window('Sopa de letras').Layout(grafico).Finalize()
    graph = window.FindElement('graph')
    return cantCeldas,misPalabras,graph,window,tamCelda,longitud

def ayuda(palabras,window):
    '''Se activa la ayuda para que se muetren las palabras a buscar'''
    window.Element('ayuda').Update(disabled = False)
    window.Element('ayuda').Update(palabras)

def horizontal(grilla,palabras,cantCeldas,tamCelda,graph):
    '''Se ingresan las palabras en la sopa de letras para que esten en formato horizontal'''
    # Tomo al azar tantas filas como palabras haya
    random_col = random.sample(range(cantCeldas), len(palabras))
    for idx, palabra in enumerate(palabras):
        row = random.randrange(cantCeldas-len(palabra)+1)
        for letra in palabra:
            grilla[row][random_col[idx]] = letra
            row = row+1
    for row in range(cantCeldas):
        for col in range(cantCeldas):
            graph.DrawRectangle((col * tamCelda, row * tamCelda), (col * tamCelda + tamCelda, row * tamCelda + tamCelda), line_color='black')
            graph.DrawText(grilla[col][row], location=(col*tamCelda +tamCelda/2, row*tamCelda + tamCelda/2), color='black', font=('Helvetica',25), angle=0)

def vertical(grilla,palabras,cantCeldas,tamCelda,graph):
    # Tomo al azar tantas columnas como palabras haya
    '''Se ingresan las palabras en la sopa de letras para que esten en formato vertical'''
    random_row = random.sample(range(cantCeldas), len(palabras))
    for idx, palabra in enumerate(palabras):
        col = random.randrange(cantCeldas-len(palabra)+1)
        for letra in palabra:
            grilla[random_row[idx]][col] = letra
            col = col+1
    for row in range(cantCeldas):
        for col in range(cantCeldas):
            graph.DrawRectangle((col * tamCelda, row * tamCelda), (col * tamCelda + tamCelda, row * tamCelda + tamCelda), line_color='black')
            graph.DrawText(grilla[col][row], location=(col*tamCelda +tamCelda/2, row*tamCelda + tamCelda/2), color='black', font=('Helvetica',25), angle=0)

def comparoPalabra(palabras, letra, pos):
    '''Se compararn las letras que se seleccionan con las que estan en la matriz de la sopa de letras'''
    for i in palabras:
        if len(i) > pos:
            if (letra == i[pos].lower() or letra == i[pos].upper()):
                return True
    return False

def mainSopa():
    archConfig = open('configuracion.txt','r')
    archConf = json.load(archConfig)
    cantCeldas,palabras, graph,window, tamCelda, longitud=grilla()
    pala = []
    for arch in archConf:
        if arch['mayuscula'] == 'minuscula':
            cod = 97
            miMatriz = matriz(cantCeldas,cod)
        else:
            cod = 65
            miMatriz = matriz(cantCeldas,cod)
        if arch['ayuda'] == 'si':
            ayuda(palabras,window)
            print(palabras)

        if arch['orientacion'] == 'vertical':
            if arch['mayuscula'] == 'minuscula':
                for pal in palabras:
                    pala.append(pal.lower())
                vertical(miMatriz,pala,cantCeldas,tamCelda,graph)
            else:
                for pal in palabras:
                    pala.append(pal.upper())
                vertical(miMatriz,pala,cantCeldas,tamCelda,graph)
        else:
            if arch['mayuscula'] == 'minuscula':
                for pal in palabras:
                    pala.append(pal.lower())
                horizontal(miMatriz,pala,cantCeldas,tamCelda,graph)
            else:
                for pal in palabras:
                    pala.append(pal.upper())
                horizontal(miMatriz,pala,cantCeldas,tamCelda,graph)
    pos=0
    pal= ""
    listaCoordenadas=[]
    while True:
        button, values = window.Read()
        if button is None or button == 'Cerrar':
            break
        mouse = values['graph']
        if button == 'graph':
            if mouse == (None, None):
                continue
            box_x = mouse[0]//tamCelda
            box_y = mouse[1]//tamCelda
            #letter_location = (box_x * tamCelda, box_y * tamCelda)
            #graph.DrawRectangle((box_x * tamCelda, box_y * tamCelda), (box_x * tamCelda + tamCelda, box_y * tamCelda + tamCelda), line_color='black', fill_color='red')
            #graph.DrawText(miMatriz[box_x][box_y], (box_x*tamCelda + tamCelda/2, box_y*tamCelda + tamCelda/2), color='black', font=('Helvetica',25), angle=0)
            letra = miMatriz[box_x][box_y]
            if comparoPalabra(pala, letra, pos):
                pal = pal + letra
                pos = pos+1
                listaCoordenadas.append((box_x,box_y))
                #print("entra en comparo palabra")
                with open('palabrasClasificadas.txt','r') as file:
                    clasificadas = json.load(file)
                    if pal in pala:
                        #tipo= pal.parse()
                        #print("entra en pal in palabras")
                        for i in listaCoordenadas:
                            if pal in clasificadas['verbos']:
                                graph.DrawRectangle((i[0] * tamCelda, i[1] * tamCelda), (i[0] * tamCelda + tamCelda, i[1] * tamCelda + tamCelda), line_color='black', fill_color=arch['colorv'])
                                graph.DrawText(miMatriz[i[0]][i[1]], (i[0]*tamCelda + tamCelda/2, i[1]*tamCelda + tamCelda/2), color='black', font=('Helvetica', 25), angle=0)
                            if pal in clasificadas['sustantivos']:
                                graph.DrawRectangle((i[0] * tamCelda, i[1] * tamCelda), (i[0] * tamCelda + tamCelda, i[1] * tamCelda + tamCelda), line_color='black', fill_color=arch['colors'])
                                graph.DrawText(miMatriz[i[0]][i[1]], (i[0]*tamCelda + tamCelda/2, i[1]*tamCelda + tamCelda/2), color='black', font=('Helvetica', 25), angle=0)
                            if pal in clasificadas['adjetivos']:
                                graph.DrawRectangle((i[0] * tamCelda, i[1] * tamCelda), (i[0] * tamCelda + tamCelda, i[1] * tamCelda + tamCelda), line_color='black', fill_color=arch['colora'])
                                graph.DrawText(miMatriz[i[0]][i[1]], (i[0]*tamCelda + tamCelda/2, i[1]*tamCelda + tamCelda/2), color='black', font=('Helvetica', 25), angle=0)

                        #print("encontre la palabra" , pal)
                        palabras.remove(pal)
                        pal =""
                        pos = 0
                        listaCoordenadas=[]
            else:
                #print("no entra en comparo palabra")
                #print(letra)
                pal = ""
                pos = 0
                listaCoordenadas=[]
            if len(palabras) == 0:
                sg.Popup("","                             " + "¡¡¡G A N A S T E!!!" + "                             ")


    window.Close()
#mainSopa()

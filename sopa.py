import sys
import PySimpleGUI as sg
import random
import json
import string 
from pattern.web import Wiktionary
from pattern.web import Element
from pattern.web.locale import geocode
from pattern.es import conjugate, verbs
from pattern.es import INFINITIVE, PRESENT, PAST, SG, PL, SUBJUNCTIVE
from pattern.es import parse, split

layoutClasificacion = [
                    [sg.Text("¿Que es la palabra que acabas de encontrar?" ,font=("Roboto",13))],
                    [sg.Radio("Adjetivo","RADIO1",default=False,size=(7,1),font=("Roboto",13),key="adj"),
                    sg.Radio("Sustantivo","RADIO1",default=False,size=(7,1),font=("Roboto",13),key="sus"),
                    sg.Radio("Verbo","RADIO1",default=False,size=(7,1),font=("Roboto",13),key="ver")],
                    [sg.Button("                                      Aceptar                                      ")]
                    ]

def matriz(longitud, cod):
    '''Se ingresan caracteres aleatorios en la matriz'''
    matriz = []
    for row in range(longitud):
        matriz.append([])
        for col in range(longitud):
            matriz[row].append(chr(random.randrange(cod, cod + 26)))
    return matriz

def matrizColores(longitud):
    '''Se crea una matriz con el color del rectangulo en cada posicion'''
    matrizColores = []
    for row in range(longitud):
        matrizColores.append([])
        for col in range(longitud):
            matrizColores[row].append("lightgrey")
    return matrizColores

def temperatura():
    '''Se obtienen los datos del archivo del sensado y se calcula el promedio de temperatura'''
    archivoDatos= open ('archivos/datos-oficinas.json','r')
    datosOficinas = json.load(archivoDatos)
    suma = 0
    cant = 0
    print(datosOficinas)
    for datos in datosOficinas:
        print('datos',datos)
        for dato in datosOficinas[datos]:
            suma = suma + dato['temperatura']
            cant = cant+1
            print('temperatura',dato['temperatura'])
            print('humedad',dato['humedad'])
    promedio = suma/cant
    print(promedio)
    return promedio

def grilla():
    '''Se arma la grilla para ingresar letras y en la sopa de letras'''
    archiPalabras = open('archivos/palabras.txt','r')
    promedio = temperatura()
    if promedio < 10:
        color= 'LightSkyBlue2'
    elif promedio<=20:
        color= 'coral'
    else:
        color= 'orange red'
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
            [sg.Graph((longitud,longitud), (0,longitud), (longitud,0), key='graph', change_submits=True, drag_submits=False, background_color=color)],
            [sg.Text('Ayuda:',font=('Roboto',12)),sg.Listbox('',key='ayuda', size=(20,2),disabled=True)],
            [sg.Cancel('Cerrar')]
            ]

    window = sg.Window('Sopa de letras').Layout(grafico).Finalize()
    graph = window.FindElement('graph')
    return cantCeldas,misPalabras,graph,window,tamCelda,longitud

def ayudaPalabras(palabras,window):
    '''Se activa la ayuda para que se muetren las palabras a buscar'''
    window.Element('ayuda').Update(disabled = False)
    window.Element('ayuda').Update(palabras)

def ayudaClasif(palabras,window,arch):
    print('aca va la ayuda de cuantos adj sus verb')
    window.Element('ayuda').Update(disabled = False)
    bla = ['Cantidad Sustantivos: '+arch['cans'],'Cantidad Adjetivos: '+arch['cana'],'Cantidad Verbos: '+arch['canv']]
    window.Element('ayuda').Update(bla)

def ayudaDefinicion():
    print('aca va la ayuda de la definicion de las palabras')

def horizontal(grilla,palabras,cantCeldas,tamCelda,graph,tipografia):
    '''Se ingresan las palabras en la sopa de letras para que esten en formato horizontal'''
    # Tomo al azar tantas filas como palabras haya
    dicCoordenadas={} # Creo diccionario, para guardar coordenadas de palabras
    random_col = random.sample(range(cantCeldas), len(palabras))
    for idx, palabra in enumerate(palabras):
        dicCoordenadas[palabra]=[] # Le asigno una lista, a la clave palabra
        row = random.randrange(cantCeldas-len(palabra)+1)
        for letra in palabra:
            grilla[row][random_col[idx]] = letra
            dicCoordenadas[palabra].append((row,random_col[idx]))
            row = row+1
    for row in range(cantCeldas):
        for col in range(cantCeldas):
            graph.DrawRectangle((col * tamCelda, row * tamCelda), (col * tamCelda + tamCelda, row * tamCelda + tamCelda), line_color='black')
            graph.DrawText(grilla[col][row], location=(col*tamCelda +tamCelda/2, row*tamCelda + tamCelda/2), color='black', font=(tipografia,25), angle=0)
    return dicCoordenadas

def vertical(grilla,palabras,cantCeldas,tamCelda,graph,tipografia):
    # Tomo al azar tantas columnas como palabras haya
    '''Se ingresan las palabras en la sopa de letras para que esten en formato vertical'''
    random_row = random.sample(range(cantCeldas), len(palabras))
    dicCoordenadas={} # Creo diccionario, para guardar coordenadas de palabras
    for idx, palabra in enumerate(palabras):
        col = random.randrange(cantCeldas-len(palabra)+1)
        dicCoordenadas[palabra]=[] # Le asigno una lista, a la clave palabra
        for letra in palabra:
            grilla[random_row[idx]][col] = letra
            dicCoordenadas[palabra].append((random_row[idx],col))
            col = col+1
    for row in range(cantCeldas):
        for col in range(cantCeldas):
            graph.DrawRectangle((col * tamCelda, row * tamCelda), (col * tamCelda + tamCelda, row * tamCelda + tamCelda), line_color='black')
            graph.DrawText(grilla[col][row], location=(col*tamCelda +tamCelda/2, row*tamCelda + tamCelda/2), color='black', font=(tipografia,25), angle=0)
    return dicCoordenadas

def comparoPalabra(letra, pos, dicCoordenadas,box_x,box_y):
    '''Se comparan las letras que se seleccionan con las que estan en la matriz de la sopa de letras'''
    for clave in dicCoordenadas.keys():
        if len(clave)-1 >= pos:
            if letra == clave[pos] and (box_x,box_y) == dicCoordenadas[clave][pos]:
                return True
    return False

def mainSopa():
    archConfig = open('archivos/configuracion.txt','r')
    archConf = json.load(archConfig)
    cantCeldas,palabras, graph,window, tamCelda, longitud=grilla()
    pala = []
    clasif = open('archivos/palabrasClasificadas.txt','r')
    clasificadas = json.load(clasif)
    miMatrizColores = matrizColores(longitud)
    #se recorre el archivo con la configuracion guardada
    for arch in archConf:

        if arch['mayuscula'] == 'minuscula':
            cod = 97
            miMatriz = matriz(cantCeldas,cod)
            palabras= list(map(lambda x: x.lower(), palabras))
        else:
            cod = 65
            miMatriz = matriz(cantCeldas,cod)
            palabras= list(map(lambda x: x.upper(), palabras))

        if arch['ayuda'] == 'palabras':
            ayudaPalabras(palabras,window)
            print(palabras)
        elif arch['ayuda']=='clasificacion':
            ayudaClasif(palabras,window,arch)
        else:
            ayudaDefinicion()

        if arch['orientacion'] == 'vertical':
            for pal in palabras:
                pala.append(pal)
            dicCoordenadas = vertical(miMatriz,pala,cantCeldas,tamCelda,graph,arch['tipografia'])
        else:
            for pal in palabras:
                pala.append(pal)
            dicCoordenadas = horizontal(miMatriz,pala,cantCeldas,tamCelda,graph,arch['tipografia'])
    pos=0
    palBuscar= ""
    listaCoordenadas=[]
    palCorrectas=0
    palError=0
    
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
            """Aca llamo a la funcion que compra las letras con la de las palabras ingresadas,
            y las pinto una vez seleccionada toda la palabra."""
            letra = miMatriz[box_x][box_y]
            if miMatrizColores[box_x][box_y] == "lightgrey":
                graph.DrawRectangle((box_x * tamCelda, box_y * tamCelda), (box_x * tamCelda + tamCelda, box_y * tamCelda + tamCelda), line_color='black', fill_color="lightblue")
                graph.DrawText(miMatriz[box_x][box_y], (box_x*tamCelda + tamCelda/2, box_y*tamCelda + tamCelda/2), color='black', font=(arch['tipografia'], 25), angle=0)
                miMatrizColores[box_x][box_y] = "lightblue"
            elif miMatrizColores[box_x][box_y] == "lightblue":
                graph.DrawRectangle((box_x * tamCelda, box_y * tamCelda), (box_x * tamCelda + tamCelda, box_y * tamCelda + tamCelda), line_color='black', fill_color="lightgrey")
                graph.DrawText(miMatriz[box_x][box_y], (box_x*tamCelda + tamCelda/2, box_y*tamCelda + tamCelda/2), color='black', font=(arch['tipografia'], 25), angle=0)
                miMatrizColores[box_x][box_y] = "lightgrey"

            
            if comparoPalabra(letra, pos, dicCoordenadas ,box_x,box_y):
                pos = pos+1
                palBuscar = palBuscar + letra
                listaCoordenadas.append((box_x,box_y))
                for clave in dicCoordenadas.keys():
                    if(palBuscar == clave):
                        wiktionary = Wiktionary(language='es')
                        articulo = wiktionary.search(palBuscar.lower())
                        misCLasific=['Sustantivo','Adjetivo','Verbo','Forma Verbal','Sustantivo intransitivo','Sustantivo transitivo','Sustantivo masculino','Verbo intransitivo','Verbo transitivo','Sustantivo femenino']
                        encontre = False
                        for section in articulo.sections:
                            if not encontre:
                                print(section)
                                if section.title in misCLasific[0] or section.title in misCLasific[4] or section.title in misCLasific[5] or section.title in misCLasific[6] or section.title in misCLasific[9]:
                                    palComparar = 'sustantivo'
                                    encontre = True
                                    print('aca1')
                                elif section.title in misCLasific[1]:
                                    palComparar = 'adjetivo'
                                    encontre = True
                                    print('aca2')
                                elif section.title in misCLasific[2] or section.title in misCLasific[3] or section.title in misCLasific[7] or section.title in misCLasific[8]:
                                    print(section.title)
                                    palComparar = 'verbo'
                                    encontre = True
                                    print('aca3')
                                
                        print(parse(palBuscar))
                        palabras.remove(palBuscar)
                        print(palComparar)                        

                        pos = 0
                        palBuscar=""
                        if (pal.upper() in pala) or (pal.lower() in pala):
                            window2 = sg.Window("Clasificacion de palabra").Layout(layoutClasificacion)
                            button, values = window2.Read()
                            color=""
                            if values["adj"]:
                                color = arch["colora"]
                                if palComparar == 'adjetivo':
                                    palCorrectas+=1
                                else:
                                    palError+=1
                            elif values["sus"]:
                                color = arch['colors']
                                if palComparar == 'sustantivo':
                                    palCorrectas+=1
                                else:
                                    palError+=1
                            elif values["ver"]:
                                color = arch['colorv']
                                if palComparar == 'verbo':
                                    palCorrectas+=1
                                else:
                                    palError+=1
                            print('palabra correcta' ,palCorrectas)
                            print('palabra incorrecta' , palError)
                            if button == "Aceptar":
                                    break
                            window2.Close()

                            for i in listaCoordenadas:
                                graph.DrawRectangle((i[0] * tamCelda, i[1] * tamCelda), (i[0] * tamCelda + tamCelda, i[1] * tamCelda + tamCelda), line_color='black', fill_color=color)
                                miMatrizColores[i[0]][i[1]] = color
                                graph.DrawText(miMatriz[i[0]][i[1]], (i[0]*tamCelda + tamCelda/2, i[1]*tamCelda + tamCelda/2), color='black', font=(arch['tipografia'], 25), angle=0)
                            listaCoordenadas=[]
            else:
                pos = 0
                palBuscar= ""
                for i in listaCoordenadas:
                    miMatrizColores[i[0]][i[1]] = "lightgrey"
                listaCoordenadas=[]
            if len(palabras) == 0:
                sg.Popup("","       " + "¡¡¡G A N A S T E!!!" + "                             ",'TUVISTE', palCorrectas, 'PALABRAS CORRECTAS , Y', palError , 'PALABRAS INCORRECTAS',font=('Roboto',15))


    window.Close()
#mainSopa()

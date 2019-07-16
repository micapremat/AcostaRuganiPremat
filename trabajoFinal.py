import PySimpleGUI as sg
from sopa import mainSopa
import json
from pattern.web import Wiktionary
from pattern.web import Element
from pattern.web.locale import geocode
from pattern.es import conjugate, verbs
from pattern.es import INFINITIVE, PRESENT, PAST, SG, PL, SUBJUNCTIVE
from pattern.es import parse, split
import Sonido
import Matriz
import Temperatura

def main(args):
    columna1 = [
        [sg.Listbox(values='',size=(30,5),key='listbox')]
    ]
    columna2 = [
        [sg.Text('Color Sustantivos:', font=('Roboto',13)),sg.InputCombo(('Verde','Azul','Amarillo'),size=(22,1),key='colors')],
        [sg.Text('Color Adjetivos:   ', font=('Roboto',13)),sg.InputCombo(('Azul','Amarillo','Verde'),size=(22,1),key='colora')],
        [sg.Text('Color Verbos:      ', font=('Roboto',13)),sg.InputCombo(('Amarillo','Verde','Azul'),size=(22,1),key='colorv')]
    ]
    layout = [
        [sg.Text('Seleccione un tipo de ayuda: ', font=('Roboto',13))],
        [sg.Radio('Mostrar Palabras','RADIO1',default=False,size=(40,1),font=('Roboto',13),key='ayudaP')],
        [sg.Radio('Mostrar cantidad de Sustantivos/Adjetivos/Verbos','RADIO1',default=True,size=(40,1),font=('Roboto',13),key='ayudaC')],
        [sg.Radio('Mostrar definicion de palabras','RADIO1',default=True,size=(40,1),font=('Roboto',13),key='ayudaD')],
        [sg.Text('Elegir orientacion de palabras:', font=('Roboto',13)),sg.Radio('Horizontal','RADIO2',default=True,size=(10,1),font=('Roboto',13),key='horizontal'),sg.Radio('Vertical','RADIO2',default=True,size=(10,1),font=('Roboto',13),key='vertical')],
        [sg.Text('Elegir Mayuscula/Minuscula:', font=('Roboto',13)),sg.Radio('Mayuscula','RADIO3',default=False,size=(10,1),font=('Roboto',13),key='mayuscula'),sg.Radio('Minuscula','RADIO3',default=True,size=(10,1),font=('Roboto',13),key='minuscula')],
        [sg.Text('Elegir tipografia:', font=('Roboto',13)),sg.InputCombo(('Helvetica','Roboto','Arial', 'Comic Sans', 'Tahoma', 'Calibri'),size=(22,1),key='tipografia')],
        [sg.Text('Cantidad de Sustantivos a mostrar:',font=('Roboto',13)),sg.InputCombo(('0','1','2','3','4','5'), font=('Roboto',13), key= 'cans')],
        [sg.Text('Cantidad de Adjetivos a mostrar:   ',font=('Roboto',13)),sg.InputCombo(('0','1','2','3','4','5'), font=('Roboto',13), key='cana')],
        [sg.Text('Cantidad de Verbos a mostrar:      ',font=('Roboto',13)),sg.InputCombo(('0','1','2','3','4','5'), font=('Roboto',13), key='canv')],
        [sg.Column(columna1),sg.Column(columna2)],
        [sg.Text('Ingrese las palabras a descubrir:',font=('Roboto',13)),sg.InputText(key='palabra')],
        [sg.Text('Ingrese la palabra a eliminar:',font=('Roboto',13)),sg.InputText(key='borrarPal')],
        [sg.Submit('Agregar'),sg.Submit('Eliminar'),sg.Cancel('Salir'),sg.Submit('Guardar')]
    ]
    inicio = [
        [sg.Text('Sopa de letras! ', font=('Roboto',18),justification='center', size=(20,1))],
        [sg.Submit('Iniciar Juego',font=('Roboto',14)),sg.Submit('Configuracion',font=('Roboto',14)),sg.Cancel('Cancelar',font=('Roboto',14))]
    ]

    palabrasClasificadas = {}
    palabrasClasificadas['sustantivos']=[]
    palabrasClasificadas['adjetivos']=[]
    palabrasClasificadas['verbos']=[]
    listaPalabras = []
    listaBox = []
    window = sg.Window('Bienvenidos!!').Layout(inicio)
    button, values = window.Read()
    inicio = True
    config = False
    data = []
    cantVerbos = 0
    cantSust = 0
    cantAdj= 0
    dicClasificacion={}
    
    while inicio:
        if button == 'Iniciar Juego':
            mainSopa()
            break
        if button == 'Cancelar':
            break
        if button == 'Configuracion':
            inicio=False
            config = True
            archivoPalabras = open('archivos/palabras.txt','w')
            archivoClasificadas = open('archivos/palabrasClasificadas.txt','w')
            archReporte = open('archivos/reporte.txt','w')
            window = sg.Window('Configuracion').Layout(layout)
            button, values = window.Read()

            while config:
                if button == 'Agregar':
                    #aca empieza wiktionary
                    wiktionary = Wiktionary(language='es')
                    articulo = wiktionary.search(values['palabra'])
                    try:
                        #print(articulo)
                        sustantivo =''
                        adjetivo = ''
                        verbo = ''
                        encontre = False
                        misCLasific=['Sustantivo','Adjetivo','Verbo','Forma Verbal','Sustantivo intransitivo','Sustantivo transitivo','Sustantivo masculino','Verbo intransitivo','Verbo transitivo','Sustantivo femenino']
                        for section in articulo.sections:
                            if not encontre:
                                titulo=section.title
                                print(section.title)
                                if section.title in misCLasific[0] or section.title in misCLasific[4] or section.title in misCLasific[5] or section.title in misCLasific[6] or section.title in misCLasific[9]:
                                    print('entra1')
                                    sustantivo = 'NN'
                                    dicClasificacion[values['palabra']]='sustantivo'
                                    encontre = True
                                elif section.title in misCLasific[1]:
                                    print('entra2')
                                    adjetivo = 'JJ'
                                    dicClasificacion[values['palabra']]='adjetivo'
                                    encontre = True
                                elif section.title in misCLasific[2] or section.title in misCLasific[3] or section.title in misCLasific[7] or section.title in misCLasific[8]:
                                    print('entra3')
                                    verbo = 'VB'
                                    dicClasificacion[values['palabra']]='verbo'
                                    encontre = True
                            else:
                                break
                        print(dicClasificacion)
                        clasificoPat = parse(values['palabra']).split()
                        if clasificoPat[0][0][1] == verbo:
                            listaBox.append(values['palabra'])
                            if (cantVerbos < int(values['canv'])):
                                palabrasClasificadas['verbos'].append(values['palabra'])
                                listaPalabras.append(values['palabra'])
                                cantVerbos += 1              
                        elif clasificoPat[0][0][1] == sustantivo:
                            listaBox.append(values['palabra'])
                            if (cantSust < int(values['cans'])):
                                palabrasClasificadas['sustantivos'].append(values['palabra'])
                                listaPalabras.append(values['palabra'])
                                cantSust += 1 
                        elif clasificoPat[0][0][1] == adjetivo:
                            listaBox.append(values['palabra'])
                            if (cantAdj < int(values['cana'])):
                                palabrasClasificadas['adjetivos'].append(values['palabra'])
                                listaPalabras.append(values['palabra'])
                                cantAdj += 1 
                        else:
                            archReporte.write('La palabra: '+values['palabra']+' no coincide con pattern\n')
                        #print(clasificoPat)
                        #print(palabrasClasificadas)
                        window.Element('listbox').Update(listaBox)
                    except:
                        archReporte.write('La palabra: '+values['palabra']+' no se encuentra\n')
                    button, values = window.Read()
                if button == 'Eliminar':
                    if values['borrarPal'] in listaPalabras:
                        listaBox.remove(values['borrarPal'])
                        listaPalabras.remove(values['borrarPal'])
                        for valor in palabrasClasificadas.keys():
                            if values['borrarPal'] in palabrasClasificadas[valor]:
                                palabrasClasificadas[valor].remove(values['borrarPal'])
                    window.Element('listbox').Update(listaPalabras)
                    button, values = window.Read()
                if button == 'Salir':
                    break
                if button == 'Guardar':
                    json.dump(palabrasClasificadas,archivoClasificadas,indent=4)
                    for pal in listaPalabras:
                        archivoPalabras.write(pal+'\n')
                    archConfig = open('archivos/configuracion.txt','w')
                    datos={}
                    #elijo si deseo ayuda
                    if values['ayudaP']:
                        datos['ayuda']='palabras'
                    elif values['ayudaC']:
                        datos['ayuda']='clasificacion'
                    else:
                        datos['ayuda']='definicion'
                    
                    #se elige la orientacion de las palabras a buscar
                    if values['horizontal']:
                        datos['orientacion'] = 'horizontal'
                    else:
                        datos['orientacion']='vertical'
                    
                    #se elige las letras en mayusculas o minusculas
                    if values['mayuscula']:
                        datos['mayuscula']='mayuscula'
                    else:
                        datos['mayuscula']='minuscula'

                    #se elige tipografia a utilizar
                    datos['tipografia']= values['tipografia']
                    
                    #se elige color para sustantivos, adjetivos y verbos.                  
                    if (values['colors'] == 'Amarillo'):
                        datos['colors']= 'yellow'
                    elif (values['colors'] == 'Verde'):
                        datos['colors']= 'green'
                    elif (values['colors'] == 'Azul'):
                        datos['colors']= 'blue'
                    
                    if (values['colora'] == 'Verde'):
                        datos['colora']= 'green'
                    elif (values['colora'] == 'Azul'):
                        datos['colora']= 'blue'
                    elif (values['colora'] == 'Amarillo'):
                        datos['colora']= 'yellow'

                    if (values['colorv'] == 'Azul'):
                        datos['colorv']= 'blue'
                    elif (values['colorv'] == 'Amarillo'):
                        datos['colorv']= 'yellow'
                    elif (values['colorv'] == 'Verde'):
                        datos['colorv']= 'green'

                    #Se elige cuantos sustantivos, adjetivos y verbos
                    datos['cans'] = values['cans']
                    datos['cana'] = values['cana'] 
                    datos['canv'] = values['canv']


                    data.append(datos)
                    json.dump(data,archConfig,indent=4)
                    archConfig.close()
                    config = False
                    archivoPalabras.close()
        button, values = window.Read()
    window.Close()
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

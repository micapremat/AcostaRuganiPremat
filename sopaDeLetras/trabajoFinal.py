import PySimpleGUI as sg
from sopa import mainSopa
import json
from pattern.web import Wiktionary
from pattern.web import Element
from pattern.web.locale import geocode
from pattern.es import conjugate, verbs
from pattern.es import INFINITIVE, PRESENT, PAST, SG, PL, SUBJUNCTIVE
from pattern.es import parse, split

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
        [sg.Text('Desea activar la ayuda: ', font=('Roboto',13)),sg.Radio('SI','RADIO1',default=False,size=(10,1),font=('Roboto',13),key='ayuda'),sg.Radio('NO','RADIO1',default=True,size=(10,1),font=('Roboto',13),key='ayudano')],
        [sg.Text('Elegir orientacion de palabras:', font=('Roboto',13)),sg.Radio('Horizontal','RADIO2',default=True,size=(10,1),font=('Roboto',13),key='horizontal'),sg.Radio('Vertical','RADIO2',default=True,size=(10,1),font=('Roboto',13),key='vertical')],
        [sg.Text('Elegir Mayuscula/Minuscula:', font=('Roboto',13)),sg.Radio('Mayuscula','RADIO3',default=False,size=(10,1),font=('Roboto',13),key='mayuscula'),sg.Radio('Minuscula','RADIO3',default=True,size=(10,1),font=('Roboto',13),key='minuscula')],
        [sg.Text('Elegir tipografia:', font=('Roboto',13)),sg.InputCombo(('Helvetica','Roboto','Arial'),size=(22,1),key='tipografia')],
        [sg.Text('Cantidad de Sustantivos a mostrar:',font=('Roboto',13)),sg.InputCombo(('0','1','2','3','4','5'), font=('Roboto',13))],
        [sg.Text('Cantidad de Adjetivos a mostrar:   ',font=('Roboto',13)),sg.InputCombo(('0','1','2','3','4','5'), font=('Roboto',13))],
        [sg.Text('Cantidad de Verbos a mostrar:      ',font=('Roboto',13)),sg.InputCombo(('0','1','2','3','4','5'), font=('Roboto',13))],
        [sg.Column(columna1),sg.Column(columna2)],
        [sg.Text('Ingrese las palabras a descubrir:',font=('Roboto',13)),sg.InputText(key='palabra')],
        [sg.Submit('Agregar'),sg.Submit('Eliminar'),sg.Cancel('Cancelar'),sg.Submit('Guardar')]
    ]
    inicio = [
        [sg.Text('Sopa de letras! ', font=('Roboto',18),justification='center', size=(20,1))],
        [sg.Submit('Iniciar Juego',font=('Roboto',14)),sg.Submit('Configuracion',font=('Roboto',14)),sg.Cancel('Salir',font=('Roboto',14))]
    ]

    palabrasClasificadas = {}
    palabrasClasificadas['sustantivos']=[]
    palabrasClasificadas['adjetivos']=[]
    palabrasClasificadas['verbos']=[]
    listaPalabras = []
    window = sg.Window('Bienvenidos!!').Layout(inicio)
    button, values = window.Read()
    inicio = True
    config = False
    data = []
    while inicio:

        if button == 'Iniciar Juego':
            mainSopa()
            break
        if button == 'Salir':
            break
        if button == 'Configuracion':
            inicio=False
            config = True
            archivoPalabras = open('palabras.txt','w')
            archivoClasificadas = open('palabrasClasificadas.txt','w')
            archReporte = open('reporte.txt','w')
            window = sg.Window('Configuracion').Layout(layout)
            button, values = window.Read()

            while config:
                if button == 'Agregar':
                    #aca empieza wiktionary
                    wiktionary = Wiktionary(language='es')
                    articulo = wiktionary.search(values['palabra'])
                    try:
                        print(articulo)
                        sustantivo =''
                        adjetivo = ''
                        verbo = ''
                        for section in articulo.sections:
                            #print(' ' * section.level + section.title)
                            if 'Sustantivo' in section.title:
                                sustantivo = 'NN'
                            if 'Adjetivo' in section.title:
                                adjetivo = 'JJ'
                            if 'Verbo' or 'Verbal' in section.title:
                                verbo = 'VB'
                        print('sustantivo',sustantivo,'adjetivo',adjetivo,'verbo',verbo)
                        clasifico = parse(values['palabra']).split()
                        if clasifico[0][0][1] == verbo:
                            print(clasifico[0][0][1],verbo)
                            palabrasClasificadas['verbos'].append(values['palabra'])
                            listaPalabras.append(values['palabra'])                   
                        if clasifico[0][0][1] == sustantivo:
                            palabrasClasificadas['sustantivos'].append(values['palabra'])
                            listaPalabras.append(values['palabra'])
                        if clasifico[0][0][1] == adjetivo:
                            palabrasClasificadas['adjetivos'].append(values['palabra'])
                            listaPalabras.append(values['palabra'])
                        else:
                            archReporte.write('La palabra: '+values['palabra']+' no coincide con pattern\n')
                        print(clasifico)
                        print(palabrasClasificadas)
                        window.Element('listbox').Update(listaPalabras)
                    except:
                        archReporte.write('La palabra: '+values['palabra']+' no se encuentra\n')
                    button, values = window.Read()
                if button == 'Eliminar':
                    listaPalabras.pop()
                    window.Element('listbox').Update(listaPalabras)
                    button, values = window.Read()
                if button == 'Cancelar':
                    break
                if button == 'Guardar':

                    json.dump(palabrasClasificadas,archivoClasificadas,indent=4)
                    for pal in listaPalabras:
                        archivoPalabras.write(pal+'\n')
                    archConfig = open('configuracion.txt','w')
                    datos={}
                    if values['ayuda']:
                        datos['ayuda']='si'
                    else:
                        datos['ayuda']='no'
                    if values['horizontal']:
                        datos['orientacion'] = 'horizontal'
                    else:
                        datos['orientacion']='vertical'
                    if values['mayuscula']:
                        datos['mayuscula']='mayuscula'
                    else:
                        datos['mayuscula']='minuscula'
                    datos['tipografia']= values['tipografia']
                    if (values['colors'] == "Amarillo"):
                        datos['colors']= "yellow"
                    elif (values['colors'] == "Verde"):
                        datos['colors']= "green"
                    elif (values['colors'] == "Azul"):
                        datos['colors']= "blue"
                    
                    if (values['colora'] == "Amarillo"):
                        datos['colora']= "yellow"
                    elif (values['colora'] == "Verde"):
                        datos['colora']= "green"
                    elif (values['colora'] == "Azul"):
                        datos['colora']= "blue"

                    if (values['colorv'] == "Amarillo"):
                        datos['colorv']= "yellow"
                    elif (values['colorv'] == "Verde"):
                        datos['colorv']= "green"
                    elif (values['colorv'] == "Azul"):
                        datos['colorv']= "blue"
    
                    print(values['horizontal'])
                    print('guardar')
                    data.append(datos)
                    json.dump(data,archConfig,indent=4)
                    archConfig.close()
                    config = False
                    print('guardar')
                    archivoPalabras.close()
        button, values = window.Read()
    window.Close()
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

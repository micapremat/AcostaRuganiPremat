from Sonido import Sonido
from Matriz import Matriz
from Temperatura import Temperatura
import time
from datetime import datetime as dt


if __name__ == '__main__':
    sonido = Sonido()
    matriz = Matriz()
    temp = Temperatura()
    t1 = dt.now()
    dic = {'oficina1':[]}
    while True:
        if ((dt.now() - t1).total_seconds() >= 60):
            t1 = dt.now()
            registro = temp.datos_sensor()
            archivoRegistro = open ('archivos/datos-oficinas.json','a')
            dic['oficina1'].append(registro)
            json.dump(dic,archivoRegistro,indent=4)
            archivoRegistro.close()
        if sonido.evento_detectado():
            mensaje = 'Temperatura: {0}, Humedad: {1}'.format(registro['temperatura'],registro['humedad'])
            matriz.mostrar_mensaje(mensaje)
        

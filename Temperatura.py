import Adafruit_DHT
class Temperatura:
    def __init__(self, pin=17, sensor=Adafruit_DHT.DHT11):
        # Usamos el DHT11 que es compatible con el DHT12
        self._sensor = sensor
        self._data_pin = pin
    def datos_sensor(self):
        humedad, temperatura = Adafruit_DHT.read_retry(self.
        _sensor, self._data_pin)
        return {'temperatura': temperatura, 'humedad': humedad}
temp = Temperatura()
datos = temp.datos_sensor()
print('Temperatura = {0:0.1f°}C Humedad = {1:0.1f} %'.format(datos['temperatura'], datos['humedad']))

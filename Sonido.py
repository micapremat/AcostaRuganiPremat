import RPi.GPIO as GPIO
class Sonido:
    def __init__(self, canal=22):
        self._canal = canal
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._canal, GPIO.IN)
        # Desactivo las warnings por tener más de un circuito en la GPIO
        GPIO.setwarnings(False)
        GPIO.add_event_detect(self._canal, GPIO.RISING)
    def evento_detectado(self, funcion):
        if GPIO.event_detected(self._canal):
            funcion()

def test():
    print('Sonido detectado!')
sonido = Sonido()
while True:
    time.sleep(0.0001)
    sonido.evento_detectado(test)
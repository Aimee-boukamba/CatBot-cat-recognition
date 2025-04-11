import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# Configuration GPIO
MOTEUR_PIN = 17  # Changer selon votre branchement
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTEUR_PIN, GPIO.OUT)
GPIO.output(MOTEUR_PIN, GPIO.LOW)

# Configuration MQTT
broker_address = "localhost"  # Si mosquitto est installé sur le Pi
topic = "jetson/chat/detecte"

def on_message(client, userdata, message):
    msg = message.payload.decode()
    print("Message reçu: " + msg)
    
    if msg == "ACTIVER_MOTEUR":
        GPIO.output(MOTEUR_PIN, GPIO.HIGH)
        print("Moteur activé")
    elif msg == "DESACTIVER_MOTEUR":
        GPIO.output(MOTEUR_PIN, GPIO.LOW)
        print("Moteur désactivé")

client = mqtt.Client("RaspberryMotorControl")
client.on_message = on_message
client.connect(broker_address)
client.subscribe(topic)
print("En attente de détection de chat...")
client.loop_forever()
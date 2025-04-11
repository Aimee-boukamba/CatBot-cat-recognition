import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time

# Configuration MQTT
broker_address = "IP_DU_RASPBERRY"  # Remplacer par l'IP du Raspberry
topic = "jetson/chat/detecte"
client = mqtt.Client("JetsonCatDetector")
client.connect(broker_address)

# Charger le modèle YOLO
net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")  # Adapter pour votre version de YOLO
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Capture vidéo
cap = cv2.VideoCapture(0)  # Utiliser 0 pour la caméra par défaut

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, channels = frame.shape

    # Détection d'objets
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Analyse des détections
    cat_detected = False
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] == "cat":
                cat_detected = True
                break

    # Envoyer la commande MQTT si chat détecté
    if cat_detected:
        client.publish(topic, "ACTIVER_MOTEUR")
        print("Chat détecté - Signal envoyé au Raspberry Pi")
    else:
        client.publish(topic, "DESACTIVER_MOTEUR")

    time.sleep(0.1)  # Réduire la charge CPU

cap.release()
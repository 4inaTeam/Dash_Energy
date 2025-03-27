import base64
from io import BytesIO
import tensorflow as tf
import numpy as np
from PIL import Image

# Charger le modèle TFLite
interpreter = tf.lite.Interpreter(model_path="models/model_unquant.tflite")
interpreter.allocate_tensors()
# Définir les classes de sortie
classes = ['Gall Midge', 'Healthy', 'Sooty Mould']  # Remplacez cela par vos classes réelles
# Fonction pour effectuer la classification d'image

# Fonction pour effectuer la classification d'image
def classify_image_web(image_data):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Décoder les données d'image base64
    image_bytes = base64.b64decode(image_data)

    # Utiliser BytesIO pour ouvrir l'image avec PIL
    image = Image.open(BytesIO(image_bytes)).convert('RGB')

    # Enregistrer l'image temporairement (vous pouvez la stocker autrement si nécessaire)
    image_path = "temp_image.jpg"
    image.save(image_path)

    # Charger et prétraiter l'image
    image = image.resize((224, 224))
    image = np.array(image).astype(np.float32) / 255.0  # Convertir en FLOAT32
    image = np.expand_dims(image, axis=0)

    # Effectuer la prédiction avec le modèle TFLite
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Renvoyer les résultats de la classification
    predicted_class_index = np.argmax(output_data)
    confidence = output_data[0][predicted_class_index]
    return classes[predicted_class_index], float(confidence)

def classify_image_mobile(image_path):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Charger et prétraiter l'image
    image = Image.open(image_path).resize((224, 224))
    image = np.array(image).astype(np.float32) / 255.0  # Convertir en FLOAT32
    image = np.expand_dims(image, axis=0)

    # Effectuer la prédiction avec le modèle TFLite
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Renvoyer les résultats de la classification
    predicted_class_index = np.argmax(output_data)
    confidence = output_data[0][predicted_class_index]
    return classes[predicted_class_index], float(confidence)
 

import numpy as np
from tensorflow.keras.models import load_model
import pandas as pd
import base64
from PIL import Image
import io
import os


def transform_image_png_to_pixels(image_jpg):
    image = Image.open(image_jpg)
    image = image.resize((28, 28))
    image = image.convert('L')
    image_np = np.array(image)
    image_np = image_np.astype('float32') / 255.0
    image_np = image_np.reshape(1, 28, 28, 1)
    # print(image_np)
    return image_np


# Charger le modèle sauvegardé
model = load_model('IA\models\cnn_model.h5')

# test_path = "./data/test.csv"
# data= pd.read_csv(test_path)
# data_done = data.values.reshape(-1, 28, 28, 1) / 255.0

test_path = "./data/testSet/testSet"  # Liste tous les fichiers JPG du dossier
fichiers_jpg = [f for f in os.listdir(test_path) if f.lower().endswith('.jpg')]

# Affiche la liste des fichiers JPG
for fichier in fichiers_jpg:
    print(fichier)
    data_done = transform_image_png_to_pixels(
        f'./data/testSet/testSet/{fichier}')

    # Supposons que `data` soit votre image ou un batch d'images prétraitées
    predictions = model.predict(data_done)
    print(predictions)

    # Si vous avez une classification, pour obtenir les classes directement:
    predicted_classes = np.argmax(predictions, axis=1)
    print(predicted_classes,'\n')

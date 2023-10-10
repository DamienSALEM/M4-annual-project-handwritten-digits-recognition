import numpy as np
import pandas as pd

def load_mnist_data():
    # Chargement des données depuis train.csv
    df = pd.read_csv("data/train.csv")
    
    # La première colonne est l'étiquette (label)
    y_train = df['label'].values
    
    # Les autres colonnes sont les pixels de l'image
    x_train = df.drop(columns=['label']).values.reshape(-1, 28, 28, 1)

    # Normaliser les images pour avoir des valeurs entre 0 et 1
    x_train = x_train.astype('float32') / 255.0
    
    # Pour cette démo, nous divisons simplement les données d'entraînement pour avoir un set de test.
    # Dans un scénario réel, vous devriez utiliser les données de `test.csv` ou diviser `train.csv` en ensembles d'entraînement et de validation.
    split_size = int(0.9 * len(x_train))
    x_test = x_train[split_size:]
    y_test = y_train[split_size:]
    x_train = x_train[:split_size]
    y_train = y_train[:split_size]

    return x_train, y_train, x_test, y_test

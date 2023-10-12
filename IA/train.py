import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
import joblib

DATA_PATH = "./train.csv"
MODEL_RF_PATH = "./models/random_forest_model.pkl"
MODEL_CNN_PATH = "models/cnn_model.h5"


def load_mnist_data():
    train_data = pd.read_csv(DATA_PATH)
    y_train = train_data["label"].values
    # Exctraction images, changement en 28x28 et normaliser les valeurs (0 < valeur < 1)
    x_train = train_data.drop(
        columns=["label"]).values.reshape(-1, 28, 28, 1) / 255.0
    x_train, x_val, y_train, y_val = train_test_split(
        x_train, y_train, test_size=0.2, random_state=42)
    return x_train, y_train, x_val, y_val

# Création + entrainement + sauvegarde modèle CNN


def train_and_save_cnn(x_train, y_train, x_val, y_val):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(28, 28, 1)),  # Entrée images 28x28
        # Couche convolutive (32 filtres)
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        # Couche réduction taille image + réduction surapprentissage (pooling)
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Flatten(),  # transformer matrice en ligne (on aplatit l'image)
        # Couche dense avec 128 neurones qui a la fonction d'activation relu (f(x)=max(0,x)
        tf.keras.layers.Dense(128, activation='relu'),
        # ce qui veut dire que si un neuronne a une sortie négative alors 0 sinon il ne change pas --> se base sur les couches précédentes)

        tf.keras.layers.Dense(10, activation='softmax')
        # Couche dense avec 10 neurones (==> pour chaque chiffre de 0 à 9). 1 neuronne = un chiffre ==> produit un score de probabilité.

        # La fonction d'activation softmax est généralement utilisée dans la couche de sortie des problèmes de classification multiclasse.
        # Elle transforme les scores de sortie de chaque neurone (qui peuvent être n'importe quel nombre réel) en probabilités, de sorte que la somme des probabilités de tous
        # les neurones de la couche soit égale à 1.
        # Pour comprendre comment cela fonctionne, supposons que la sortie des 10 neurones (avant activation) soit un vecteur z.
        # La fonction softmax calculera la probabilité pour chaque neurone i comme étant e^Zi divisé par la somme de e^Zj pour tous les j de 0 à 9.
        # Ce processus garantit que chaque élément est entre 0 et 1 et que la somme de tous les éléments est 1.
        # Grâce à cette transformation, il est facile d'interpréter la sortie comme une distribution de probabilités sur les 10 classes.
    ])

    # Compilation du modèle avec l'optimiseur Adam ==> ajuste son taux d'apprentissage en cours de route
    # La fonction de perte est utilisée pour mesurer à quel point les prédictions du modèle sont éloignées des valeurs réelles pendant l'entraînement
    # "sparse" est une variante spéciale qui est utile lorsque vos étiquettes sont des entiers
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=12, batch_size=1024,
              validation_data=(x_val, y_val))
    model.save(MODEL_CNN_PATH)
    print(f"CNN Model saved to {MODEL_CNN_PATH}")


def train_and_save_rf(x_train, y_train, x_val, y_val):
    param_distributions_rf = {
        'n_estimators': [50, 100, 150, 200],
        'max_depth': [10, 20, 30, None],
        'max_features': ['sqrt', 'log2', 0.5, 0.7],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'bootstrap': [True, False]
    }

    # Initialisation du modèle Random Forest
    rf = RandomForestClassifier()
    # Utilisation de RandomizedSearchCV pour trouver les meilleurs hyperparamètres
    random_search_rf = RandomizedSearchCV(
        estimator=rf, param_distributions=param_distributions_rf, n_iter=10, cv=3, verbose=2)
    # Aplatir les images en vecteurs pour l'entraînement RF
    random_search_rf.fit(x_train.reshape(-1, 28*28), y_train)
    # Sauvegarde du meilleur modèle Random Forest trouvé
    joblib.dump(random_search_rf.best_estimator_, MODEL_RF_PATH)
    # Confirmation que le modèle a été enregistré
    print(f"RandomForest Model saved to {MODEL_RF_PATH}")


if __name__ == "__main__":
    x_train, y_train, x_val, y_val = load_mnist_data()

    train_and_save_cnn(x_train, y_train, x_val, y_val)
    # train_and_save_rf(x_train, y_train, x_val, y_val)

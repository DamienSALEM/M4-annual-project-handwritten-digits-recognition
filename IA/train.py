import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
import os
import joblib

# Chemins
DATA_PATH = "./data/train.csv"
MODEL_RF_PATH = "./models/random_forest_model.pkl"
MODEL_CNN_PATH = "./models/cnn_model.h5"

def load_mnist_data():
    train_data = pd.read_csv(DATA_PATH)
    y_train = train_data["label"].values
    x_train = train_data.drop(columns=["label"]).values.reshape(-1, 28, 28, 1) / 255.0
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, random_state=42)
    return x_train, y_train, x_val, y_val

def train_and_save_cnn(x_train, y_train, x_val, y_val):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(28, 28, 1)),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=5, batch_size=32, validation_data=(x_val, y_val))
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

    rf = RandomForestClassifier()
    random_search_rf = RandomizedSearchCV(estimator=rf, param_distributions=param_distributions_rf, n_iter=10, cv=3, verbose=2)
    random_search_rf.fit(x_train.reshape(-1, 28*28), y_train)

    # Sauvegarde du modèle RF optimisé
    joblib.dump(random_search_rf.best_estimator_, MODEL_RF_PATH)
    print(f"RandomForest Model saved to {MODEL_RF_PATH}")

if __name__ == "__main__":
    x_train, y_train, x_val, y_val = load_mnist_data()
    
    train_and_save_cnn(x_train, y_train, x_val, y_val)
    train_and_save_rf(x_train, y_train, x_val, y_val)

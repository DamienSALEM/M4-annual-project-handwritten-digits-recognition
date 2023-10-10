import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import RandomizedSearchCV
from data_utils import load_mnist_data

# Charger les données
x_train, y_train, x_test, y_test = load_mnist_data()

# Modèle CNN (réduction du nombre d'époques)
model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(28, 28, 1)),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=3, batch_size=32, validation_data=(x_test, y_test))  # Reduced epochs
model.save("models/mnist_cnn.h5")

# Entraînement RandomForest
clf_rf = RandomForestClassifier()
clf_rf.fit(x_train.reshape(-1, 28*28), y_train)
y_pred_rf = clf_rf.predict(x_test.reshape(-1, 28*28))
print("RandomForest Results:")
print(confusion_matrix(y_test, y_pred_rf))
print(classification_report(y_test, y_pred_rf))

# Entraînement SVM (cette étape peut être longue en fonction de la taille du jeu de données)
clf_svm = SVC()
clf_svm.fit(x_train.reshape(-1, 28*28), y_train)
y_pred_svm = clf_svm.predict(x_test.reshape(-1, 28*28))
print("SVM Results:")
print(confusion_matrix(y_test, y_pred_svm))
print(classification_report(y_test, y_pred_svm))

# Optimisation avec RandomizedSearch pour RandomForest
param_distributions_rf = {
    'n_estimators': [50, 100, 150, 200],
    'max_depth': [10, 20, 30, None],
    'max_features': ['sqrt', 'log2', 0.5, 0.7],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}

random_search_rf = RandomizedSearchCV(
    RandomForestClassifier(), 
    param_distributions=param_distributions_rf, 
    n_iter=30, 
    cv=3, 
    n_jobs=-1, 
    verbose=2
)

random_search_rf.fit(x_train.reshape(-1, 28*28), y_train)
y_pred_random_rf = random_search_rf.predict(x_test.reshape(-1, 28*28))
print("Optimized RandomForest Results:")
print(confusion_matrix(y_test, y_pred_random_rf))
print(classification_report(y_test, y_pred_random_rf))
print("Meilleurs paramètres pour RandomForest:", random_search_rf.best_params_)

# Vous pouvez ajouter l'optimisation avec RandomizedSearch pour SVM ici si nécessaire.

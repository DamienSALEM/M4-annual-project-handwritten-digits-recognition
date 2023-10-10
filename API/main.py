from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf

app = Flask(__name__)
model = tf.keras.models.load_model("../IA/models/mnist_model.h5")

@app.route("/predict", methods=["POST"])
def predict():
    # Convertir image reçue en array numpy
    return jsonify({"prediction": "votre_prediction_here"})

if __name__ == "__main__":
    app.run(debug=True)

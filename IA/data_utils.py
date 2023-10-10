import pandas as pd
from sklearn.model_selection import train_test_split

def load_mnist_data(train_path):
    train_data = pd.read_csv(train_path)
    y_train = train_data["label"].values
    x_train = train_data.drop(columns=["label"]).values.reshape(-1, 28, 28, 1) / 255.0
    
    # Diviser les données pour créer un ensemble de test.
    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=42)
    
    return x_train, y_train, x_test, y_test

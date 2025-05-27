# File: ai-component/src/model_training.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib
import os

def load_data(file_path):
    """Load processed data from a specified file path."""
    return pd.read_csv(file_path)

def train_model(X, y):
    """Train a K-Nearest Neighbors model on the provided features and labels."""
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X, y)
    return model

def save_model(model, model_path):
    """Save the trained model to the specified path."""
    joblib.dump(model, model_path)

def main():
    # Load processed data
    data = load_data(os.path.join('data', 'processed', 'processed_data.csv'))
    
    # Select features and target variable
    X = data[['materia', 'tema', 'contenido']]
    y = data['actividad_contenido']
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the KNN model
    model = train_model(X_train, y_train)
    
    # Ensure the models directory exists
    os.makedirs(os.path.join('data', 'models'), exist_ok=True)
    
    # Save the trained model
    save_model(model, os.path.join('data', 'models', 'knn_model.pkl'))

if __name__ == "__main__":
    main()
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib
from src.db_connection import app
from database.Materias.Contenido import Contenido
from database.Materias.Materia import Materia
from database.Materias.Tema import Tema
from database.Materias.UsuarioMateria import UsuarioMateria
from database.Usuarios.Usuario import Usuario
import sys

def extract_data():
    data_to_learn = (
        Usuario.query
        .join(Usuario.usuario_materia)
        .join(UsuarioMateria.materias)
        .join(Materia.temas)
        .join(Tema.contenidos)
        .with_entities(
            Materia.nombre.label('materia'),
            Tema.nombre.label('tema'),
            Contenido.titulo.label('contenido'),
            Contenido.nivel_grado,
        )
        .order_by(Contenido.nivel_grado)
    )
    print(data_to_learn.statement)
    data_to_learn = data_to_learn.all()
    return pd.DataFrame(data_to_learn)

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data.drop_duplicates()
    # Fill NA/NaN values using the specified method.
    data = data.fillna(method='ffill')
    return data

def normalize_text(text: str) -> str:
    text = text.lower()
    # Remove punctuation and special characters
    text = ''.join(char for char in text if char.isalnum() or char.isspace())
    return text

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_data(df)
    df['materia'] = df['materia'].apply(normalize_text)
    df['tema'] = df['tema'].apply(normalize_text)
    df['contenido'] = df['contenido'].apply(normalize_text)

    df['materia'] = df['materia'].astype('category').cat.codes
    df['tema'] = df['tema'].astype('category').cat.codes
    df['contenido'] = df['contenido'].astype('category').cat.codes
    df['nivel_grado'] = df['nivel_grado'].astype(int)
    return df

def train_and_save_model(df: pd.DataFrame, model_path: str):
    # Define X (features) and y (target)
    X = df[['materia', 'tema', 'contenido']]
    Y = df['nivel_grado']

    # Divide in train/test
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    n_neighbors = min(5, len(x_train))
    if n_neighbors < 5:
        raise ValueError("No hay suficientes datos para entrenar el modelo KNN.")

    # Train KNN model
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    model.fit(x_train, y_train)

    # Save model
    joblib.dump(model, model_path)
    print(f"Modelo guardado en {model_path}")

    return model, x_test, y_test

def main(filename: str):
    with app.app_context():
        df = extract_data()
        df_processed = preprocess_data(df)

        # Save locally processed data
        processed_path = os.path.join('static', 'data_ai', 'processed', filename)
        os.makedirs(os.path.dirname(processed_path), exist_ok=True)
        df_processed.to_csv(processed_path, index=False)
        print("Datos procesados y guardados.")

        # Train and save the KNN model
        model_path = os.path.join('static', 'data_ai', 'models', 'knn_model.pkl')
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        model, x_test, y_test = train_and_save_model(df_processed, model_path)

        # Evaluate the model
        try:
            from ai_component.src.model_evaluation import evaluate_model
            metrics = evaluate_model(model, x_test, y_test)
            print("Métricas de evaluación:", metrics)
        except ImportError:
            print("No se pudo importar evaluate_model para evaluación.")

if __name__ == "__main__":
    if (
        len(sys.argv) > 1 and sys.argv[1] == 'corrections_ia'
        and os.path.exists(os.path.join('static', 'data_ai', 'processed', 'corrections_ia.csv'))
    ):
        main('corrections_ia.csv')
    else:
        main('processed_data.csv')
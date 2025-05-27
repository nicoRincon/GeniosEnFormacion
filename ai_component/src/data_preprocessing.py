import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib
from src.db_connection import app
from database.Materias.Actividad import Actividad
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
        .join(Contenido.actividades)
        .with_entities(
            Usuario.id.label('user_id'),
            Usuario.nombre_usuario,
            Materia.id.label('materia_id'),
            Materia.nombre.label('materia'),
            Tema.id.label('tema_id'),
            Tema.nombre.label('tema'),
            Contenido.id.label('contenido_id'),
            Contenido.titulo.label('contenido'),
            Actividad.id.label('actividad_id'),
            Actividad.contenido.label('actividad_contenido')
        )
        .all()
    )
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
    cleaned_data = clean_data(df)
    cleaned_data['actividad_contenido'] = cleaned_data['actividad_contenido'].apply(normalize_text)

    df['materia'] = df['materia'].astype('category').cat.codes
    df['tema'] = df['tema'].astype('category').cat.codes
    df['contenido'] = df['contenido'].astype('category').cat.codes
    df['actividad_contenido'] = df['actividad_contenido'].astype('category').cat.codes
    return df

def train_and_save_model(df: pd.DataFrame, model_path: str):
    # Define X (features) and y (target)
    X = df[['materia', 'tema', 'contenido', 'contenido_id']]
    y = df['actividad_contenido']

    # Divide en train/test
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    n_neighbors = len(x_train)
    if n_neighbors < 1:
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
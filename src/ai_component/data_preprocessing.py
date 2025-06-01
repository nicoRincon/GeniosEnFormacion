import random
import pandas as pd
import os
import joblib
import json
from flask import session
from sklearn.neighbors import KNeighborsClassifier
from database.Materias.NotaContenido import NotaContenido
from src.db_connection import app
from src.ai_component.model_evaluation import evaluate_model
from database.Materias.Contenido import Contenido
from database.Materias.Materia import Materia
from database.Materias.Tema import Tema
from database.Materias.UsuarioMateria import UsuarioMateria
from database.Usuarios.Usuario import Usuario


class AiComponent:
    mappings = {}

    def __init__(self, filename: str = 'processed_data.csv'):
        self.filename = filename

    def extract_data(self):
        session['user_id'] = session.get('user_id', 1)
        data_to_learn = (
            Usuario.query
            .join(Usuario.usuario_materia)
            .join(UsuarioMateria.materias)
            .join(Materia.temas)
            .join(Tema.contenidos)
            .join(
                NotaContenido,
                NotaContenido.id_usuario == Usuario.id &
                NotaContenido.id_contenido == Contenido.id &
                NotaContenido.id_usuario == session['user_id'],
                isouter=True
            )
            .filter(
                Usuario.id == session['user_id']
            )
            .with_entities(
                Materia.nombre.label('materia'),
                Tema.nombre.label('tema'),
                Contenido.titulo.label('contenido'),
                NotaContenido.id_usuario,
                Contenido.nivel_grado,
                NotaContenido.nota_obtenida
            )
            .order_by(Contenido.nivel_grado)
        )
        print(data_to_learn.statement)
        data_to_learn = data_to_learn.all()
        data_list = []
        for row in data_to_learn:
            row_dict = row._asdict()
            if row_dict['nota_obtenida'] is None:
                # Esto será lo que queremos predecir
                row_dict['nota_obtenida'] = None
                row_dict['aprobado'] = None
            else:
                row_dict['aprobado'] = (row_dict['nota_obtenida'] >= 3.5)
            data_list.append(row_dict)

        data_frame = pd.DataFrame(data_list)
        return data_frame

    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data.drop_duplicates()
        # Fill NA/NaN values using the specified method.
        data = data.ffill()
        return data

    def normalize_text(self, text: str) -> str:
        text = text.lower()
        # Remove punctuation and special characters
        text = ''.join(char for char in text if char.isalnum() or char.isspace())
        return text

    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.clean_data(df)
        df['materia'] = df['materia'].apply(self.normalize_text)
        df['tema'] = df['tema'].apply(self.normalize_text)
        df['contenido'] = df['contenido'].apply(self.normalize_text)

        materia_cat = df['materia'].astype('category')
        tema_cat = df['tema'].astype('category')
        contenido_cat = df['contenido'].astype('category')

        self.mappings = {
            'materia': dict(enumerate(materia_cat.cat.categories)),
            'tema': dict(enumerate(tema_cat.cat.categories)),
            'contenido': dict(enumerate(contenido_cat.cat.categories))
        }

        df['materia'] = materia_cat.cat.codes
        df['tema'] = tema_cat.cat.codes
        df['contenido'] = contenido_cat.cat.codes
        df['nivel_grado'] = df['nivel_grado'].astype(int)

        mappings_path = os.path.join('static', 'data_ai', 'mappings', 'category_mappings.json')
        os.makedirs(os.path.dirname(mappings_path), exist_ok=True)
        with open(mappings_path, 'w', encoding='utf-8') as f:
            json.dump(self.mappings, f, ensure_ascii=False, indent=2)

        return df

    def train_and_save_model(self, df: pd.DataFrame, model_path: str):
        # Separación datos con notas (para entrenar) y sin notas (para predecir)
        df_with_notes = df[df['nota_obtenida'].notna()].copy()
        df_to_predict = df[df['nota_obtenida'].isna()].copy()

        if len(df_with_notes) < 5:
            print("Muy pocos datos para entrenar. Generando datos sintéticos...")
            # Genera algunos datos sintéticos para poder entrenar
            for _, row in df_to_predict.iterrows():
                synthetic_note = round(random.uniform(1.0, 5.0), 1)
                synthetic_row = row.copy()
                synthetic_row['nota_obtenida'] = synthetic_note
                synthetic_row['aprobado'] = (synthetic_note >= 3.5)
                df_with_notes = pd.concat([df_with_notes, synthetic_row.to_frame().T], ignore_index=True)

        # Entrena solo con datos que tienen notas
        X = df_with_notes[['materia', 'tema', 'contenido', 'nivel_grado']]
        Y = df_with_notes['aprobado'].astype(int)

        # Train model
        n_neighbors = min(3, len(X))
        model = KNeighborsClassifier(n_neighbors=n_neighbors)
        model.fit(X, Y)

        # Save model
        joblib.dump(model, model_path)
        print(f"Modelo guardado en {model_path}")

        return model, X, Y

    def main(self):
        with app.app_context():
            df = self.extract_data()
            df_processed = self.preprocess_data(df)

            # Save locally processed data
            processed_path = os.path.join('static', 'data_ai', 'processed', self.filename)
            os.makedirs(os.path.dirname(processed_path), exist_ok=True)
            df_processed.to_csv(processed_path, index=False)
            print("Datos procesados y guardados.")

            # Train and save the KNN model
            model_path = os.path.join('static', 'data_ai', 'models', 'knn_model.pkl')
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            model, x_test, y_test = self.train_and_save_model(df_processed, model_path)

            # Evaluate the model
            try:
                metrics = evaluate_model(model, x_test, y_test)
                print("Métricas de evaluación:", metrics)
                return metrics
            except ImportError:
                print("No se pudo importar evaluate_model para evaluación.")

        return { "error": "No se pudo completar el proceso de IA." }

    def recommend_content(self):
        # Carga el modelo entrenado
        model_path = os.path.join('static', 'data_ai', 'models', 'knn_model.pkl')
        model: KNeighborsClassifier = joblib.load(model_path)

        mappings_path = os.path.join('static', 'data_ai', 'mappings', 'category_mappings.json')
        with open(mappings_path, 'r', encoding='utf-8') as f:
            self.mappings = json.load(f)

        with app.app_context():
            df = self.extract_data()
            df_processed = self.preprocess_data(df)

            # Filtra contenidos no vistos
            df_not_seen = df_processed[df_processed['nota_obtenida'].isna()]

            if len(df_not_seen) == 0:
                return {"message": "El usuario ha visto todos los contenidos"}

            x_predict = df_not_seen[['materia', 'tema', 'contenido', 'nivel_grado']]
            probabilities = model.predict_proba(x_predict)[:, 1]

            df_not_seen = df_not_seen.copy()
            df_not_seen['prob_aprobar'] = probabilities

            # Recomienda basándose en probabilidad y nivel de grado
            # Prioriza contenidos de menor nivel con alta probabilidad
            df_not_seen['score'] = df_not_seen['prob_aprobar'] - (df_not_seen['nivel_grado'] * 0.1)

            # Ordena por score descendente
            recommended = df_not_seen.nlargest(3, 'score')[['contenido', 'nivel_grado', 'prob_aprobar']]
            recommended['contenido'] = recommended['contenido'].map(self.mappings['contenido'])
            return recommended.to_dict('records')

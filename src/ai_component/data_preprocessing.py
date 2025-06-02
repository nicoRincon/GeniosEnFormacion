import time
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
    _user_models = {}  # {user_id: {'model': model, 'mappings': mappings, 'last_training': timestamp}}

    def __init__(self, filename: str = 'processed_data.csv'):
        self.filename = filename
        self.mappings = {}

    def get_user_id(self) -> int:
        return session.get('user_id', 1)

    def should_retrain(self, user_id: int) -> bool:
        if user_id not in AiComponent._user_models:
            print(f"Re-entrenando: Usuario {user_id} no tiene modelo")
            return True

        user_data = AiComponent._user_models[user_id]
        if time.time() - user_data.get('last_training', 0) > 3600:  # 1 hora
            print(f"Re-entrenando: Usuario {user_id} - modelo obsoleto")
            return True

        return False

    def clear_user_model(self, user_id: int):
        if user_id in AiComponent._user_models:
            print(f"Limpiando modelo del usuario {user_id}")
            del AiComponent._user_models[user_id]

    def get_or_train_model(self, force_retrain: bool = False):
        user_id = self.get_user_id()

        if force_retrain or self.should_retrain(user_id):
            self.clear_user_model(user_id)

            print(f"Entrenando modelo para usuario {user_id}...")
            with app.app_context():
                df = self.extract_data()
                df_processed = self.preprocess_data(df)

                processed_path = os.path.join('static', 'data_ai', 'processed', f'user_{user_id}_{self.filename}')
                os.makedirs(os.path.dirname(processed_path), exist_ok=True)
                df_processed.to_csv(processed_path, index=False)

                model_path = os.path.join('static', 'data_ai', 'models', f'user_{user_id}_knn_model.pkl')
                os.makedirs(os.path.dirname(model_path), exist_ok=True)

                model, _, _ = self.train_and_save_model(df_processed, model_path)

                AiComponent._user_models[user_id] = {
                    'model': model,
                    'mappings': self.mappings.copy(),
                    'last_training': time.time()
                }

                print(f"Modelo entrenado para usuario {user_id}")
        else:
            if user_id not in AiComponent._user_models:
                print(f"Cargando modelo desde archivo para usuario {user_id}...")
                try:
                    model_path = os.path.join('static', 'data_ai', 'models', f'user_{user_id}_knn_model.pkl')
                    model = joblib.load(model_path)
                    mappings_path = os.path.join('static', 'data_ai', 'mappings', f'user_{user_id}_category_mappings.json')
                    with open(mappings_path, 'r', encoding='utf-8') as f:
                        mappings = json.load(f)
                    AiComponent._user_models[user_id] = {
                        'model': model,
                        'mappings': mappings,
                        'last_training': time.time()
                    }
                    print(f"Modelo cargado para usuario {user_id}")
                except FileNotFoundError:
                    print(f"No se encontró modelo para usuario {user_id}, entrenando nuevo...")
                    return self.get_or_train_model(force_retrain=True)
            else:
                print(f"Usando modelo en memoria para usuario {user_id}")

        user_data = AiComponent._user_models[user_id]
        return user_data['model'], user_data['mappings']

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
                Contenido.id.label('id_contenido'),
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
                # Lo que se desea predecir
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
            'contenido': dict(enumerate(contenido_cat.cat.categories)),
            'id_contenido': dict(enumerate(df['id_contenido']))
        }

        df['materia'] = materia_cat.cat.codes
        df['tema'] = tema_cat.cat.codes
        df['contenido'] = contenido_cat.cat.codes
        df['nivel_grado'] = df['nivel_grado'].astype(int)
        df.drop('id_contenido', axis=1, inplace=True)

        user_id = self.get_user_id()
        mappings_path = os.path.join('static', 'data_ai', 'mappings', f'user_{user_id}_category_mappings.json')
        os.makedirs(os.path.dirname(mappings_path), exist_ok=True)
        with open(mappings_path, 'w', encoding='utf-8') as f:
            json.dump(self.mappings, f, ensure_ascii=False, indent=2)

        return df

    def preprocess_data_for_prediction(self, df: pd.DataFrame, existing_mappings: dict) -> pd.DataFrame:
        df = self.clean_data(df)
        df['materia'] = df['materia'].apply(self.normalize_text)
        df['tema'] = df['tema'].apply(self.normalize_text)
        df['contenido'] = df['contenido'].apply(self.normalize_text)

        reverse_mappings = {
            'materia': {v: k for k, v in existing_mappings['materia'].items()},
            'tema': {v: k for k, v in existing_mappings['tema'].items()},
            'contenido': {v: k for k, v in existing_mappings['contenido'].items()}
        }

        df['materia'] = df['materia'].map(reverse_mappings['materia']).fillna(-1).astype(int)
        df['tema'] = df['tema'].map(reverse_mappings['tema']).fillna(-1).astype(int)
        df['contenido'] = df['contenido'].map(reverse_mappings['contenido']).fillna(-1).astype(int)
        df['nivel_grado'] = df['nivel_grado'].astype(int)

        return df

    def train_and_save_model(self, df: pd.DataFrame, model_path: str):
        # Separación datos con notas (para entrenar) y sin notas (para predecir)
        df_with_notes = df[df['nota_obtenida'].notna()].copy()
        df_to_predict = df[df['nota_obtenida'].isna()].copy()

        if len(df_with_notes) < 5:
            print("Muy pocos datos para entrenar. Generando datos sintéticos...")
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
        """Recomienda contenido usando el modelo específico del usuario"""
        try:
            model, mappings = self.get_or_train_model()
            user_id = self.get_user_id()

            with app.app_context():
                df = self.extract_data()

                df_processed = self.preprocess_data_for_prediction(df, mappings)

                df_not_seen = df_processed[df_processed['nota_obtenida'].isna()]

                if len(df_not_seen) == 0:
                    return {"message": f"El usuario {user_id} ha visto todos los contenidos"}

                # Filtra contenidos válidos
                df_not_seen = df_not_seen[
                    (df_not_seen['materia'] != -1) &
                    (df_not_seen['tema'] != -1) &
                    (df_not_seen['contenido'] != -1)
                ]

                if len(df_not_seen) == 0:
                    return {"message": "No hay contenidos nuevos que el modelo pueda procesar"}

                x_predict = df_not_seen[['materia', 'tema', 'contenido', 'nivel_grado']]
                probabilities = model.predict_proba(x_predict)[:, 1]

                df_not_seen = df_not_seen.copy()
                df_not_seen['prob_aprobar'] = probabilities

                df_not_seen['score'] = df_not_seen['prob_aprobar'] - (df_not_seen['nivel_grado'] * 0.1)

                recommended = df_not_seen.nlargest(3, 'score')[['contenido', 'nivel_grado', 'prob_aprobar', 'score']]

                result = []
                for index, row in recommended.iterrows():
                    contenido_code = int(row['contenido'])
                    index_mapping = list(mappings['contenido'].keys()).index(int(row['contenido']))
                    contenido_nombre = mappings['contenido'].get(contenido_code, f"Contenido {contenido_code}")
                    contenido_id = list(mappings['id_contenido'])[index_mapping]

                    result.append({
                        'contenido': contenido_nombre,
                        'id_contenido': contenido_id,
                        'nivel_grado': int(row['nivel_grado']),
                        'prob_aprobar': float(row['prob_aprobar']),
                        'score': float(row['score'])
                    })

                print(f"Recomendaciones para usuario {user_id}: {len(result)} contenidos")
                return result

        except Exception as e:
            user_id = self.get_user_id()
            print(f"Error en recomendación para usuario {user_id}: {e}")
            return {"error": f"Error al generar recomendaciones: {str(e)}"}

    @classmethod
    def clear_all_models(cls):
        """Limpia todos los modelos en memoria (útil para mantenimiento)"""
        for user_id in cls._user_models:
            mappings_path = os.path.join('static', 'data_ai', 'mappings', f'user_{user_id}_category_mappings.json')
            if os.path.isfile(mappings_path):
                os.remove(mappings_path)

            memory_path = os.path.join('static', 'data_ai', 'models', f'user_{user_id}_knn_model.pkl')
            if os.path.isfile(memory_path):
                os.remove(memory_path)

        cls._user_models.clear()
        print("Todos los modelos en memoria han sido limpiados")

    @classmethod
    def get_active_users(cls):
        """Obtiene lista de usuarios con modelos activos"""
        return list(cls._user_models.keys())

import subprocess
from database.Materias.Recurso import Recurso
from src.content_management.contents.contents_service import ContentsService
from database.Materias.TipoActividad import TipoActividad
from database.Materias.Actividad import Actividad
from database.Materias.Contenido import Contenido
from src.db_connection import db

class ActivitiesService:
    def get_activity_by_id(self, activity_id: int) -> Actividad:
        activity_by_id = (
            Actividad.query
            .with_entities(
                Actividad.id,
                Actividad.id_contenido,
                Actividad.id_tipo_actividad,
                Actividad.contenido,
            )
            .filter(Actividad.id == activity_id)
            .first()
        )
        if activity_by_id is None:
            raise ValueError(f"Actividad con ID {activity_id} no existe.")
        return activity_by_id

    def get_all_activities(self) -> list[Actividad]:
        all_activities = (
            Actividad.query
            .with_entities(
                Actividad.id,
                Contenido.titulo.label('nombre_contenido'),
                TipoActividad.tipo_actividad,
                Actividad.contenido,
            )
            .join(Actividad.contenido_relacionado)
            .join(Actividad.tipo_actividad_relacionada)
            .all()
        )
        if len(all_activities) == 0:
            raise ValueError("No hay actividades disponibles.")

        return all_activities

    def create_activity(self, content_id: int, activity_type_id: int, content: str):
        ContentsService().get_content_by_id(content_id)
        self.validate_type_activity(activity_type_id)
        self.validate_activity(content, content_id, None)

        new_activity = Actividad()
        new_activity.id_contenido = content_id
        new_activity.id_tipo_actividad = activity_type_id
        new_activity.contenido = content

        subprocess.run(
            ["python", "-m", "ai_component.src.data_preprocessing"],
            check=True,
        )

        db.session.add(new_activity)
        db.session.commit()
        return { 'message': "Actividad creada." }

    def update_activity(
        self,
        activity_id: int,
        content_id: int,
        activity_type_id: int,
        content: str
    ):
        ContentsService().get_content_by_id(content_id)
        self.validate_type_activity(activity_type_id)

        activity_to_update: Actividad = Actividad.query.filter(Actividad.id == activity_id).first()
        if activity_to_update is None:
            raise ValueError(f"Actividad con ID {activity_id} no existe.")

        self.validate_activity(content, content_id, activity_id)

        activity_to_update.contenido = content
        activity_to_update.id_contenido = content_id
        activity_to_update.id_tipo_actividad = activity_type_id

        db.session.commit()
        return { 'message': f"Actividad {activity_id} actualizada." }

    def delete_activity(self, activity_id: int):
        activity_to_delete: Actividad = Actividad.query.filter(Actividad.id == activity_id).first()

        if activity_to_delete is None:
            raise ValueError(f"Actividad con ID {activity_id} no existe.")

        resource = Recurso.query.filter(Recurso.id_actividad == activity_id).first()
        if resource:
            raise ValueError(
                "La actividad no se puede eliminar porque tiene recursos asociados"
            )

        db.session.delete(activity_to_delete)
        db.session.commit()
        return { 'message': f"Actividad {activity_id} eliminada." }

    def validate_activity(self, content: str, content_id: int, activity_id: int|None):
        activity = Actividad.query
        if activity_id is not None:
            activity = activity.filter(Actividad.id != activity_id)

        activity = activity.filter(Actividad.id_contenido == content_id, Actividad.contenido == content)
        activity = activity.first()

        if activity:
            raise ValueError("La actividad ya existe para el contenido seleccionado.")

    def validate_type_activity(self, activity_type_id: int):
        activity_type = TipoActividad.query.filter(TipoActividad.id == activity_type_id).first()
        if activity_type is None:
            raise ValueError(f"El tipo de actividad con el id: {activity_type_id}, no existe.")
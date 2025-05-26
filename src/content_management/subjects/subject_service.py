from database.Materias.Materia import Materia
from database.Materias.Tema import Tema
from database.Materias.UsuarioMateria import UsuarioMateria
from database.Usuarios.Usuario import Usuario
from src.db_connection import db

class SubjectsService:
    def get_subject_by_id(self, subject_id: int) -> Materia:
        subject_by_id = (
            Materia.query
            .with_entities(
                Materia.id,
                Materia.nombre,
                Materia.descripcion,
            )
            .filter(Materia.id == subject_id)
            .first()
        )
        if subject_by_id is None:
            raise ValueError(f"Materia con ID {subject_id} no existe.")
        return subject_by_id

    def get_all_subjects(self) -> list[Materia]:
        all_subjects = (
            Materia.query
            .with_entities(
                Materia.id,
                Materia.nombre,
                Materia.descripcion,
            )
            .all()
        )
        if len(all_subjects) == 0:
            raise ValueError("No hay materias disponibles.")

        return all_subjects

    def create_subject(self, subject_name: str, subject_description: str|None):
        self.validate_subject(subject_name, None)

        new_subject = Materia(nombre=subject_name, descripcion=subject_description)
        db.session.add(new_subject)
        db.session.commit()
        return { 'message': f"Materia {subject_name} creada." }

    def update_subject(self, subject_id: int, subject_name: str, subject_description: str):
        subject_to_update: Materia = Materia.query.filter(Materia.id == subject_id).first()
        if subject_to_update is None:
            raise ValueError(f"Materia con ID {subject_id} no existe.")

        self.validate_subject(subject_name, subject_id)

        subject_to_update.nombre = subject_name
        subject_to_update.descripcion = subject_description
        db.session.commit()
        return { 'message': f"Tema {subject_id} actualizado." }

    def delete_subject(self, subject_id: int):
        subject_to_delete = Materia.query.filter(Materia.id == subject_id).first()
        if subject_to_delete is None:
            raise ValueError(f"Materia con ID {subject_id} no existe.")

        associated_data = (
            Materia.query
            .join(Usuario.usuario_materia, isouter=True)
            .join(Materia, UsuarioMateria.id_materia == Materia.id,  isouter=True)
            .join(Tema, Tema.id_materia == Materia.id, isouter=True)
            .filter(Materia.id == subject_id)
            .with_entities(
                UsuarioMateria.id_usuario,
                Tema.id.label('id_tema'),
                Materia.id,
                Materia.nombre,
            )
            .all()
        )

        error_messages = []

        user_associated = False
        topic_associated = False
        for associated_data in associated_data:
            if associated_data.id_usuario is not None and user_associated:
                user_associated = True

            if associated_data.id_tema is not None and topic_associated:
                topic_associated = True

            if user_associated and topic_associated:
                break

        if user_associated:
            error_messages.append(
                f"La materia {associated_data.nombre} no se puede eliminar porque tiene usuarios asociados."
            )
        if topic_associated:
            error_messages.append(
                f"La materia {associated_data.nombre} no se puede eliminar porque tiene temas asociados."
            )

        if error_messages:
            raise ValueError(", ".join(error_messages))

        db.session.delete(subject_to_delete)
        db.session.commit()
        return { 'message': f"Materia {subject_id} eliminada." }

    def validate_subject(self, subject_name: str, subject_id: int|None):
        subject = Materia.query

        if subject_id is not None:
            subject = subject.filter(Materia.id != subject_id)
        subject = subject.all()

        if subject and subject[0].nombre == subject_name:
            raise ValueError(f"Materia con el nombre: {subject_name}, ya existe.")

        return subject
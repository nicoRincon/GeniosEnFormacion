from database.Materias.Materia import Materia
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
        materia_to_update: Materia = Materia.query.filter(Materia.id == subject_id).first()
        if materia_to_update is None:
            raise ValueError(f"Materia with ID {subject_id} no existe.")

        self.validate_subject(subject_name, subject_id)

        materia_to_update.nombre = subject_name
        materia_to_update.descripcion = subject_description
        db.session.commit()
        return { 'message': f"Materia {subject_id} actualizada." }

    def delete_subject(self, subject_id: int):
        subject_to_delete = Materia.query.filter(Materia.id == subject_id).first()
        if subject_to_delete is None:
            raise ValueError(f"Materia con ID {subject_id} no existe.")

        user: Usuario = (
            Usuario.query
            .join(UsuarioMateria.usuarios)
            .filter(Usuario.id == subject_id)
            .first()
        )
        if user:
            raise ValueError(f"La materia {subject_id} no se puede eliminar porque tiene usuarios asociados.")

        db.session.delete(subject_to_delete)
        db.session.commit()
        return { 'message': f"Materia {subject_id} eliminada." }

    def validate_subject(self, subject_name: str, subject_id: int|None):
        subject = Materia.query

        if subject_id is not None:
            subject = subject.filter(Materia.id != subject_id)
        print(subject.statement)
        subject = subject.all()

        if subject and subject[0].nombre == subject_name:
            raise ValueError(f"Materia con el nombre: {subject_name}, ya existe.")

        return subject
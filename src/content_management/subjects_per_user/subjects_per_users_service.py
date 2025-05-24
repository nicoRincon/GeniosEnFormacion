from flask import session
from database.Materias.Materia import Materia
from database.Materias.UsuarioMateria import UsuarioMateria
from database.Usuarios.Usuario import Usuario
from src.db_connection import db
from src.content_management.subjects.subject_service import SubjectsService

class SubjectsPerUsersService:
    def get_subjects_per_user(self) -> list[Materia]:
        subjects = (
            Materia.query
            .with_entities(
                Materia.id,
                Materia.nombre,
                Materia.descripcion,
            )
            .join(UsuarioMateria, UsuarioMateria.id_materia == Materia.id)
            .join(Usuario, Usuario.id == UsuarioMateria.id_usuario)
            .filter(Usuario.id == session['user_id'])
            .all()
        )
        if len(subjects) == 0:
            raise ValueError(f"No hay materias disponibles para el usuario {session['username']}.")

        return subjects

    def set_subjects_per_user(self, subject_id: int):
        SubjectsService().get_subject_by_id(subject_id)

        user_per_subject = (
            UsuarioMateria.query
            .with_entities(
                Materia.id,
                Materia.nombre,
                Materia.descripcion,
                UsuarioMateria.id_usuario,
            )
            .join(Materia, UsuarioMateria.id_materia == Materia.id)
            .join(Usuario, Usuario.id == UsuarioMateria.id_usuario)
            .filter(Usuario.id == session['user_id'], Materia.id == subject_id)
            .first()
        )

        if user_per_subject is None:
            user_per_subject_to_create = UsuarioMateria(
                id_usuario=session['user_id'],
                id_materia=subject_id
            )
            db.session.add(user_per_subject_to_create)
            db.session.commit()

    def delete_subjects_by_user(self, subject_id: int):
        subject = SubjectsService().get_subject_by_id(subject_id)

        subject_to_delete = (
            UsuarioMateria.query
            .filter(UsuarioMateria.id_usuario == session['user_id'], UsuarioMateria.id_materia == subject_id)
            .first()
        )
        if subject_to_delete is None:
            raise ValueError(f"La materia {subject.nombre} no existe para el usuario {session['username']}.")

        db.session.delete(subject_to_delete)
        db.session.commit()
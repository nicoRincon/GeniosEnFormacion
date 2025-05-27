from flask import session
from database.Materias.Materia import Materia
from database.Materias.UsuarioMateria import UsuarioMateria
from database.Usuarios.Usuario import Usuario
from src.db_connection import db
from src.content_management.subjects.subject_service import SubjectsService
from src.users.roles_service import RolesService

class SubjectsPerUsersService:
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

        if user_per_subject is not None:
            raise ValueError("La materia ya está asignada a este usuario.")

        user_per_subject_to_create = UsuarioMateria(
            id_usuario=session['user_id'],
            id_materia=subject_id
        )
        db.session.add(user_per_subject_to_create)
        db.session.commit()
        return user_per_subject_to_create.id

    def delete_assignment_by_id(self, assignment_id: int):
        assignment = (
            UsuarioMateria.query
            .filter(
                UsuarioMateria.id == assignment_id,
            )
        )

        roles_service = RolesService().get_role_by_user_id(session['user_id'])
        if roles_service.id != 1:
            assignment = assignment.filter(UsuarioMateria.id_usuario == session['user_id'])
        assignment = assignment.first()
        if assignment is None:
            raise ValueError("La asignación no existe.")
        db.session.delete(assignment)
        db.session.commit()

    def get_all_subjects_per_user(self) -> list[Materia]:
        subjects = (
            Materia.query
            .with_entities(
                UsuarioMateria.id.label('id_asignacion'),
                Usuario.nombre.label('nombre_usuario'),
                Materia.id,
                Materia.nombre,
                Materia.descripcion,
            )
            .join(UsuarioMateria, UsuarioMateria.id_materia == Materia.id)
            .join(Usuario, Usuario.id == UsuarioMateria.id_usuario)
        )

        roles_service = RolesService().get_role_by_user_id(session['user_id'])
        if roles_service.id != 1:
            subjects = subjects.filter(Usuario.id == session['user_id'])

        subjects = subjects.all()

        if len(subjects) == 0:
            raise ValueError(f"No hay materias disponibles para el usuario {session['username']}.")

        return subjects
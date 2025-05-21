from database.Usuarios.Rol import Rol
from database.Usuarios.Usuario import Usuario
from src.db_connection import db

class Roles:
    def get_role_by_id(self, role_id: int):
        role_by_id = db.session.query(Rol).filter(Rol.id == role_id).first()
        if role_by_id is None:
            raise ValueError(f"Rol con ID {role_id} no existe.")
        return role_by_id

    def get_all_roles(self):
        all_roles = Rol.query.all()
        if len(all_roles) == 0:
            raise ValueError("No hay roles disponibles.")

        return all_roles

    def create_role(self, role_name: str):
        new_role = Rol(nombre_rol=role_name)
        db.session.add(new_role)
        db.session.commit()
        return { 'message': f"Rol {role_name} creado." }

    def update_role(self, role_id: int, new_role_name: str):
        role_to_update = db.session.query(Rol).filter(Rol.id == role_id).first()
        if role_to_update is None:
            raise ValueError(f"Role with ID {role_id} no existe.")
        role_to_update.nombre_rol = new_role_name
        db.session.commit()
        return { 'message': f"Rol {role_id} actualizado." }

    def delete_role(self, role_id: int):
        role_to_delete = db.session.query(Rol).filter(Rol.id == role_id).first()
        if role_to_delete is None:
            raise ValueError(f"Rol con ID {role_id} no existe.")

        user = db.session.query(Usuario).filter(Usuario.id_rol == role_id).first()
        if user:
            raise ValueError(f"Rol {role_id} no se puede eliminar porque tiene usuarios asociados.")

        db.session.delete(role_to_delete)
        db.session.commit()
        return { 'message': f"Rol {role_id} eliminado." }
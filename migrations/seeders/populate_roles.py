import sys
import os
from sqlalchemy import exc, text

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.db_connection import db, app
from database.Usuarios.Rol import Rol

def safe_insert_role(role_name):
    """Función segura para insertar roles con manejo de errores"""
    try:
        # Verificar si el rol ya existe
        exists = db.session.query(Rol).filter_by(nombre_rol=role_name).first()
        if exists:
            print(f"Rol '{role_name}' ya existe en la base de datos")
            return False
        
        # Crear nuevo rol
        new_role = Rol(nombre_rol=role_name)
        db.session.add(new_role)
        db.session.commit()
        print(f"Rol '{role_name}' insertado correctamente")
        return True
        
    except exc.IntegrityError as e:
        db.session.rollback()
        print(f"Error de integridad al insertar '{role_name}': {e}")
        return False
    except Exception as e:
        db.session.rollback()
        print(f"Error inesperado con '{role_name}': {e}")
        return False

def up():
    """Insertar roles básicos"""
    with app.app_context():
        roles = ['Superadmin', 'Profesor', 'Estudiante']
        success_count = 0
        
        for role_name in roles:
            if safe_insert_role(role_name):
                success_count += 1
        
        print(f"\nResumen: {success_count}/{len(roles)} roles insertados correctamente")

def down():
    """Eliminar roles insertados (función de reversión)"""
    with app.app_context():
        try:
            # Eliminar relaciones primero (si existen)
            db.session.execute(text('DELETE FROM rol_paginas WHERE rol_id IN (SELECT id FROM roles WHERE nombre_rol IN :roles)'),
                             {'roles': ('Superadmin', 'Profesor', 'Estudiante')})
            
            # Eliminar los roles
            delete_count = db.session.query(Rol)\
                .filter(Rol.nombre_rol.in_(['Superadmin', 'Profesor', 'Estudiante']))\
                .delete(synchronize_session=False)
            
            db.session.commit()
            
            # Resetear autoincremental (MySQL)
            try:
                db.session.execute(text('ALTER TABLE roles AUTO_INCREMENT = 1'))
                db.session.commit()
            except Exception as alter_err:
                print(f"Advertencia: No se pudo resetear el autoincremento: {alter_err}")
            
            print(f"\nSe eliminaron {delete_count} roles y sus relaciones")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error durante la reversión: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "down":
        down()
    else:
        up()
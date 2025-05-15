import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '../../'
        )
    )
)

from src.db_connection import db, app
from database.Usuarios.Rol import Rol

def up():
    with app.app_context():
        try:
            roles = ['Superadmin', 'Profesor', 'Estudiante']
            for nombre in roles:
                rol = Rol(nombre_rol=nombre)
                db.session.add(rol)
            db.session.commit()
            print("Roles insertados")
        except Exception as e:
            db.session.rollback()
            print(f"Error insertando roles: {e}")

def down():
    with app.app_context():
        try:
            db.session.query(Rol).filter(Rol.nombre_rol.in_(['Superadmin', 'Profesor', 'Estudiante'])).delete(synchronize_session=False)
            db.session.commit()
            print("Roles eliminados")
        except Exception as e:
            db.session.rollback()
            print(f"Error eliminando roles: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "down":
        down()
    else:
        up()
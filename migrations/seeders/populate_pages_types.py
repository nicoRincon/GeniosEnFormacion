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
from sqlalchemy import text
from database.Paginas.TipoPagina import TipoPagina

def up():
    with app.app_context():
        try:
            page_types = ['Modulo', 'Paginas', 'Sub-paginas']
            for page_type in page_types:
                page_type = TipoPagina(nombre_tipo_pagina=page_type)
                db.session.add(page_type)
            db.session.commit()
            print("Tipos de paginas insertadas")
        except Exception as e:
            db.session.rollback()
            print(f"Error insertando tipos de paginas: {e}")

def down():
    with app.app_context():
        try:
            TipoPagina.query.filter(
                TipoPagina.nombre_tipo_pagina.in_(['Modulo', 'Paginas', 'Sub-paginas'])
            ).delete(synchronize_session=False)
            db.session.commit()

            db.session.execute(text('ALTER TABLE tipos_pagina AUTO_INCREMENT = 1;'))
            db.session.commit()
            print("Tipos de paginas eliminadas")
        except Exception as e:
            db.session.rollback()
            print(f"Error eliminando tipos de paginas: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "down":
        down()
    else:
        up()
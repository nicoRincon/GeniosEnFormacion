from typing import List
from flask import session
from database.Paginas.RolPagina import RolPagina
from database.Usuarios.Usuario import Usuario
from database.Paginas.Pagina import Pagina

class PagesByUsers:
    def get_page_by_user_id(self, user_id: int):
        page_by_user: List[Pagina] = (
            Pagina.query
            .with_entities(
                Pagina.id,
                Pagina.nombre_pagina,
                Pagina.ruta,
                Pagina.id_tipo_pagina,
                Pagina.id_pagina_padre,
            )
            .join(RolPagina.pagina)
            .join(Usuario.rol)
            .filter(Usuario.id == user_id)
            .order_by(Pagina.id)
            .all()
        )
        if len(page_by_user) == 0:
            raise ValueError(f"El usuario {session['username']} no tiene paginas asignadas.")

        hierarchy = []

        for module in page_by_user:
            if module.id_tipo_pagina == 1:
                module_data = {
                    "module": module.nombre_pagina,
                    "pages": []
                }

                # Busca páginas hijas
                for page in page_by_user:
                    if page.id_pagina_padre == module.id:
                        dict_pages = {
                            "page": page.nombre_pagina,
                            "route": page.ruta,
                            "sub_page": [{"sub_page": sp.nombre_pagina, "route": sp.ruta} for sp in page_by_user if sp.id_pagina_padre == page.id]
                        }
                        module_data["pages"].append(dict_pages)
                hierarchy.append(module_data)

        return hierarchy

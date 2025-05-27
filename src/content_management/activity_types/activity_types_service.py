from database.Materias.TipoActividad import TipoActividad

class ActivityTypesService:
    def get_all_activity_types(self) -> list[TipoActividad]:
        all_activity_types = (
            TipoActividad.query
            .with_entities(
                TipoActividad.id,
                TipoActividad.tipo_actividad,
                TipoActividad.peso
            )
            .all()
        )
        if len(all_activity_types) == 0:
            raise ValueError("No hay tipos de contenidos parametrizados.")

        return all_activity_types

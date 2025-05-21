import sys
import os
from sqlalchemy import text
from datetime import datetime
from werkzeug.security import generate_password_hash

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '../../'
        )
    )
)

from src.db_connection import db, app
from database.Usuarios.Usuario import Usuario
from database.Materias.Materia import Materia
from database.Materias.Tema import Tema
from database.Materias.Contenido import Contenido
from database.Materias.Ejemplo import Ejemplo
from database.Materias.TipoActividad import TipoActividad
from database.Materias.Actividad import Actividad
from database.Materias.Recurso import Recurso
from database.Materias.Evaluacion import Evaluacion
from database.Materias.UsuarioMateria import UsuarioMateria
from database.Materias.NotaContenido import NotaContenido

def up():
    with app.app_context():
        try:
            # 1. Crear usuarios de prueba
            if Usuario.query.count() == 0:
                print("Creando usuarios de prueba...")
                usuarios = [
                    {
                        'id_rol': 1,  # Superadmin
                        'nombre': 'Admin',
                        'apellido': 'Principal',
                        'nombre_usuario': 'admin',
                        'correo': 'admin@geniosenformacion.com',
                        'clave': generate_password_hash('Admin123*')
                    },
                    {
                        'id_rol': 2,  # Profesor
                        'nombre': 'María',
                        'apellido': 'Gómez',
                        'nombre_usuario': 'maria.profesor',
                        'correo': 'maria@geniosenformacion.com',
                        'clave': generate_password_hash('Profe123*')
                    },
                    {
                        'id_rol': 3,  # Estudiante
                        'nombre': 'Juan',
                        'apellido': 'Pérez',
                        'nombre_usuario': 'juan.estudiante',
                        'correo': 'juan@geniosenformacion.com',
                        'clave': generate_password_hash('Alumno123*')
                    },
                    {
                        'id_rol': 3,  # Estudiante
                        'nombre': 'Ana',
                        'apellido': 'Martínez',
                        'nombre_usuario': 'ana.estudiante',
                        'correo': 'ana@geniosenformacion.com',
                        'clave': generate_password_hash('Alumno123*')
                    }
                ]
                for usuario_data in usuarios:
                    usuario = Usuario(**usuario_data)
                    db.session.add(usuario)
                db.session.commit()
                print("Usuarios creados correctamente")
            
            # 2. Crear tipos de actividad
            if TipoActividad.query.count() == 0:
                print("Creando tipos de actividad...")
                tipos_actividad = [
                    {'tipo_actividad': 'Lectura', 'peso': 20},
                    {'tipo_actividad': 'Escritura', 'peso': 25},
                    {'tipo_actividad': 'Juego Interactivo', 'peso': 30},
                    {'tipo_actividad': 'Quiz', 'peso': 25}
                ]
                for tipo_data in tipos_actividad:
                    tipo = TipoActividad(**tipo_data)
                    db.session.add(tipo)
                db.session.commit()
                print("Tipos de actividad creados correctamente")
            
            # 3. Crear materia de Español
            materia_espanol = Materia.query.filter_by(nombre='Español').first()
            if not materia_espanol:
                print("Creando materia de Español...")
                materia_espanol = Materia(
                    nombre='Español',
                    descripcion='Aprendizaje del idioma español, lectura, escritura y comunicación.'
                )
                db.session.add(materia_espanol)
                db.session.commit()
                print("Materia Español creada correctamente")
            
            # 4. Crear temas para la materia de Español
            if Tema.query.filter_by(id_materia=materia_espanol.id).count() == 0:
                print("Creando temas para Español...")
                temas_espanol = [
                    {
                        'id_materia': materia_espanol.id,
                        'nombre': 'El Abecedario',
                        'descripcion': 'Aprende las letras del abecedario español y sus sonidos.'
                    },
                    {
                        'id_materia': materia_espanol.id,
                        'nombre': 'Las Vocales',
                        'descripcion': 'Aprende sobre las vocales: a, e, i, o, u.'
                    },
                    {
                        'id_materia': materia_espanol.id,
                        'nombre': 'Formando Sílabas',
                        'descripcion': 'Aprende a formar sílabas combinando consonantes y vocales.'
                    },
                    {
                        'id_materia': materia_espanol.id,
                        'nombre': 'Palabras y Oraciones',
                        'descripcion': 'Aprende a formar palabras y oraciones simples.'
                    }
                ]
                
                for tema_data in temas_espanol:
                    tema = Tema(**tema_data)
                    db.session.add(tema)
                db.session.commit()
                print("Temas creados correctamente")
            
            # 5. Crear contenido para "El Abecedario"
            tema_abecedario = Tema.query.filter_by(nombre='El Abecedario').first()
            
            if not tema_abecedario:
                print("Error: No se encontró el tema 'El Abecedario'")
                return
                
            if Contenido.query.filter_by(id_tema=tema_abecedario.id).count() == 0:
                print("Creando contenido para El Abecedario...")
                contenido_abecedario = Contenido(
                    id_tema=tema_abecedario.id,
                    titulo='El Abecedario Español',
                    contenido="""
                    <h2>El Abecedario Español</h2>
                    <p>El abecedario español tiene 27 letras. Cada letra tiene un sonido que nos ayuda a formar palabras cuando hablamos y escribimos.</p>
                    
                    <p>Las letras del abecedario español son:</p>
                    <ul>
                        <li>A a - como en "avión"</li>
                        <li>B b - como en "barco"</li>
                        <li>C c - como en "casa"</li>
                        <li>D d - como en "dedo"</li>
                        <li>E e - como en "elefante"</li>
                        <li>F f - como en "foca"</li>
                        <li>G g - como en "gato"</li>
                        <li>H h - como en "helado"</li>
                        <li>I i - como en "iglesia"</li>
                        <li>J j - como en "juego"</li>
                        <li>K k - como en "kiosco"</li>
                        <li>L l - como en "luna"</li>
                        <li>M m - como en "mamá"</li>
                        <li>N n - como en "nube"</li>
                        <li>Ñ ñ - como en "niño"</li>
                        <li>O o - como en "oso"</li>
                        <li>P p - como en "papá"</li>
                        <li>Q q - como en "queso"</li>
                        <li>R r - como en "rosa"</li>
                        <li>S s - como en "sol"</li>
                        <li>T t - como en "taza"</li>
                        <li>U u - como en "uva"</li>
                        <li>V v - como en "vaca"</li>
                        <li>W w - como en "wifi"</li>
                        <li>X x - como en "xilófono"</li>
                        <li>Y y - como en "yo-yo"</li>
                        <li>Z z - como en "zapato"</li>
                    </ul>
                    
                    <p>Cada letra puede escribirse de dos formas: <strong>mayúscula</strong> y <strong>minúscula</strong>.</p>
                    
                    <p>Usamos mayúsculas al inicio de oraciones y para nombres propios como "María" o "Colombia".</p>
                    """,
                    nivel_grado=1
                )
                db.session.add(contenido_abecedario)
                db.session.commit()
                
                # 6. Crear ejemplos para "El Abecedario"
                print("Creando ejemplos para El Abecedario...")
                ejemplos_abecedario = Ejemplo(
                    id_contenido=contenido_abecedario.id,
                    ejemplos="""
                    <h3>Ejemplos del Abecedario</h3>
                    
                    <h4>Letras mayúsculas y minúsculas</h4>
                    <p>A (mayúscula) - a (minúscula): Ana come una manzana.</p>
                    <p>B (mayúscula) - b (minúscula): Brenda tiene un barco.</p>
                    <p>C (mayúscula) - c (minúscula): Carlos vive en una casa.</p>
                    
                    <h4>Palabras que empiezan con la misma letra</h4>
                    <ul>
                        <li>M: Mamá, Mesa, Manzana</li>
                        <li>P: Pelota, Papel, Pato</li>
                        <li>S: Sol, Sombrero, Sopa</li>
                    </ul>
                    
                    <h4>Letras al inicio de palabras</h4>
                    <ul>
                        <li>A de Avión</li>
                        <li>B de Barco</li>
                        <li>C de Casa</li>
                        <li>D de Dedo</li>
                        <li>E de Elefante</li>
                    </ul>
                    """
                )
                db.session.add(ejemplos_abecedario)
                db.session.commit()
                
                # 7. Crear actividades para "El Abecedario"
                print("Creando actividades para El Abecedario...")
                
                # Actividad 1: Encuentra la letra
                actividad1 = Actividad(
                    id_contenido=contenido_abecedario.id,
                    id_tipo_actividad=3,  # Juego Interactivo
                    contenido="""
                    <h3>Actividad 1: Encuentra la letra</h3>
                    <p>Observa las imágenes y selecciona la letra con la que comienza cada palabra.</p>
                    
                    <div class="actividad-item">
                        <img src="/static/img/actividades/dinosaurio.jpg" alt="Dinosaurio">
                        <p>Dinosaurio</p>
                        <div class="opciones">
                            <button>B</button>
                            <button>D</button>
                            <button>P</button>
                        </div>
                    </div>
                    
                    <div class="actividad-item">
                        <img src="/static/img/actividades/tortuga.jpg" alt="Tortuga">
                        <p>Tortuga</p>
                        <div class="opciones">
                            <button>S</button>
                            <button>T</button>
                            <button>J</button>
                        </div>
                    </div>
                    
                    <div class="actividad-item">
                        <img src="/static/img/actividades/manzana.jpg" alt="Manzana">
                        <p>Manzana</p>
                        <div class="opciones">
                            <button>M</button>
                            <button>N</button>
                            <button>A</button>
                        </div>
                    </div>
                    """
                )
                db.session.add(actividad1)
                
                # Actividad 2: Ordena el abecedario
                actividad2 = Actividad(
                    id_contenido=contenido_abecedario.id,
                    id_tipo_actividad=3,  # Juego Interactivo
                    contenido="""
                    <h3>Actividad 2: Ordena el abecedario</h3>
                    <p>Arrastra las letras a su posición correcta en el abecedario.</p>
                    
                    <div class="abecedario-container">
                        <div class="letra-placeholder">A</div>
                        <div class="letra-placeholder">B</div>
                        <div class="letra-placeholder">C</div>
                        <div class="letra-placeholder">?</div>
                        <div class="letra-placeholder">E</div>
                        <div class="letra-placeholder">F</div>
                        <div class="letra-placeholder">?</div>
                        <div class="letra-placeholder">H</div>
                    </div>
                    
                    <div class="letras-disponibles">
                        <div class="letra-dragable">D</div>
                        <div class="letra-dragable">G</div>
                    </div>
                    """
                )
                db.session.add(actividad2)
                
                # Actividad 3: Crea palabras con letras
                actividad3 = Actividad(
                    id_contenido=contenido_abecedario.id,
                    id_tipo_actividad=2,  # Escritura
                    contenido="""
                    <h3>Actividad 3: Crea palabras con letras</h3>
                    <p>Une las letras para formar la palabra que describe cada imagen.</p>
                    
                    <div class="palabra-container">
                        <img src="/static/img/actividades/pelota.jpg" alt="Pelota">
                        <div class="letras-palabra">
                            <span>P</span>
                            <span>E</span>
                            <span>L</span>
                            <span>O</span>
                            <span>T</span>
                            <span>A</span>
                        </div>
                        <input type="text" placeholder="Escribe la palabra">
                    </div>
                    
                    <div class="palabra-container">
                        <img src="/static/img/actividades/zapato.jpg" alt="Zapato">
                        <div class="letras-palabra">
                            <span>Z</span>
                            <span>A</span>
                            <span>P</span>
                            <span>A</span>
                            <span>T</span>
                            <span>O</span>
                        </div>
                        <input type="text" placeholder="Escribe la palabra">
                    </div>
                    """
                )
                db.session.add(actividad3)
                db.session.commit()
                print("Actividades insertadas correctamente.")
                
                # 8. Crear evaluación para "El Abecedario"
                print("Creando evaluación para El Abecedario...")
                
                # Buscar el usuario profesor
                profesor = Usuario.query.filter_by(nombre_usuario='maria.profesor').first()
                
                if profesor:
                    evaluacion_abecedario = Evaluacion(
                        id_usuario=profesor.id,
                        id_contenido=contenido_abecedario.id,
                        titulo='Evaluación: El Abecedario',
                        tipo_evaluacion='quiz',
                        lista_preguntas="""
                        [
                            {
                                "pregunta": "¿Cuántas letras tiene el abecedario español?",
                                "tipo": "opcion_multiple",
                                "opciones": ["25 letras", "26 letras", "27 letras", "28 letras"],
                                "respuesta_correcta": "27 letras"
                            },
                            {
                                "pregunta": "¿Qué letra viene después de la 'J' en el abecedario?",
                                "tipo": "opcion_multiple",
                                "opciones": ["H", "I", "K", "L"],
                                "respuesta_correcta": "K"
                            },
                            {
                                "pregunta": "Relaciona cada imagen con la letra inicial correcta",
                                "tipo": "relacionar",
                                "items": [
                                    {"imagen": "oso.jpg", "letra": "O"},
                                    {"imagen": "uva.jpg", "letra": "U"},
                                    {"imagen": "elefante.jpg", "letra": "E"}
                                ]
                            },
                            {
                                "pregunta": "¿Cuándo se usan las letras mayúsculas?",
                                "tipo": "seleccion_multiple",
                                "opciones": [
                                    "Al inicio de una oración",
                                    "En los nombres propios como 'María' o 'Colombia'",
                                    "En todas las palabras de un texto",
                                    "Después de un punto"
                                ],
                                "respuestas_correctas": [
                                    "Al inicio de una oración",
                                    "En los nombres propios como 'María' o 'Colombia'",
                                    "Después de un punto"
                                ]
                            },
                            {
                                "pregunta": "Completa la palabra con la letra correcta: PE_RO",
                                "tipo": "completar",
                                "opciones": ["R", "L", "S", "T"],
                                "respuesta_correcta": "R"
                            }
                        ]
                        """
                    )
                    db.session.add(evaluacion_abecedario)
                    db.session.commit()
                    print("Evaluación insertada correctamente.")
                else:
                    print("No se encontró el usuario profesor para crear la evaluación")
                
                # 9. Crear recursos para las actividades
                print("Creando recursos para las actividades...")
                
                # Recurso para Actividad 1
                recurso1 = Recurso(
                    id_actividad=actividad1.id,
                    titulo='Audio del Abecedario',
                    tipo='audio',
                    contenido='/static/audio/abecedario.mp3',
                    descripcion='Grabación con la pronunciación de cada letra del abecedario'
                )
                db.session.add(recurso1)
                
                # Recurso para Actividad 2
                recurso2 = Recurso(
                    id_actividad=actividad2.id,
                    titulo='Video del Abecedario',
                    tipo='video',
                    contenido='/static/video/abecedario_animado.mp4',
                    descripcion='Video animado sobre el abecedario español'
                )
                db.session.add(recurso2)
                
                # Recurso para Actividad 3
                recurso3 = Recurso(
                    id_actividad=actividad3.id,
                    titulo='Tarjetas de palabras',
                    tipo='imagen',
                    contenido='/static/img/recursos/tarjetas_abecedario.jpg',
                    descripcion='Tarjetas con palabras que empiezan con cada letra'
                )
                db.session.add(recurso3)
                db.session.commit()
                print("Recursos creados correctamente.")
                
                # 10. Asignar materias a usuarios
                print("Asignando materias a usuarios...")
                
                # Asignar Español al profesor
                if profesor:
                    profesor_materia = UsuarioMateria(
                        id_usuario=profesor.id,
                        id_materia=materia_espanol.id
                    )
                    db.session.add(profesor_materia)
                
                # Asignar Español a los estudiantes
                estudiantes = Usuario.query.filter_by(id_rol=3).all()
                for estudiante in estudiantes:
                    estudiante_materia = UsuarioMateria(
                        id_usuario=estudiante.id,
                        id_materia=materia_espanol.id
                    )
                    db.session.add(estudiante_materia)
                
                db.session.commit()
                print("Materias asignadas correctamente a los usuarios.")
                
                print("¡Datos educativos insertados correctamente en la base de datos!")
                
            else:
                print("Ya existe contenido para el tema 'El Abecedario'. No se insertó contenido adicional.")
                
        except Exception as e:
            db.session.rollback()
            print(f"Error al insertar datos educativos: {e}")
            raise e

def down():
    with app.app_context():
        try:
            # Eliminar recursos
            Recurso.query.delete()
            
            # Eliminar evaluaciones
            Evaluacion.query.delete()
            
            # Eliminar actividades
            Actividad.query.delete()
            
            # Eliminar ejemplos
            Ejemplo.query.delete()
            
            # Eliminar contenidos
            Contenido.query.delete()
            
            # Eliminar usuarios_x_materia
            UsuarioMateria.query.delete()
            
            # Eliminar temas
            Tema.query.delete()
            
            # Eliminar materias
            Materia.query.delete()
            
            # Eliminar tipos de actividad
            TipoActividad.query.delete()
            
            # Eliminar notas_x_contenido
            NotaContenido.query.delete()
            
            # Eliminar usuarios (excepto superadmin)
            Usuario.query.filter(Usuario.id_rol != 1).delete()
            
            # Restablecer autoincrement
            tables = ['recursos', 'evaluaciones', 'actividades', 'ejemplos', 'contenido', 'usuarios_x_materia', 
                     'temas', 'materias', 'tipo_actividad', 'notas_x_contenido', 'usuarios']
            
            for table in tables:
                db.session.execute(text(f'ALTER TABLE {table} AUTO_INCREMENT = 1;'))
            
            db.session.commit()
            print("Datos educativos eliminados correctamente.")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error eliminando datos educativos: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "down":
        down()
    else:
        up()
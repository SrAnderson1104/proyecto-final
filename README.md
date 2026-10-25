# Buscador de películas

Proyecto final del Bootcamp *Aprender a programar desde cero XXVI* (KeepCoding).

Aplicación web para buscar películas por título y año, ver su detalle,
dejar comentarios y calificarlas de 1 a 5 estrellas. Los datos de las películas
vienen de la API externa [OMDb](https://www.omdbapi.com/).

## Tecnologías

- **Back-end:** Python 3 + FastAPI + SQLite
- **Front-end:** HTML + CSS + Bootstrap 5 + JavaScript
- **Arquitectura:** MVC (modelo, vista, controlador)
- **Tests:** pytest

## Estructura del proyecto

```
├── main.py                     # Arranca la aplicación (empieza por aquí)
├── config.py                   # Configuración: API key, rutas, base de datos
├── requirements.txt            # Librerías necesarias
├── .env.example                # Plantilla para la API key
├── app/
│   ├── database.py             # Conexión con SQLite y creación de tablas
│   ├── errors.py               # Control de errores
│   ├── schemas.py              # Validación de los datos que envía el usuario
│   ├── models/                 # MODELO: acceso a datos
│   │   ├── movie_model.py      #   películas (API OMDb)
│   │   ├── comment_model.py    #   comentarios (tabla Comentario)
│   │   └── rating_model.py     #   calificaciones (tabla Calificacion)
│   └── controllers/            # CONTROLADOR: rutas de la API
│       ├── movie_controller.py
│       ├── comment_controller.py
│       ├── rating_controller.py
│       └── view_controller.py  #   sirve las páginas HTML
├── views/                      # VISTA: HTML, CSS y JavaScript
│   ├── index.html              #   página de búsqueda
│   ├── detalle.html            #   página de detalle
│   ├── css/estilos.css
│   └── js/
│       ├── comun.js            #   funciones compartidas
│       ├── busqueda.js
│       └── detalle.js
└── tests/                      # Tests automáticos
    ├── conftest.py             #   preparación (BD temporal y OMDb falso)
    ├── test_movies.py
    ├── test_comments.py
    └── test_ratings.py
```

## Instalación

### 1. Clonar el repositorio y entrar en la carpeta

```bash
git clone <url-del-repositorio>
cd jean_proyecto
```

### 2. Crear y activar el entorno virtual

En macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

En Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar las librerías

```bash
pip install -r requirements.txt
```

### 4. Configurar la API key de OMDb

1. Pide una API key gratuita en <https://www.omdbapi.com/apikey.aspx> (llega por correo).
2. Copia el fichero `.env.example` con el nombre `.env`:

   ```bash
   cp .env.example .env
   ```

3. Abre `.env` y sustituye `pon_aqui_tu_api_key` por tu clave.

### 5. Base de datos

No hay que hacer nada: el fichero `peliculas.db` se crea solo, con sus dos tablas,
la primera vez que arranca la aplicación (ver `app/database.py`).

## Arrancar la aplicación

```bash
uvicorn main:app --reload
```

Después abre en el navegador:

- <http://127.0.0.1:8000> → aplicación web
- <http://127.0.0.1:8000/docs> → documentación automática de la API

En Visual Studio Code también puedes pulsar **F5** y elegir *Levantar API (uvicorn)*.

## Ejecutar los tests

```bash
pytest tests -v
```

Los tests usan una base de datos temporal y una versión falsa de OMDb,
así que no necesitan Internet ni API key.

## Rutas de la API

| Método | Ruta | Qué hace |
|--------|------|----------|
| GET | `/api/peliculas/buscar?titulo=...&anio=...` | Busca películas por título (el año es un filtro opcional) |
| GET | `/api/peliculas/{id}` | Detalle de una película |
| GET | `/api/peliculas/{id}/comentarios` | Lista los comentarios de una película |
| POST | `/api/peliculas/{id}/comentarios` | Guarda un comentario |
| GET | `/api/peliculas/{id}/calificaciones` | Promedio de calificaciones |
| POST | `/api/peliculas/{id}/calificaciones` | Guarda una calificación (1 a 5) |

### Notas sobre OMDb

- OMDb exige siempre un título para buscar; el año solo filtra los resultados.
  Por eso el título es obligatorio y el año opcional.
- OMDb devuelve los textos (sinopsis, género) únicamente en inglés; no tiene opción de idioma.

## Base de datos

Dos tablas en SQLite, tal y como pide el enunciado:

- **Comentario:** `id`, `id_pelicula`, `persona`, `comentario`, `fecha`
- **Calificacion:** `id`, `id_pelicula`, `persona`, `calificacion`, `fecha` (opcional)

`id_pelicula` guarda el id de OMDb como número: el id `tt0133093` se guarda como `133093`.

## Control de errores

| Situación | Código HTTP |
|-----------|-------------|
| Título vacío o año mal escrito | 400 |
| Película no encontrada | 404 |
| Datos del formulario no válidos (nombre vacío, calificación fuera de 1-5...) | 422 |
| Error en la base de datos | 500 |
| OMDb no responde o falta la API key | 502 |

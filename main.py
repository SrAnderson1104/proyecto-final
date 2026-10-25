"""
========================================================================
 PROYECTO FINAL - Bootcamp "Aprender a programar desde cero XXVI"
========================================================================

Aplicación web para buscar películas (por título y año), ver su detalle,
dejar comentarios y calificarlas de 1 a 5 estrellas.

Tecnologías: Python + FastAPI + SQLite + HTML/CSS/Bootstrap/JavaScript.
Datos de películas: API externa OMDb (https://www.omdbapi.com/).

Arquitectura MVC ("divide y vencerás": cada fichero hace una sola cosa):

    main.py                 -> arranca la aplicación y conecta todas las piezas
    config.py               -> configuración (API key, rutas, base de datos)
    app/database.py         -> conexión con SQLite y creación de tablas
    app/errors.py           -> control de errores
    app/schemas.py          -> validación de los datos que envía el usuario
    app/models/             -> MODELO: acceso a datos (OMDb y SQLite)
        movie_model.py      -> películas (API OMDb)
        comment_model.py    -> comentarios (tabla Comentario)
        rating_model.py     -> calificaciones (tabla Calificacion)
    app/controllers/        -> CONTROLADOR: rutas de la API
        movie_controller.py
        comment_controller.py
        rating_controller.py
        view_controller.py  -> sirve las páginas HTML
    views/                  -> VISTA: HTML, CSS y JavaScript
    tests/                  -> tests automáticos (pytest)

Cómo arrancar la API (desde la carpeta del proyecto, con el entorno virtual activo):

    uvicorn main:app --reload

Después abre en el navegador:
    http://127.0.0.1:8000          -> aplicación web
    http://127.0.0.1:8000/docs     -> documentación automática de la API
========================================================================
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import config
from app.controllers import comment_controller, movie_controller, rating_controller, view_controller
from app.database import create_tables
from app.errors import register_error_handlers


def create_app():
    """Crea y configura la aplicación FastAPI paso a paso."""

    # 1. Creamos la aplicación
    app = FastAPI(
        title="Buscador de películas",
        description="Proyecto final del bootcamp: búsqueda de películas con OMDb, comentarios y calificaciones.",
        version="1.0.0",
    )

    # 2. Registramos el control de errores
    register_error_handlers(app)

    # 3. Conectamos las rutas de cada controlador
    app.include_router(movie_controller.router)
    app.include_router(comment_controller.router)
    app.include_router(rating_controller.router)
    app.include_router(view_controller.router)

    # 4. Publicamos los ficheros estáticos (CSS y JavaScript) en /static
    app.mount("/static", StaticFiles(directory=config.VIEWS_DIR), name="static")

    # 5. Creamos las tablas de la base de datos si no existen
    create_tables()

    return app


# Esta es la variable que usa uvicorn: "uvicorn main:app"
app = create_app()

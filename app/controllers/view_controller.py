"""
CONTROLADOR de vistas.

Sirve las páginas HTML del front-end (la de búsqueda y la de detalle).
El contenido de las páginas lo rellena el JavaScript llamando a la API.
"""

import os

from fastapi import APIRouter
from fastapi.responses import FileResponse

import config

router = APIRouter(tags=["Vistas"])


@router.get("/")
def home_page():
    """Página principal: buscador de películas."""
    return FileResponse(os.path.join(config.VIEWS_DIR, "index.html"))


@router.get("/favicon.ico")
def favicon():
    """Icono de la pestaña del navegador (el navegador lo pide solo)."""
    return FileResponse(os.path.join(config.VIEWS_DIR, "favicon.svg"), media_type="image/svg+xml")


@router.get("/pelicula/{movie_id}")
def detail_page(movie_id: int):
    """Página de detalle de una película (comentarios y calificaciones)."""
    return FileResponse(os.path.join(config.VIEWS_DIR, "detalle.html"))

"""
CONTROLADOR de calificaciones (funcionalidad opcional).

Rutas para calificar una película y consultar su promedio.
Las rutas empiezan por /api/peliculas/{movie_id}/calificaciones.
"""

from fastapi import APIRouter

from app.models import rating_model
from app.schemas import RatingInput

router = APIRouter(prefix="/api/peliculas/{movie_id}/calificaciones", tags=["Calificaciones"])


@router.get("")
def get_rating_summary(movie_id: int):
    """Devuelve el promedio de calificaciones de la película y cuántas tiene."""
    summary = rating_model.get_rating_summary(movie_id)

    return summary


@router.post("", status_code=201)
def create_rating(movie_id: int, rating_input: RatingInput):
    """Guarda una calificación nueva (de 1 a 5) en la película."""
    new_rating = rating_model.create_rating(
        movie_id,
        rating_input.persona.strip(),
        rating_input.calificacion,
    )

    return new_rating

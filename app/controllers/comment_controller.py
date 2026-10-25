"""
CONTROLADOR de comentarios.

Rutas para leer y crear comentarios de una película.
Las rutas empiezan por /api/peliculas/{movie_id}/comentarios.
"""

from fastapi import APIRouter

from app.models import comment_model
from app.schemas import CommentInput

router = APIRouter(prefix="/api/peliculas/{movie_id}/comentarios", tags=["Comentarios"])


@router.get("")
def get_comments(movie_id: int):
    """Devuelve todos los comentarios de la película."""
    comments = comment_model.get_comments_by_movie(movie_id)

    return {"total": len(comments), "comentarios": comments}


@router.post("", status_code=201)
def create_comment(movie_id: int, comment_input: CommentInput):
    """Guarda un comentario nuevo en la película."""
    new_comment = comment_model.create_comment(
        movie_id,
        comment_input.persona.strip(),
        comment_input.comentario.strip(),
    )

    return new_comment

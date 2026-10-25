"""
Esquemas de datos de entrada.

Describen qué datos esperamos recibir cuando el usuario envía un formulario.
FastAPI los usa para comprobar automáticamente que los datos son correctos
(por ejemplo, que la calificación está entre 1 y 5).
"""

from pydantic import BaseModel, Field


class CommentInput(BaseModel):
    """Datos para crear un comentario."""
    persona: str = Field(min_length=1, max_length=50)
    comentario: str = Field(min_length=1, max_length=500)


class RatingInput(BaseModel):
    """Datos para crear una calificación."""
    persona: str = Field(min_length=1, max_length=50)
    calificacion: int = Field(ge=1, le=5)  # ge = mayor o igual, le = menor o igual

"""
Control de errores de la aplicación.

1. Definimos nuestros propios tipos de error (excepciones).
2. Definimos qué respuesta devuelve la API cuando ocurre cada error.
3. Registramos esas respuestas en la aplicación FastAPI.

Así, en el resto del código solo tenemos que hacer "raise MovieNotFoundError(...)"
y la API responderá sola con el código HTTP correcto.
"""

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


# ---------- 1. Nuestros tipos de error ----------

class InvalidDataError(Exception):
    """Los datos que ha enviado el usuario no son correctos (HTTP 400)."""


class MovieNotFoundError(Exception):
    """OMDb no ha encontrado la película (HTTP 404)."""


class ExternalApiError(Exception):
    """Ha fallado la comunicación con OMDb (HTTP 502)."""


class DatabaseError(Exception):
    """Ha fallado algo al leer o guardar en la base de datos (HTTP 500)."""


# ---------- 2. Respuesta para cada error ----------

def build_error_response(status_code, message):
    """Crea la respuesta JSON de error. Siempre con el mismo formato: {"detail": "mensaje"}."""
    return JSONResponse(status_code=status_code, content={"detail": message})


def handle_invalid_data(request, error):
    return build_error_response(400, str(error))


def handle_movie_not_found(request, error):
    return build_error_response(404, str(error))


def handle_external_api_error(request, error):
    return build_error_response(502, str(error))


def handle_database_error(request, error):
    return build_error_response(500, str(error))


def handle_validation_error(request, error):
    """
    FastAPI lanza este error cuando los datos no cumplen las reglas
    (por ejemplo, una calificación de 7). Lo convertimos en un mensaje sencillo.
    """
    messages = []
    for problem in error.errors():
        field_name = problem["loc"][-1]
        messages.append(f"{field_name}: {problem['msg']}")

    message = "Los datos enviados no son válidos. " + " | ".join(messages)
    return build_error_response(422, message)


# ---------- 3. Registro en la aplicación ----------

def register_error_handlers(app):
    """Le dice a FastAPI qué función usar para cada tipo de error."""
    app.add_exception_handler(InvalidDataError, handle_invalid_data)
    app.add_exception_handler(MovieNotFoundError, handle_movie_not_found)
    app.add_exception_handler(ExternalApiError, handle_external_api_error)
    app.add_exception_handler(DatabaseError, handle_database_error)
    app.add_exception_handler(RequestValidationError, handle_validation_error)

"""
MODELO de películas.

Este módulo se encarga de hablar con la API externa OMDb.
No sabe nada de HTTP de nuestra API ni de las vistas: solo pide datos y los devuelve.
"""

import requests

import config
from app.errors import ExternalApiError, InvalidDataError, MovieNotFoundError


def imdb_id_to_number(imdb_id):
    """
    Convierte el id de OMDb en un número entero.
    OMDb usa ids como "tt0133093"; el enunciado pide guardar id_pelicula como int,
    así que quitamos el prefijo "tt" y nos quedamos con el número: 133093.
    """
    if not imdb_id.startswith("tt"):
        raise InvalidDataError(f"El id de película '{imdb_id}' no es válido")

    number_part = imdb_id[2:]

    if not number_part.isdigit():
        raise InvalidDataError(f"El id de película '{imdb_id}' no es válido")

    return int(number_part)


def number_to_imdb_id(number):
    """Hace lo contrario: 133093 -> "tt0133093". OMDb usa 7 dígitos como mínimo."""
    return "tt" + str(number).zfill(7)


def call_omdb(params):
    """
    Hace la petición a OMDb y devuelve la respuesta como diccionario.
    Todos los demás métodos pasan por aquí, así el control de errores está en un solo sitio.
    """
    if config.OMDB_API_KEY == "":
        raise ExternalApiError("Falta la API key de OMDb. Revisa el fichero .env")

    # Añadimos la api key a los parámetros de la petición
    params["apikey"] = config.OMDB_API_KEY

    try:
        response = requests.get(config.OMDB_URL, params=params, timeout=config.REQUEST_TIMEOUT)
    except requests.RequestException:
        raise ExternalApiError("No se ha podido conectar con OMDb")

    if response.status_code != 200:
        raise ExternalApiError(f"OMDb ha respondido con el código {response.status_code}")

    try:
        data = response.json()
    except ValueError:
        raise ExternalApiError("OMDb ha devuelto una respuesta que no es JSON")

    return data


def build_movie_from_search_item(item):
    """Convierte un resultado de búsqueda de OMDb en nuestro formato de película."""
    return {
        "id_pelicula": imdb_id_to_number(item["imdbID"]),
        "imdb_id": item["imdbID"],
        "titulo": item.get("Title", ""),
        "anio": item.get("Year", ""),
        "tipo": item.get("Type", ""),
        "poster": item.get("Poster", ""),
    }


def search_movies(title, year=None):
    """
    Busca películas por título y, opcionalmente, por año.
    Devuelve una lista de películas (puede estar vacía).
    """
    params = {"s": title}

    if year is not None:
        params["y"] = year

    data = call_omdb(params)

    # OMDb devuelve Response "False" cuando no encuentra nada
    if data.get("Response") == "False":
        return []

    movies = []
    for item in data.get("Search", []):
        movies.append(build_movie_from_search_item(item))

    return movies


def get_movie_detail(movie_id):
    """Devuelve el detalle de una película a partir de su id numérico."""
    imdb_id = number_to_imdb_id(movie_id)

    data = call_omdb({"i": imdb_id, "plot": "full"})

    if data.get("Response") == "False":
        raise MovieNotFoundError(f"No se ha encontrado la película con id {movie_id}")

    movie = {
        "id_pelicula": movie_id,
        "imdb_id": imdb_id,
        "titulo": data.get("Title", ""),
        "anio": data.get("Year", ""),
        "duracion": data.get("Runtime", ""),
        "genero": data.get("Genre", ""),
        "director": data.get("Director", ""),
        "actores": data.get("Actors", ""),
        "sinopsis": data.get("Plot", ""),
        "poster": data.get("Poster", ""),
        "puntuacion_imdb": data.get("imdbRating", ""),
    }

    return movie

"""
Tests de comentarios: crear, listar y control de errores.
"""

from datetime import date


def test_comments_empty_at_start(client):
    response = client.get("/api/peliculas/133093/comentarios")

    assert response.status_code == 200
    assert response.json()["total"] == 0


def test_create_comment(client):
    new_comment = {"persona": "Ana", "comentario": "Muy buena película"}

    response = client.post("/api/peliculas/133093/comentarios", json=new_comment)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["id_pelicula"] == 133093
    assert data["persona"] == "Ana"
    assert data["comentario"] == "Muy buena película"
    assert data["fecha"] == date.today().isoformat()


def test_comments_are_listed_after_creating(client):
    client.post("/api/peliculas/133093/comentarios", json={"persona": "Ana", "comentario": "Primero"})
    client.post("/api/peliculas/133093/comentarios", json={"persona": "Luis", "comentario": "Segundo"})

    response = client.get("/api/peliculas/133093/comentarios")

    assert response.json()["total"] == 2
    # El más reciente sale primero
    assert response.json()["comentarios"][0]["comentario"] == "Segundo"


def test_comments_are_separated_by_movie(client):
    client.post("/api/peliculas/133093/comentarios", json={"persona": "Ana", "comentario": "De Matrix"})
    client.post("/api/peliculas/234215/comentarios", json={"persona": "Ana", "comentario": "De Reloaded"})

    response = client.get("/api/peliculas/133093/comentarios")

    assert response.json()["total"] == 1
    assert response.json()["comentarios"][0]["comentario"] == "De Matrix"


def test_create_comment_with_empty_name_returns_422(client):
    response = client.post("/api/peliculas/133093/comentarios", json={"persona": "", "comentario": "Hola"})

    assert response.status_code == 422
    assert "persona" in response.json()["detail"]


def test_create_comment_without_text_returns_422(client):
    response = client.post("/api/peliculas/133093/comentarios", json={"persona": "Ana"})

    assert response.status_code == 422
    assert "comentario" in response.json()["detail"]

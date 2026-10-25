"""
Tests de calificaciones: crear, promedio y control de errores.
"""


def test_rating_summary_empty_at_start(client):
    response = client.get("/api/peliculas/133093/calificaciones")

    assert response.status_code == 200
    assert response.json()["promedio"] == 0
    assert response.json()["total"] == 0


def test_create_rating(client):
    response = client.post("/api/peliculas/133093/calificaciones", json={"persona": "Ana", "calificacion": 4})

    assert response.status_code == 201
    data = response.json()
    assert data["id_pelicula"] == 133093
    assert data["calificacion"] == 4


def test_rating_average_is_calculated(client):
    client.post("/api/peliculas/133093/calificaciones", json={"persona": "Ana", "calificacion": 5})
    client.post("/api/peliculas/133093/calificaciones", json={"persona": "Luis", "calificacion": 4})
    client.post("/api/peliculas/133093/calificaciones", json={"persona": "Eva", "calificacion": 3})

    response = client.get("/api/peliculas/133093/calificaciones")

    assert response.json()["promedio"] == 4.0
    assert response.json()["total"] == 3


def test_rating_above_5_returns_422(client):
    response = client.post("/api/peliculas/133093/calificaciones", json={"persona": "Ana", "calificacion": 7})

    assert response.status_code == 422
    assert "calificacion" in response.json()["detail"]


def test_rating_below_1_returns_422(client):
    response = client.post("/api/peliculas/133093/calificaciones", json={"persona": "Ana", "calificacion": 0})

    assert response.status_code == 422


def test_rating_with_text_value_returns_422(client):
    response = client.post("/api/peliculas/133093/calificaciones", json={"persona": "Ana", "calificacion": "cinco"})

    assert response.status_code == 422

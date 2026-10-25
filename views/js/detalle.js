/*
 * JavaScript de la página de detalle (detalle.html).
 *
 * Al cargar la página:
 *   1. Sacamos el id de la película de la URL (/pelicula/133093 -> 133093)
 *   2. Cargamos el detalle, los comentarios y la calificación
 * Después escuchamos los formularios de comentar y calificar.
 */

// Sacamos el id de la URL: "/pelicula/133093" -> ["", "pelicula", "133093"]
const partesUrl = window.location.pathname.split("/");
const idPelicula = partesUrl[2];

const zonaDetalle = document.getElementById("detalle");
const zonaEstrellas = document.getElementById("estrellas");
const resumenCalificacion = document.getElementById("resumen-calificacion");
const listaComentarios = document.getElementById("lista-comentarios");
const formularioComentario = document.getElementById("formulario-comentario");
const formularioCalificacion = document.getElementById("formulario-calificacion");


/* ---------- Detalle de la película ---------- */

function mostrarDetalle(pelicula) {
    const poster = obtenerPoster(pelicula.poster);

    zonaDetalle.innerHTML = `
        <div class="row g-0">
            <div class="col-md-4 p-3">
                <img src="${poster}" class="poster-detalle" alt="Póster de ${escaparHtml(pelicula.titulo)}">
            </div>
            <div class="col-md-8">
                <div class="card-body">
                    <h1 class="h3 card-title">${escaparHtml(pelicula.titulo)} (${escaparHtml(pelicula.anio)})</h1>
                    <p class="text-muted">${escaparHtml(pelicula.genero)} · ${escaparHtml(pelicula.duracion)}</p>
                    <p><strong>Director:</strong> ${escaparHtml(pelicula.director)}</p>
                    <p><strong>Reparto:</strong> ${escaparHtml(pelicula.actores)}</p>
                    <p><strong>Puntuación IMDb:</strong> ${escaparHtml(pelicula.puntuacion_imdb)} / 10</p>
                    <p>${escaparHtml(pelicula.sinopsis)}</p>
                </div>
            </div>
        </div>
    `;

    document.title = pelicula.titulo + " - Detalle";
}


async function cargarDetalle() {
    const pelicula = await llamarApi("/api/peliculas/" + idPelicula);
    mostrarDetalle(pelicula);
}


/* ---------- Comentarios ---------- */

function crearComentarioHtml(comentario) {
    return `
        <div class="comentario">
            <strong>${escaparHtml(comentario.persona)}</strong>
            <span class="text-muted small"> · ${escaparHtml(comentario.fecha)}</span>
            <p class="mb-0">${escaparHtml(comentario.comentario)}</p>
        </div>
    `;
}


function mostrarComentarios(comentarios) {
    if (comentarios.length === 0) {
        listaComentarios.innerHTML = '<p class="text-muted">Todavía no hay comentarios. ¡Sé el primero!</p>';
        return;
    }

    listaComentarios.innerHTML = "";

    for (const comentario of comentarios) {
        listaComentarios.innerHTML += crearComentarioHtml(comentario);
    }
}


async function cargarComentarios() {
    const datos = await llamarApi("/api/peliculas/" + idPelicula + "/comentarios");
    mostrarComentarios(datos.comentarios);
}


async function alEnviarComentario(evento) {
    evento.preventDefault();
    ocultarMensaje();

    const persona = document.getElementById("comentario-persona").value.trim();
    const texto = document.getElementById("comentario-texto").value.trim();

    const opciones = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ persona: persona, comentario: texto }),
    };

    try {
        await llamarApi("/api/peliculas/" + idPelicula + "/comentarios", opciones);
        formularioComentario.reset();
        mostrarMensaje("Comentario guardado", "success");
        await cargarComentarios();
    } catch (error) {
        mostrarMensaje(error.message, "danger");
    }
}


/* ---------- Calificaciones (opcional) ---------- */

/* Convierte un promedio (por ejemplo 3.4) en estrellas: ★★★☆☆ */
function crearEstrellas(promedio) {
    const estrellasLlenas = Math.round(promedio);
    let texto = "";

    for (let i = 1; i <= 5; i++) {
        if (i <= estrellasLlenas) {
            texto += "★";
        } else {
            texto += "☆";
        }
    }

    return texto;
}


function mostrarCalificacion(resumen) {
    zonaEstrellas.textContent = crearEstrellas(resumen.promedio);

    if (resumen.total === 0) {
        resumenCalificacion.textContent = "Sin calificaciones todavía";
    } else {
        resumenCalificacion.textContent = "Promedio " + resumen.promedio + " de 5 (" + resumen.total + " votos)";
    }
}


async function cargarCalificacion() {
    const resumen = await llamarApi("/api/peliculas/" + idPelicula + "/calificaciones");
    mostrarCalificacion(resumen);
}


async function alEnviarCalificacion(evento) {
    evento.preventDefault();
    ocultarMensaje();

    const persona = document.getElementById("calificacion-persona").value.trim();
    const valor = Number(document.getElementById("calificacion-valor").value);

    const opciones = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ persona: persona, calificacion: valor }),
    };

    try {
        await llamarApi("/api/peliculas/" + idPelicula + "/calificaciones", opciones);
        formularioCalificacion.reset();
        mostrarMensaje("Calificación guardada", "success");
        await cargarCalificacion();
    } catch (error) {
        mostrarMensaje(error.message, "danger");
    }
}


/* ---------- Arranque de la página ---------- */

async function iniciarPagina() {
    // Cargamos el detalle por un lado: si OMDb falla, los comentarios y
    // la calificación (que están en nuestra base de datos) se cargan igualmente.
    try {
        await cargarDetalle();
    } catch (error) {
        mostrarMensaje(error.message, "danger");
        zonaDetalle.innerHTML = '<div class="card-body"><p class="text-muted mb-0">No se ha podido cargar la película.</p></div>';
    }

    try {
        await cargarComentarios();
        await cargarCalificacion();
    } catch (error) {
        mostrarMensaje(error.message, "danger");
    }
}

formularioComentario.addEventListener("submit", alEnviarComentario);
formularioCalificacion.addEventListener("submit", alEnviarCalificacion);

iniciarPagina();

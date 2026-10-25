/*
 * JavaScript de la página de búsqueda (index.html).
 */

const formularioBusqueda = document.getElementById("formulario-busqueda");
const campoTitulo = document.getElementById("campo-titulo");
const campoAnio = document.getElementById("campo-anio");
const zonaResultados = document.getElementById("resultados");


/* Crea el HTML de una tarjeta de película. */
function crearTarjetaPelicula(pelicula) {
    const poster = obtenerPoster(pelicula.poster);

    return `
        <div class="col-6 col-md-4 col-lg-3">
            <div class="card h-100 shadow-sm tarjeta-pelicula" data-id="${pelicula.id_pelicula}">
                <img src="${poster}" class="card-img-top" alt="Póster de ${escaparHtml(pelicula.titulo)}">
                <div class="card-body">
                    <h2 class="h6 card-title">${escaparHtml(pelicula.titulo)}</h2>
                    <p class="card-text text-muted small mb-0">${escaparHtml(pelicula.anio)}</p>
                </div>
            </div>
        </div>
    `;
}


/* Pinta la lista de películas en la página. */
function mostrarResultados(peliculas) {
    zonaResultados.innerHTML = "";

    if (peliculas.length === 0) {
        mostrarMensaje("No se ha encontrado ninguna película con esos datos", "warning");
        return;
    }

    for (const pelicula of peliculas) {
        zonaResultados.innerHTML += crearTarjetaPelicula(pelicula);
    }

    // Al hacer clic en una tarjeta vamos a la página de detalle
    const tarjetas = document.querySelectorAll(".tarjeta-pelicula");

    for (const tarjeta of tarjetas) {
        tarjeta.addEventListener("click", function () {
            window.location.href = "/pelicula/" + tarjeta.dataset.id;
        });
    }
}


/* Llama a la API para buscar películas. */
async function buscarPeliculas(titulo, anio) {
    const parametros = new URLSearchParams({ titulo: titulo, anio: anio });

    const datos = await llamarApi("/api/peliculas/buscar?" + parametros.toString());

    return datos.peliculas;
}


/* Qué hacemos cuando el usuario envía el formulario. */
async function alEnviarBusqueda(evento) {
    evento.preventDefault();  // Evitamos que la página se recargue
    ocultarMensaje();
    zonaResultados.innerHTML = "";

    const titulo = campoTitulo.value.trim();
    const anio = campoAnio.value.trim();

    try {
        const peliculas = await buscarPeliculas(titulo, anio);
        mostrarResultados(peliculas);
    } catch (error) {
        mostrarMensaje(error.message, "danger");
    }
}


formularioBusqueda.addEventListener("submit", alEnviarBusqueda);

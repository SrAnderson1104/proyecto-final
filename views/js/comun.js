/*
 * Funciones comunes que usan las dos páginas (búsqueda y detalle).
 */

// Imagen que mostramos cuando OMDb no tiene póster
const POSTER_POR_DEFECTO = "https://via.placeholder.com/300x450?text=Sin+poster";


/* Muestra un mensaje al usuario. tipo puede ser "danger" (error), "warning" o "success". */
function mostrarMensaje(texto, tipo) {
    const zonaMensaje = document.getElementById("mensaje");

    zonaMensaje.textContent = texto;
    zonaMensaje.className = "alert alert-" + tipo;
}


/* Oculta el mensaje. */
function ocultarMensaje() {
    const zonaMensaje = document.getElementById("mensaje");

    zonaMensaje.className = "alert d-none";
}


/*
 * Llama a nuestra API y devuelve la respuesta en formato JSON.
 * Si la API responde con error, lanza una excepción con el mensaje del error.
 */
async function llamarApi(url, opciones) {
    const respuesta = await fetch(url, opciones);
    const datos = await respuesta.json();

    if (!respuesta.ok) {
        throw new Error(datos.detail);
    }

    return datos;
}


/* Devuelve el póster de la película o la imagen por defecto si no tiene. */
function obtenerPoster(poster) {
    if (poster === "N/A" || poster === "") {
        return POSTER_POR_DEFECTO;
    }

    return poster;
}


/* Evita que un texto escrito por el usuario se interprete como HTML. */
function escaparHtml(texto) {
    const elemento = document.createElement("div");
    elemento.textContent = texto;

    return elemento.innerHTML;
}

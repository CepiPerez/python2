// Parámetros para la API
const options = {
    method: 'GET',
    headers: {
        accept: 'application/json',
        Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhODViZTJjYWY5MjUzOWVmMDM0NzA1ODFhMWQ1ZTAzMSIsInN1YiI6IjY0ZTY4ZDQyYzYxM2NlMDEwYjhiYzc1ZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.AzcehxudafYj4U2pzKNuWxw8BZLJJFK_sVXO_Bjg6QE'
    }
};



/* 
Llamamos a la API para obtener la lista de películas

Parametros: seccion 
Valores permitidos: now_playing, popular, top_rated, upcoming
 */ 
async function cargarListadoPeliculas(seccion) {
    
    var respuesta = [];

    await fetch('https://api.themoviedb.org/3/movie/' + seccion + '?language=en&page=1', options)
        .then(response => response.json())
        .then(response => respuesta = response.results)
        .catch(err => console.error(err));

    return respuesta;
}


/*
Llamamos a la API para obtener el detalle de la película
Hacemos una segunda llamada para obtener la lista de videos de la misma
Hacemos una tercer llamada para obtener los actores y equipo 

Parametros: ID de la pelicula 
*/
async function cargarDetallePelicula(id) {

    var respuesta = {};

    await fetch('https://api.themoviedb.org/3/movie/' + id + '?language=es-AR', options)
        .then(response => response.json())
        .then(response => respuesta.detalle = response)
        .catch(err => console.error(err));

    await fetch('https://api.themoviedb.org/3/movie/' + id + '/videos?language=es-AR', options)
        .then(response => response.json())
        .then(response => respuesta.videos = response)
        .catch(err => console.error(err));

    await fetch('https://api.themoviedb.org/3/movie/' + id + '/credits?language=es-AR', options)
        .then(response => response.json())
        .then(response => respuesta.reparto = response)
        .catch(err => console.error(err));

    return respuesta;
}

/* 
Llamamos a la API para obtener una coleccion de peliculas (saga)

Parametros: ID de la saga
 */ 
async function cargarColeccionPeliculas(id) {
    
    var respuesta = [];

    await fetch('https://api.themoviedb.org/3/collection/' + id + '?language=es_ar&region=AR', options)
        .then(response => response.json())
        .then(response => respuesta = response)
        .catch(err => console.error(err));

    return respuesta;
}

// Menu hamburguesa
const mainmenu = document.getElementById('mainmenu');
const menucontainer = document.querySelector('.menu-container');
const menucontainershadow = document.querySelector('.menu-container-shadow');

mainmenu.addEventListener('click', toggleMenu, false);
menucontainershadow.addEventListener('click', toggleMenu, false);

function toggleMenu() {
    if (menucontainer.classList.contains('opened')) {
        menucontainer.classList.remove('opened')
    } else {
        menucontainer.classList.add('opened')
    }
}


// Esta funcion solamente limpia la imagen (le saca la barra y la extensión)
function cleanPath(path) {
    return path.replace('/', '').replace('.jpg', '');
}

// Esta funcion agraga un fondo al CSS de un elemento
function agregarFondo(id, value) {
    document.getElementById(id).style.backgroundImage = 'url("' + value + '")';
}

// Esta funcion agraga un atributo a un elemento
function agregarAtributo(id, attr, value) {
    document.getElementById(id).setAttribute(attr, value);
}

// Esta funcion agraga el texto directamente al elemento
function agregarTexto(id, value) {
    document.getElementById(id).innerHTML = value;
}

// Esta funcion busca los géneros en un array y los une en un string
// Si la API no devuelve generos retornamos "no clasificada"
function juntarGeneros(generos) {

    if (generos.length==0) {
        return 'No clasificada';
    }

    var resultado = [];
    
    generos.forEach(genero => {
        resultado.push(genero.name);
    });

    return resultado.join(' - '); 
}

// Esta funcion convierte una fecha al formato local (2023-05-25 a 25-05-2023)
function convertirFecha(fecha) {
    return fecha.substring(8, 10) + '-' + fecha.substring(5, 7) + '-' + fecha.substring(0, 4);
}




/*
Esta funcion genera la lista de películas

Parametros:
- peliculas: JSON con los datos de la API
- main: DIV contenedor para agregar las peliculas

*/
function generarListadoPeliculas(peliculas, main) {

    peliculas.forEach(pelicula => {
        //console.log(pelicula)
        
        var peli = document.createElement('a');
        peli.classList.add('pelicula_caja');
        peli.setAttribute('href', 'detalle.html?id=' + pelicula.id + '&path=' + cleanPath(pelicula.poster_path));
        
        peli.innerHTML = `
            <img class="pelicula_poster" src="https://image.tmdb.org/t/p/w300/` + pelicula.poster_path  + `" alt="" loading="lazy">
            <p class="pelicula_titulo">` + pelicula.original_title + `</p>`;

        var porcentaje = parseInt(pelicula.vote_average * 10);

        var color = porcentaje >= 70 
            ? '#23cf23'
            : porcentaje >= 40 
                ? 'orange' 
                : porcentaje > 0 ? 'red' : '#333';

        
        peli.innerHTML += `<div class="small-percent-container">
            <div class="percent-container" id="circular">
                <div class="percent-box" id="percent-box" style="--i:${porcentaje>0 ? porcentaje : '100'}%; 
                    --clr:${color}">
                    <div class="circle small">
                        <span id="percent-text">${porcentaje>0 ? porcentaje : 'SC'}</span>
                    </div>
                </div>
            </div></div>`;

        main.appendChild(peli);

    });

    // Agregamos cada peli al observer para generar la animacion
    const cards = document.querySelectorAll(".pelicula_caja");
    cards.forEach( card => {
        card.style.transitionDelay = (card.getBoundingClientRect().left / 2) + 'ms'
        observer.observe(card);
    });
}


/* 
Esta funcion carga el detalle de la pelicula

Parametros:
- detalle: JSON con los datos de la API
- calificacion: DIV de la calificacion
- calificacionText: SPAN donde se indica el texto de la calificacion 
- estudios: DIV para agregar la lista de estudios (productoras)
- estudiosTitulo: PARRAFO con el titulo de estudios
- coleccion: DIV contenedor de la coleccion 

*/
function generarDetallePelicula(detalle, calificacion, calificacionText, estudios, estudiosTitulo, coleccion) {

    const urlSearchParams = new URLSearchParams(window.location.search);
    const params = Object.fromEntries(urlSearchParams.entries());

    // Agregamos el fondo usando CSS (background_image) al elemento
    agregarFondo('detalle_pelicula_fondo', 'https://image.tmdb.org/t/p/original/' + 
        (detalle.backdrop_path ? detalle.backdrop_path : detalle.poster_path));
    
    // Agregamos la imagen del póster usando el atributo "src" de la etiqueta "img"
    agregarAtributo('poster', 'src', 'https://image.tmdb.org/t/p/w500/' + params.path + '.jpg');

    // Agregamos el título, incluyendo el año de la pelicula
    agregarTexto('titulo', detalle.original_title 
        + '<span style="font-weight:100;margin-left:.5rem;opacity:.7;">(' 
        + detalle.release_date.substring(0, 4) + ')</span>');

    // Si el nombre original es distinto que el nombre traducido lo mostramos
    // (para evitar mostrar dos titulos iguales)
    if (detalle.original_title != detalle.title) {
        agregarTexto('titulo_traducido', detalle.title);
    }

    // Calculamos el porcentaje de calificación de la película
    // y lo mostramos con una barra circular 
    var porcentaje = parseInt(parseFloat(detalle.vote_average).toFixed(1) * 10);
    
    if (porcentaje > 0) {
        var color = porcentaje >= 70 
            ? '#23cf23'
            : porcentaje >= 40 ? 'orange' : 'red';

        calificacion.setAttribute('style', '--i:' + porcentaje + '%; --clr:' + color);

        calificacionText.innerHTML = porcentaje + '<i>%</i>';
    
        calificacion.classList.add('ranked');
    }

    // Agregamos la fecha de lanzamiento, convertida al formato local
    agregarTexto('fecha', 'Lanzamiento: <b>' + convertirFecha(detalle.release_date) + '</b>');
    
    // Agregamos la lista de generos unificada en un string
    agregarTexto('genero', juntarGeneros(detalle.genres));
    
    // Agregamos el tag de la película
    agregarTexto('tag', detalle.tagline);
    
    // Agregamos la descripción
    agregarTexto('sinopsis', detalle.overview ? detalle.overview : 'No hay una descripción disponible para esta película.');
    
    // Agregamos la calificación en formato decimal (2 digitos)
    agregarTexto('calificacion', 'Calificación: <b>' 
        + (detalle.vote_average > 0 ? detalle.vote_average.toFixed(2) : 'Sin Calificar') + '</b>');
    
    // Calculamos la duración y la mostramos
    // La API devuelve en minutos, así que la cambiamos a hora/minutos 
    var hours = Math.floor(detalle.runtime / 60);          
    var minutes = detalle.runtime % 60;
    agregarTexto('duracion', 'Duración: <b>' + (hours > 0 ? hours + 'h ' : ' ') + minutes + 'm</b>');
    
    // Si la película pertenece a una colección (saga)
    // mostramos una sección con el póster y el nombre 
    // para que se pueda acceder a la misma
    if (detalle.belongs_to_collection) {
        let imagen = detalle.belongs_to_collection.poster_path
            ? detalle.belongs_to_collection.poster_path
            : detalle.belongs_to_collection.backdrop_path
            
        coleccion.innerHTML = `
            <img src="https://image.tmdb.org/t/p/w200/` + imagen 
            + `" alt="" height="180px" width="auto">
            <div>
            <p>Esta película es parte de</p>
            <a href="coleccion.html?id=` + detalle.belongs_to_collection.id 
            + `&path=` + cleanPath(imagen)
            + `">` + detalle.belongs_to_collection.name + `</a>
            </div>`;

        coleccion.style.display = 'flex';
    }

    // Agregamos una lista de las productoras
    detalle.production_companies.forEach(estudio => {
        if (estudio.logo_path) {
            var item = document.createElement('img');
            item.setAttribute('src', 'https://image.tmdb.org/t/p/w200/' + estudio.logo_path);

            estudios.appendChild(item);
        }
    });
    if (estudios.childElementCount > 0) {
        estudiosTitulo.style.display = 'block';
        estudios.style.display = 'flex';
    }

}

/* 
Esta funcion genera la lista de videos disponibles (trailers)

Parametros:
- videos: JSON con los datos de videos
- trailer: DIV para el video principal
- listaVideos: DIV contenedor de la lista del resto de videos

Si no hay datos, el DIV "listaVideos" se va a ocultar
Si hay datos, se agrega cada actor al DIV listaReparto
*/
function generarVideosPelicula(videos, trailer, listaVideos) {

    var trailerLoaded = false;
    var cantidadVideos = 0;

    videos.results.forEach(video => {
        
        // Por ahora solamente si son de youtube
        // (si hay de otra plataforma hay que implementar la generación del link)
        if (video.site=='YouTube') {

            // Si el vídeo es de tipo "Trailer" mostramos directamente un reproductor
            // Solamente se muestra el primero (si hay varios se omite el resto)
            if (video.type=='Trailer' && !trailerLoaded) {
                var w = window.innerWidth;
                w = w > 650 ? 650 : w;
                w = w - (w < 768 ? 40 : 90); 

                var h = parseInt((w / 16) * 9); 

                var item = document.createElement('iframe');
                item.classList.add('pelicula_trailer');
                item.setAttribute('height', h);
                item.setAttribute('width', w);
                item.setAttribute('src', 'https://www.youtube.com/embed/' + video.key);

                trailer.appendChild(item);
                trailerLoaded = true;
                trailer.style.display = 'block';
            }
            // Si el video no es de tipo "Trailer" se agrega a una lista
            // Solamente se agregan los primeros 5 (para evitar una lista larga)
            else {
                var item = document.createElement('a');
                item.classList.add('pelicula_detalle_video');
                item.setAttribute('target', '_blank');
                item.setAttribute('href', 'https://www.youtube.com/watch?v=' + video.key);
                item.innerHTML = video.name;

                if (listaVideos.childElementCount < 6) {
                    listaVideos.appendChild(item);
                    cantidadVideos++;
                }
            }
        }
    });

    if (cantidadVideos==0) {
        listaVideos.style.display = 'none';
    }
}


/* 
Esta funcion genera la lista de protagonistas
Tambien buscamos el director y escritor (ya que son importantes)

Parametros:
- datos: JSON con los datos del reparto
- reparto: DIV contenedor de la lista de reparto
- listaReparto: DIV de la lista
- produccion: DIV contenedor de datos de director/escritor

Si no hay datos, el DIV "reparto" se va a ocultar
Si hay datos, se agrega cada actor al DIV listaReparto
*/
function generarRepartoPelicula(datos, reparto, listaReparto, produccion) {

    var actores = datos.cast;
    var personal = datos.crew;

    // Primero los actores
    // Usamos un contador para mostrar solamente los primeros 5
    var contador = 0;
    actores.some(function(actor) {
        //console.log(actor.name)

        var item = document.createElement('div');

        text = `<div class="pelicula_actor">` 
            + (actor.profile_path ? 
                `<div class="image" style="background-image:url('https://image.tmdb.org/t/p/w200/` 
                + actor.profile_path + `')"></div>`
            : '')
            + `<div class="pelicula_actor_detalle"`
            + (actor.profile_path ? '' : 'style="margin-left:0;"') + `>
                    <div>` + actor.name + `</div><span>` + actor.character + `</span>
                </div>
            </div>`;
        
        item.innerHTML = text;

        listaReparto.appendChild(item);

        contador++;
        return contador==5;
    });

    if (contador>0) {
        reparto.style.display = 'block';
    }


    // Ahora buscamos directores y escritores
    var datos = {};
    personal.forEach(persona => {
        if (persona.job=='Director') {
            datos[persona.name] = datos[persona.name]? datos[persona.name] + ', ' + persona.job : persona.job;
        } else if (persona.job=='Writer') {
            datos[persona.name] = datos[persona.name]? datos[persona.name] + ', ' + persona.job : persona.job;
        }
    });

    for (var key in datos) {
        var value = datos[key];

        var item = document.createElement('div');
        item.classList.add('pelicula_detalle_produccion_item');
        item.innerHTML = `
            <span style="font-weight:600;">` + key + `</span>
            <span style="opacity: .7;">` + value + `</span>
        `;

        produccion.appendChild(item);
    }

}



/*
Esta funcion genera la coleccion de películas (saga)

Parametros:
- coleccion: JSON con los datos de la API
- listado: DIV contenedor para agregar las peliculas

*/
function generarColeccionPeliculas(coleccion, listado) {
    //console.log(coleccion);

    // Agregamos el fondo usando CSS (background_image) al elemento
    agregarFondo('detalle_pelicula_fondo', 'https://image.tmdb.org/t/p/original/' + coleccion.backdrop_path);

    // Agregamos la imagen del póster usando el atributo "src" de la etiqueta "img"
    agregarAtributo('poster', 'src', 'https://image.tmdb.org/t/p/w500/' + params.path + '.jpg');

    // Agregamos el título
    agregarTexto('titulo', coleccion.name);

    // Agregamos la descripción
    agregarTexto('sinopsis', coleccion.overview);

    // Agregamos las películas de la colección al listado HTML
    coleccion.parts.forEach(pelicula => {
        console.log(pelicula)
        
        if (pelicula.poster_path) {
            var peli = document.createElement('a');
            peli.classList.add('pelicula_caja');
        
            peli.setAttribute('href', 'detalle.html?id=' + pelicula.id + '&path=' + cleanPath(pelicula.poster_path));
        
            peli.innerHTML = `
                <img class="pelicula_poster" src="https://image.tmdb.org/t/p/w300/` + pelicula.poster_path  + `" alt="" loading="lazy">
                <p class="pelicula_titulo">` + pelicula.original_title + `</p>`;

            var porcentaje = parseInt(pelicula.vote_average * 10);

            var color = porcentaje >= 70 
                ? '#23cf23'
                : porcentaje >= 40 
                    ? 'orange' 
                    : porcentaje > 0 ? 'red' : '#333';

            
            peli.innerHTML += `<div class="small-percent-container">
                <div class="percent-container" id="circular">
                    <div class="percent-box" id="percent-box" style="--i:${porcentaje>0 ? porcentaje : '100'}%; 
                        --clr:${color}">
                        <div class="circle small">
                            <span id="percent-text">${porcentaje>0 ? porcentaje : 'SC'}</span>
                        </div>
                    </div>
                </div></div>`;

            listado.appendChild(peli);

        }

    });

    // Agregamos cada peli al observer para generar la animacion
    const cards = document.querySelectorAll(".pelicula_caja");
    cards.forEach( card => {
        card.style.transitionDelay = (card.getBoundingClientRect().left) + 'ms'
        observer.observe(card);
    });
}
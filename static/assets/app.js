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



/* 
Esta funcion genera una paginacion

Parametros:
- seccion actual
- pagina actual
- total de paginas
- paginador: DIV contenedor de los botones de paginas
*/
function generarPaginado(seccion, buscar, actual, total) {

    const first = document.getElementById('pagination_first');
    const previous = document.getElementById('pagination_previous');
    const next = document.getElementById('pagination_next');
    const last = document.getElementById('pagination_last');

    var ruta = seccion? "/"+seccion+"/" : "buscar?query="+buscar+"&pagina=";


    if (actual==1) {
        first.classList.add('disabled')
        previous.classList.add('disabled')
    } else {
        first.href = ruta + "1" 
        previous.href = ruta + (parseInt(actual) - 1)
    }

    if (actual==(total-1)) {
        next.classList.add('disabled')
    } else {
        next.href = ruta + (parseInt(actual) + 1)
    }

    if (actual==total) {
        last.classList.add('disabled')
    } else {
        last.href = ruta + total 
    }

}


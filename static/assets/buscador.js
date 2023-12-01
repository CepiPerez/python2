// ----------------------------------------------------
// Buscador con botones de limpiar y buscar
// (C) 2021. Matias Perez para New Rol IT
// ----------------------------------------------------
// form = el id del formulario padre 
// (necesario para poder hacer el submit)
//
// valor = el valor que tiene el buscador 
// (si no se viene de una busqueda deberia estar vacio)
//
// NOTA: Es necesario el custom.css para los iconos
// ----------------------------------------------------

class Buscador extends HTMLElement
{
    constructor() {
        super();

        var myid = this.getAttribute('id') ? this.getAttribute('id') : 'buscador';
        var buscarval = this.getAttribute('valor') ? this.getAttribute('valor') : '';
        var buscarname = this.getAttribute('name') ? this.getAttribute('name') : 'buscar';
        var formulario = document.getElementById(this.getAttribute('form'));
        var fallback = this.getAttribute('fallback');

        this.classList.add("form-group");
        this.setAttribute("id", myid);
    
        var inputtext = document.createElement('input');
        inputtext.classList.add("form-control");
        inputtext.classList.add("text");
        inputtext.setAttribute("placeholder", "Buscar");
        inputtext.setAttribute("name", buscarname);
        inputtext.setAttribute("value", buscarval);
        this.appendChild(inputtext);
    
        var limpiar = document.createElement('a');
        limpiar.classList.add("fa");
        limpiar.classList.add("fa-times-circle");
        limpiar.classList.add("invisible");
        limpiar.setAttribute("id", "limpiar");
        limpiar.setAttribute("href", "");
        this.appendChild(limpiar);
    
        var separador = document.createElement('p');
        separador.classList.add("separator");
        separador.classList.add("invisible");
        separador.innerHTML = "|"
        this.appendChild(separador);
    
        var buscar = document.createElement('a');
        buscar.classList.add("fa");
        buscar.classList.add("fa-search");
        buscar.classList.add("disabled");
        buscar.setAttribute("id", "buscar");
        buscar.setAttribute("href", "");
        this.appendChild(buscar);
    
    
        if (inputtext.value!=="")
        {
            limpiar.classList.remove("invisible");
            separador.classList.remove("invisible");
        }
    
        limpiar.addEventListener("click", function(e) {
            e.preventDefault()
            inputtext.value = '';
            buscar.classList.add("disabled");
            limpiar.classList.add("invisible");
            separador.classList.add("invisible");
            inputtext.focus();

            if (buscarval!=="") {
                window.location.href = fallback
            }
        });

        inputtext.addEventListener('change', function(e) {
            procesarInput()
        })

        inputtext.addEventListener('keyup', function(e) {
            procesarInput()
        })

        inputtext.addEventListener('paste', function(e) {
            procesarInput()
        })
    
        function procesarInput() {
            if (inputtext.value.length==0 && buscarval.length==0) {
              buscar.classList.add("disabled");
              limpiar.classList.add("invisible");
              separador.classList.add("invisible");
            } else {
              buscar.classList.remove("disabled");
              limpiar.classList.remove("invisible");
              separador.classList.remove("invisible");
            }
        }
        
        buscar.addEventListener('click', function(e) {
            e.preventDefault()
            formulario.submit();
        })
    
    }

}

customElements.define('mi-buscador', Buscador);


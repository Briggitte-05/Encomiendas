// static/js/main.js 

document.addEventListener('DOMContentLoaded', function () { 
    // ── Inicializar tooltips de Bootstrap ───────────────────── 
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]'); 
    tooltips.forEach(el => new bootstrap.Tooltip(el)); 

    // ── Auto-cerrar alertas flash despues de 5 segundos ─────── 
    // (complementa la animacion CSS del styles.css) 
    setTimeout(function () { 
        document.querySelectorAll('.alert').forEach(function (alert) { 
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert); 
            if (bsAlert) {
                bsAlert.close(); 
            }
        }); 
    }, 5000); 

    // ── Confirmacion antes de eliminar ──────────────────────── 
    window.confirmar = function (mensaje) { 
        return confirm(mensaje || '¿Estás seguro de realizar esta acción?'); 
    }; 

    // ── Resaltar fila al hacer clic (navegacion intuitiva) ─────── 
    // Se activa en elementos con la clase .fila-link que tengan data-href
    document.querySelectorAll('.fila-link').forEach(function (fila) { 
        fila.style.cursor = 'pointer'; // Cambia el cursor a una mano
        fila.addEventListener('click', function () { 
            if (this.dataset.href) {
                window.location = this.dataset.href; 
            }
        }); 
    });
});
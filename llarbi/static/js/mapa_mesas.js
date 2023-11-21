function mostrarTodasMesas() {
    var mesasElement = document.querySelectorAll('.mesa');
    mesasElement.forEach(function(mesa) {
        mesa.style.display = 'flex';
    });
}

function mostrarMesasOcupadas() {
    var mesasElement = document.querySelectorAll('.mesa');
    mesasElement.forEach(function(mesa) {
        if (mesa.classList.contains('ocupada')) {
            mesa.style.display = 'flex';
        } else {
            mesa.style.display = 'none';
        }
    });
}

function mostrarMesasDesocupadas() {
    var mesasElement = document.querySelectorAll('.mesa');
    mesasElement.forEach(function(mesa) {
        if (mesa.classList.contains('libre')) {
            mesa.style.display = 'flex';
        } else {
            mesa.style.display = 'none';
        }
    });
}

function mostrarDetalleMesa(numeroMesa, gameMode, players, horaInicio) {
    var detalleMesaElement = document.querySelector('.detalle-mesa');
    detalleMesaElement.style.display = 'block';

    var detallesMesaElement = document.createElement('div');
    detallesMesaElement.innerHTML = `
        <h2>Detalles de Mesa ${numeroMesa}</h2>
        <p>Tipo de juego: ${gameMode}</p>
        <p>Número de jugadores: ${players}</p>
        <p>Hora de inicio: ${horaInicio}</p>
        <!-- Agrega más detalles según tus necesidades -->
        <button onclick="cerrarDetalleMesa()">Cerrar Detalle</button>
    `;

    detalleMesaElement.innerHTML = '';
    detalleMesaElement.appendChild(detallesMesaElement);
}

function cerrarDetalleMesa() {
    var detalleMesaElement = document.querySelector('.detalle-mesa');
    detalleMesaElement.style.display = 'none';
}
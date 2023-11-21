let contadorJugador1 = document.getElementById("pj1");
let sumaJugador1 = 0;

let contadorJugador2 = document.getElementById("pj2");
let sumaJugador2 = 0;

let contadorJugador3 = document.getElementById("pj3");
let sumaJugador3 = 0;

let historialBandera = [];
let historial = [];

function incrementJ1(puntos) {
  sumaJugador1 += puntos;
  contadorJugador1.innerText = sumaJugador1;
  historialBandera.push(1);
  historial.push(puntos);
}

function incrementJ2(puntos) {
  sumaJugador2 += puntos;
  contadorJugador2.innerText = sumaJugador2;
  historialBandera.push(2);
  historial.push(puntos);
}

function incrementJ3(puntos) {
  sumaJugador3 += puntos;
  contadorJugador3.innerText = sumaJugador3;
  historialBandera.push(3);
  historial.push(puntos);
}

function undo() {
  if (historialBandera.length > 0) {
    const jugador = historialBandera.pop();
    const puntos = historial.pop();

    switch (jugador) {
      case 1:
        sumaJugador1 -= puntos;
        contadorJugador1.innerText = sumaJugador1;
        break;
      case 2:
        sumaJugador2 -= puntos;
        contadorJugador2.innerText = sumaJugador2;
        break;
      case 3:
        sumaJugador3 -= puntos;
        contadorJugador3.innerText = sumaJugador3;
        break;
    }
  }
}

// Resto del código permanece igual

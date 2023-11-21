let contadorL = document.getElementById("plocal");
let sumaL = 0;
let contadorV = document.getElementById("pvis");  // Agregado: Define el elemento pvis
let sumaV = 0;
let historialBandera = [];
let historial = [];

function incrementJ1(puntos){
  sumaL += puntos;
  contadorL.innerText = sumaL;
  historialBandera.push(1);
  historial.push(puntos);
  console.log(historialBandera.length);
}

function incrementV(puntos){
  sumaV += puntos;
  contadorV.innerText = sumaV;
  historialBandera.push(0);
  historial.push(puntos);
  console.log(historialBandera.length);
}

function newgame(){
  sumaL = 0;
  sumaV = 0;
  historialBandera = [];
  historial = [];
  contadorV.innerText = sumaL;
  contadorL.innerText = sumaV;
}

function undo(){
  if (historialBandera[historialBandera.length - 1] === 1){
    sumaL -= historial[historial.length - 1];
    historialBandera.pop();
    historial.pop();
    contadorL.innerText = sumaL;
  } else if (historialBandera[historialBandera.length - 1] === 0){
    sumaV -= historial[historial.length - 1];
    historialBandera.pop();
    historial.pop();
    contadorV.innerText = sumaV;
  }
}

var startTime = 0;
var timerInterval;

function updateTimer() {
  var elapsedTime = Math.floor((Date.now() - startTime) / 1000);
  var minutes = Math.floor(elapsedTime / 60);
  var seconds = elapsedTime % 60;
  var formattedTime = padNumber(minutes) + ":" + padNumber(seconds);
  document.getElementById("contador").textContent = 'Tiempo restante: ' + minutes + ' minutos, ' + seconds + ' segundos';
}

function padNumber(number) {
  return number.toString().padStart(2, "0");
}

function startGame() {
  startTime = Date.now();
  timerInterval = setInterval(updateTimer, 1000);
}

function endGame() {
  clearInterval(timerInterval);
}

document.addEventListener("DOMContentLoaded", function() {
  startGame();
});

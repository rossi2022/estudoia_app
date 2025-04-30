// frontend/pomodoro.js

let tempo = 25 * 60; // 25 minutos padrão
let intervalo;
let rodando = false;

const tempoEl = document.getElementById("tempoPomodoro");
const iniciarBtn = document.getElementById("iniciarPomodoro");
const pausarBtn = document.getElementById("pausarPomodoro");
const resetarBtn = document.getElementById("resetarPomodoro");

// 🔹 Alarme de fim do ciclo
const audioFim = new Audio("https://www.soundjay.com/buttons/sounds/beep-07.mp3");

function atualizarTempo() {
  const minutos = Math.floor(tempo / 60);
  const segundos = tempo % 60;
  tempoEl.textContent = `${minutos.toString().padStart(2, '0')}:${segundos.toString().padStart(2, '0')}`;
}

function iniciarPomodoro() {
  if (!rodando) {
    intervalo = setInterval(() => {
      if (tempo > 0) {
        tempo--;
        atualizarTempo();
        tempoEl.classList.add("pulse");
        setTimeout(() => tempoEl.classList.remove("pulse"), 200); // animação rápida
      } else {
        clearInterval(intervalo);
        audioFim.play();
        tempoEl.classList.add("tempo-finalizado");
        rodando = false;
        iniciarBtn.classList.remove("ativo");
      }
    }, 1000);
    rodando = true;
    iniciarBtn.classList.add("ativo");
  }
}

function pausarPomodoro() {
  clearInterval(intervalo);
  rodando = false;
  iniciarBtn.classList.remove("ativo");
}

function resetarPomodoro() {
  clearInterval(intervalo);
  tempo = 25 * 60;
  rodando = false;
  atualizarTempo();
  iniciarBtn.classList.remove("ativo");
  tempoEl.classList.remove("tempo-finalizado");
}

// Eventos dos botões
iniciarBtn.addEventListener("click", iniciarPomodoro);
pausarBtn.addEventListener("click", pausarPomodoro);
resetarBtn.addEventListener("click", resetarPomodoro);

// Atualiza o tempo na tela no início
atualizarTempo();


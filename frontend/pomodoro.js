// File: frontend/pomodoro.js

document.addEventListener('DOMContentLoaded', () => {
  const tempoTotal = 25 * 60; // 25 minutos em segundos
  let tempoRestante = tempoTotal;
  let intervalo = null;

  const tempoPomodoro = document.getElementById('tempoPomodoro');
  const iniciarBtn = document.getElementById('iniciarPomodoro');
  const pausarBtn = document.getElementById('pausarPomodoro');
  const resetarBtn = document.getElementById('resetarPomodoro');

  const formatarTempo = (segundos) => {
    const minutos = String(Math.floor(segundos / 60)).padStart(2, '0');
    const segundosRestantes = String(segundos % 60).padStart(2, '0');
    return `${minutos}:${segundosRestantes}`;
  };

  const atualizarDisplay = () => {
    tempoPomodoro.textContent = formatarTempo(tempoRestante);

    if (tempoRestante <= 0) {
      clearInterval(intervalo);
      intervalo = null;
      tempoPomodoro.classList.add('tempo-finalizado');
      iniciarBtn.disabled = true;
      pausarBtn.disabled = true;
      resetarBtn.classList.add('pulse');
    }
  };

  const iniciarPomodoro = () => {
    if (intervalo) return; // Evita múltiplos intervalos
    intervalo = setInterval(() => {
      if (tempoRestante > 0) {
        tempoRestante--;
        atualizarDisplay();
      } else {
        clearInterval(intervalo);
        intervalo = null;
      }
    }, 1000);

    iniciarBtn.classList.add('pulse');
    pausarBtn.classList.remove('pulse');
    resetarBtn.classList.remove('pulse');
  };

  const pausarPomodoro = () => {
    clearInterval(intervalo);
    intervalo = null;

    iniciarBtn.classList.remove('pulse');
    pausarBtn.classList.add('pulse');
  };

  const resetarPomodoro = () => {
    clearInterval(intervalo);
    intervalo = null;
    tempoRestante = tempoTotal;
    tempoPomodoro.classList.remove('tempo-finalizado');
    atualizarDisplay();

    iniciarBtn.disabled = false;
    pausarBtn.disabled = false;

    iniciarBtn.classList.remove('pulse');
    pausarBtn.classList.remove('pulse');
    resetarBtn.classList.remove('pulse');
  };

  // Inicializa o tempo ao abrir a página
  atualizarDisplay();

  // Eventos
  iniciarBtn.addEventListener('click', iniciarPomodoro);
  pausarBtn.addEventListener('click', pausarPomodoro);
  resetarBtn.addEventListener('click', resetarPomodoro);
});




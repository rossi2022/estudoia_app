// File: frontend/scripts/script_estudo_diario.js

// Assume que API_URL e alunoId já estão definidos globalmente no dashboard.html

const btnCheckin = document.getElementById('btn-checkin');
const spanStreak = document.getElementById('seu-streak');

// Função para buscar e exibir o streak atual
async function atualizarStreak() {
  try {
    const res = await fetch(`${API_URL}/modo_estudo/${alunoId}/streak`);
    if (res.status === 404) {
      // Se o endpoint não existir, exibe streak zero
      spanStreak.textContent = '0';
      return;
    }
    if (!res.ok) throw new Error(`Status ${res.status}`);
    const { streak } = await res.json();
    spanStreak.textContent = streak;
  } catch (err) {
    console.error('Erro ao obter streak:', err);
  }
}

// Evento de clique no botão de check-in
btnCheckin.addEventListener('click', async () => {
  try {
    const res = await fetch(`${API_URL}/modo_estudo/${alunoId}/checkin`, {
      method: 'POST'
    });
    if (res.status === 404) {
      // Se não existe rota de check-in, apenas desloga no console
      console.warn('Rota de check-in não encontrada');
      return;
    }
    if (!res.ok) throw new Error(`Status ${res.status}`);
    await atualizarStreak();
  } catch (err) {
    console.error('Erro no check-in de estudo:', err);
  }
});

// Carrega o streak assim que a página for exibida
document.addEventListener('DOMContentLoaded', atualizarStreak);


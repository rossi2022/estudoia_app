// File: frontend/scripts/script_estudo_diario.js

// Assume que API_URL e alunoId já estão definidos globalmente no dashboard.html

const btnCheckin = document.getElementById('btn-checkin');
const spanStreak = document.getElementById('seu-streak');

// 📌 Atualiza o streak atual do aluno
async function atualizarStreak() {
  try {
    const response = await fetch(`${API_URL}/modo_estudo/${alunoId}/streak`);
    if (response.status === 404) {
      spanStreak.textContent = 'Streak: 0 dias';
      return;
    }
    if (!response.ok) throw new Error(`Status ${response.status}`);
    const { streak } = await response.json();
    spanStreak.textContent = `Streak: ${streak} dias`;
  } catch (error) {
    console.error('❌ Erro ao atualizar streak:', error);
  }
}

// 📌 Evento de clique no botão de check-in
btnCheckin?.addEventListener('click', async () => {
  try {
    const response = await fetch(`${API_URL}/modo_estudo/${alunoId}/checkin`, {
      method: 'POST'
    });
    if (response.status === 404) {
      console.warn('⚠️ Rota de check-in não encontrada.');
      return;
    }
    if (!response.ok) throw new Error(`Status ${response.status}`);
    await atualizarStreak();
  } catch (error) {
    console.error('❌ Erro no check-in de estudo:', error);
  }
});

// 📌 Atualiza o streak assim que a página carregar
document.addEventListener('DOMContentLoaded', atualizarStreak);






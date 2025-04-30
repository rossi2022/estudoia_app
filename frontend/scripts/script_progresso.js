// scripts/script_progresso.js
document.addEventListener('DOMContentLoaded', () => {
  const alunoId = localStorage.getItem('aluno_id');
  if (!alunoId) return window.location.href = 'index.html';
  listarProgresso(alunoId);
});

async function listarProgresso(alunoId) {
  console.log('🔍 Fetch /progresso/' + alunoId);
  const resp = await fetch(`${window.location.origin}/progresso/${alunoId}`);
  console.log('Progresso status:', resp.status);
  if (!resp.ok) {
    console.error('Erro ao carregar progresso:', resp.status);
    return;
  }
  const dados = await resp.json();
  // Inicialize seu Chart.js com `dados` aqui
}

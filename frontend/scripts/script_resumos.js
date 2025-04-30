// scripts/script_resumos.js
document.addEventListener('DOMContentLoaded', () => {
  const alunoId = localStorage.getItem('aluno_id');
  if (!alunoId) return location.href = 'index.html';

  listarResumos(alunoId);
});

async function listarResumos(alunoId) {
  const url = `${window.location.origin}/resumos/${alunoId}`;
  console.log('🔍 GET', url);
  const resp = await fetch(url);
  console.log('Resumos status:', resp.status);
  if (!resp.ok) return console.error('Erro ao carregar resumos:', resp.status);
  const resumos = await resp.json();
  const cont = document.getElementById('resumos-container');
  cont.innerHTML = '';
  resumos.forEach(r => {
    const card = document.createElement('div');
    card.className = 'resumo-card';
    card.innerHTML = `<h3>${r.titulo}</h3><p>${r.conteudo}</p>`;
    cont.appendChild(card);
  });
}

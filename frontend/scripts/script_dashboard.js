// scripts/script_dashboard.js
document.addEventListener('DOMContentLoaded', () => {
  const alunoId = localStorage.getItem('aluno_id');
  if (!alunoId) return location.href = 'index.html';

  carregarPerfil(alunoId);
  carregarConquistas(alunoId);
});

async function carregarPerfil(alunoId) {
  const url = `${window.location.origin}/aluno/${alunoId}`;
  console.log('🔍 GET', url);
  const resp = await fetch(url);
  console.log('Perfil status:', resp.status);
  if (!resp.ok) return console.error('Erro ao carregar perfil:', resp.status);
  const aluno = await resp.json();
  document.getElementById('nome').textContent = aluno.nome;
  document.getElementById('email').textContent = aluno.email;
}

async function carregarConquistas(alunoId) {
  const url = `${window.location.origin}/conquistas/${alunoId}`;
  console.log('🔍 GET', url);
  const resp = await fetch(url);
  console.log('Conquistas status:', resp.status);
  if (!resp.ok) return console.error('Erro ao carregar conquistas:', resp.status);
  const conquistas = await resp.json();
  const cont = document.getElementById('conquistas-container');
  cont.innerHTML = '';
  conquistas.forEach(c => {
    const div = document.createElement('div');
    div.className = 'conquista-card';
    div.textContent = c.titulo;
    cont.appendChild(div);
  });
}













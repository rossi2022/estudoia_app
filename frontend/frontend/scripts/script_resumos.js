// Assumindo API_URL e alunoId globais em dashboard.html, mas aqui declaramos:
const API_URL = 'http://127.0.0.1:8000';
const alunoId = 1;

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btn-gerar').addEventListener('click', gerarResumo);
  listarResumos();
});

async function gerarResumo() {
  const texto = document.getElementById('input-texto').value;
  try {
    const res = await fetch(`${API_URL}/resumos/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ aluno_id: alunoId, texto })
    });
    if (!res.ok) throw new Error(`Status ${res.status}`);
    document.getElementById('input-texto').value = '';
    await listarResumos();
  } catch (err) {
    console.error('Erro ao gerar resumo:', err);
  }
}

async function listarResumos() {
  try {
    const res = await fetch(`${API_URL}/resumos/${alunoId}`);
    if (!res.ok) throw new Error(`Status ${res.status}`);
    const resumos = await res.json();
    const ul = document.getElementById('lista-resumos');
    ul.innerHTML = '';
    resumos.forEach(r => {
      const li = document.createElement('li');
      li.textContent = `${new Date(r.data).toLocaleString()}: ${r.conteudo}`;
      ul.appendChild(li);
    });
  } catch (err) {
    console.error('Erro ao listar resumos:', err);
  }
}


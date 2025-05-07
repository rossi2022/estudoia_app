document.addEventListener('DOMContentLoaded', () => {
  const API_URL = window.API_BASE_URL || `${window.location.origin}/api`;
  const alunoId = localStorage.getItem("aluno_id");

  // Proteção: exige login
  if (!alunoId || isNaN(alunoId)) {
    alert("Você precisa estar logado para acessar os resumos.");
    window.location.href = "/";
    return;
  }

  document.getElementById('btn-gerar').addEventListener('click', () => gerarResumo(API_URL, alunoId));
  listarResumos(API_URL, alunoId);
});

async function gerarResumo(API_URL, alunoId) {
  const texto = document.getElementById('input-texto').value;
  try {
    const res = await fetch(`${API_URL}/resumos/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ aluno_id: parseInt(alunoId), texto })
    });
    if (!res.ok) throw new Error(`Status ${res.status}`);
    document.getElementById('input-texto').value = '';
    await listarResumos(API_URL, alunoId);
  } catch (err) {
    console.error('Erro ao gerar resumo:', err);
    alert('Erro ao gerar resumo. Tente novamente.');
  }
}

async function listarResumos(API_URL, alunoId) {
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
    alert('Erro ao carregar resumos.');
  }
}


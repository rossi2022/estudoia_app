// 🔄 Ajuste aqui a porta correta do seu backend
const API_URL = 'http://127.0.0.1:8000';
const alunoId = 1;

document.addEventListener('DOMContentLoaded', () => {
  gerarGraficoProgresso(alunoId);
  popularTabelaProgresso(alunoId);
});

async function gerarGraficoProgresso(id) {
  try {
    const res = await fetch(`${API_URL}/graficos/desempenho/${id}`);
    if (!res.ok) throw new Error(`Status ${res.status}`);
    const { desempenho } = await res.json();
    const materias = Object.keys(desempenho);
    const todasDatas = Array.from(new Set(
      materias.flatMap(m => desempenho[m].map(e => e.data))
    )).sort();
    const datasets = materias.map((mat, i) => ({
      label: mat,
      data: todasDatas.map(d =>
        (desempenho[mat].find(e => e.data === d)?.acertos) || 0
      ),
      borderColor: `hsl(${(i * 60) % 360}, 70%, 50%)`,
      fill: false,
      tension: 0.1
    }));
    const ctx = document.getElementById('graficoProgresso').getContext('2d');
    new Chart(ctx, { type: 'line', data: { labels: todasDatas, datasets } });
  } catch (err) {
    console.error('Erro ao gerar gráfico de progresso:', err);
  }
}

async function popularTabelaProgresso(id) {
  try {
    const res = await fetch(`${API_URL}/progresso/${id}`);
    if (!res.ok) throw new Error(`Status ${res.status}`);
    const progresso = await res.json();
    const tbody = document.getElementById('bodyTabelaProgresso');
    tbody.innerHTML = '';
    Object.entries(progresso).forEach(([data, materias]) => {
      Object.entries(materias).forEach(([mat, nota]) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${new Date(data).toLocaleDateString()}</td>
          <td>${mat}</td>
          <td>${nota}</td>
        `;
        tbody.appendChild(tr);
      });
    });
  } catch (err) {
    console.error('Erro ao popular tabela de progresso:', err);
  }
}


// File: frontend/static/js/script_dashboard.js

document.addEventListener('DOMContentLoaded', async () => {
  const API_BASE_URL = `${window.location.origin}/api`;

  const alunoIdRaw = localStorage.getItem("aluno_id");
  const alunoId = parseInt(alunoIdRaw, 10);
  const token = localStorage.getItem("token");

  if (!alunoIdRaw || isNaN(alunoId) || !token) {
    alert("Você precisa estar logado para acessar o painel.");
    window.location.href = "/";
    return;
  }

  console.log("aluno_id carregado:", alunoId);

  const headersAuth = {
    Authorization: `Bearer ${token}`
  };

  const fetchData = async (url, errorMsg) => {
    const res = await fetch(url, { headers: headersAuth });
    if (!res.ok) throw new Error(errorMsg);
    return await res.json();
  };

  const setElementContent = (id, content) => {
    const el = document.getElementById(id);
    if (el) el.textContent = content;
  };

  const carregarDadosAluno = async () => {
    const aluno = await fetchData(`${API_BASE_URL}/aluno/${alunoId}`, "Erro ao buscar perfil");
    setElementContent('nomeAluno', `Olá, ${aluno.nome}! 👋`);
    const foto = document.getElementById('fotoAluno');
    if (foto) foto.src = aluno.foto_url || "/static/img/default-avatar.png";
    setElementContent('nomeAlunoText', aluno.nome);
    setElementContent('emailAluno', aluno.email);
  };

  const carregarDesempenho = async () => {
    const progresso = await fetchData(`${API_BASE_URL}/progresso/${alunoId}`, "Erro ao buscar progresso");

    new Chart(document.getElementById('graficoDesempenho').getContext('2d'), {
      type: 'bar',
      data: {
        labels: Object.keys(progresso),
        datasets: [{
          label: 'Acertos por Matéria',
          data: Object.values(progresso),
          backgroundColor: 'rgba(54, 162, 235, 0.6)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true, max: 10 }
        }
      }
    });
  };

  const carregarMedalhas = async () => {
    const medalha = await fetchData(`${API_BASE_URL}/recompensas/${alunoId}`, "Erro ao buscar recompensas");
    document.getElementById('medalhasContainer').innerHTML = `
      <div class='medalha'>
        <h3>${medalha.tipo}</h3>
        <p>${medalha.descricao}</p>
      </div>
    `;
  };

  const carregarMaterias = async () => {
    const materias = await fetchData(`${API_BASE_URL}/materias`, "Erro ao buscar matérias");
    const grid = document.getElementById("materiasGrid");
    grid.innerHTML = materias.map(m => `
      <button class="botao-materia" onclick="${m.apostila_url ? `window.open('${m.apostila_url}', '_blank')` : "alert('Apostila não disponível para esta matéria.')"}">
        <img src="/static/img/${m.nome.toLowerCase()}.png" alt="${m.nome}" width="60" />
        <span>${m.nome}</span>
      </button>
    `).join('');
  };

  const carregarLista = async (endpoint, elementId, formatter) => {
    const items = await fetchData(`${API_BASE_URL}/${endpoint}/${alunoId}`, `Erro ao buscar ${endpoint}`);
    const container = document.getElementById(elementId);
    container.innerHTML = items.map(formatter).join('');
  };

  const interacoesDashboard = () => {
    document.querySelectorAll("#btnConcluirMeta, #btnDetalhesResumo").forEach(btn => {
      btn.addEventListener("click", e => {
        e.target.disabled = true;
        e.target.textContent = e.target.id === "btnConcluirMeta" ? "Meta concluída! 🎉" : "Resumo detalhado exibido!";
        e.target.style.backgroundColor = "#4caf50";
        if (e.target.id === "btnDetalhesResumo") {
          document.getElementById("resumoExpandido").innerHTML = `
            <p>📌 Você estudou <strong>3 matérias</strong> hoje.</p>
            <p>✅ Acertou <strong>8 de 10 questões</strong>.</p>
            <p>💡 Revise a matéria com mais erros amanhã.</p>
          `;
          document.getElementById("resumoExpandido").style.display = "block";
        }
      });
    });
  };

  try {
    await Promise.all([
      carregarDadosAluno(),
      carregarDesempenho(),
      carregarMedalhas(),
      carregarMaterias(),
      carregarLista('agenda-provas', 'provasGrid', p => `<li><strong>${p.materia}</strong> - ${p.data_prova} - ${p.descricao}</li>`),
      carregarLista('conquistas', 'listaConquistas', c => `<li>${c.titulo} - ${c.data_conquista}</li>`),
      carregarLista('motivacao/sugestoes', 'sugestoesIA', msg => `<li>${msg}</li>`),
      carregarLista('estudo/diario', 'estudoDiarioContainer', (a, i) => `
        <div class="quiz-card">
          <p class="enunciado"><strong>${i + 1}.</strong> ${a}</p>
          <button class="btn-concluir">✔️ Concluir</button>
        </div>
      `)
    ]);

    interacoesDashboard();
    lucide.createIcons();
  } catch (err) {
    console.error(err);
    alert("Erro ao carregar informações. Tente novamente.");
  }
});























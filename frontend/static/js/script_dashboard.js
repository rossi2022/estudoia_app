// File: frontend/static/js/script_dashboard.js

document.addEventListener('DOMContentLoaded', async () => {
  // Base URL da API
  const API_BASE_URL = window.API_BASE_URL || `${window.location.origin}/api`;

  // Recupera dados de login
  const alunoIdRaw = localStorage.getItem("aluno_id");
  const alunoId = parseInt(alunoIdRaw, 10);
  const token = localStorage.getItem("token");
  const nome = localStorage.getItem("aluno_nome");

  if (!alunoIdRaw || isNaN(alunoId) || !token) {
    alert("Você precisa estar logado para acessar o painel.");
    window.location.href = "/";
    return;
  }

  // Exibe o nome do aluno no cabeçalho
  const nomeAlunoEl = document.getElementById("nome-aluno");
  if (nomeAlunoEl && nome) {
    nomeAlunoEl.textContent = `Olá, ${nome}!`;
  }

  const headersAuth = { Authorization: `Bearer ${token}` };

  // Função genérica para buscar dados e lançar erro em falha
  const fetchData = async (url, errorMsg, useAuth = true) => {
    const opts = {};
    if (useAuth) opts.headers = headersAuth;
    const res = await fetch(url, opts);
    if (!res.ok) throw new Error(errorMsg);
    return res.json();
  };

  // Preenche texto de um elemento
  const setElementContent = (id, content) => {
    const el = document.getElementById(id);
    if (el) el.textContent = content;
  };

  // 1) Dados gerais do aluno
  const carregarDadosAluno = async () => {
    const aluno = await fetchData(
      `${API_BASE_URL}/aluno/${alunoId}`,
      "Erro ao buscar perfil"
    );
    setElementContent('nomeAlunoText', aluno.nome);
    setElementContent('emailAluno', aluno.email);
    const foto = document.getElementById('fotoAluno');
    if (foto) foto.src = aluno.foto_url || "/static/img/default-avatar.png";
  };

  // 2) Gráfico de desempenho (acertos por matéria)
  const carregarDesempenho = async () => {
    const progresso = await fetchData(
      `${API_BASE_URL}/progresso/${alunoId}`,
      "Erro ao buscar progresso"
    );
    const ctx = document.getElementById('graficoDesempenho').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: Object.keys(progresso),
        datasets: [{
          label: 'Acertos por Matéria',
          data: Object.values(progresso)
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  };

  // 3) Medalhas
  const carregarMedalhas = async () => {
    const dados = await fetchData(
      `${API_BASE_URL}/medalhas/${alunoId}`,
      "Erro ao buscar medalhas"
    );
    const container = document.getElementById('listaMedalhas');
    if (!container) return;
    container.innerHTML = dados.medalhas.map(m => `
      <li>
        <strong>${m.titulo}</strong>: ${m.descricao}
        <em>(${m.data_conquista})</em>
      </li>
    `).join('');
  };

  // 4) Matérias e apostilas
  const carregarMaterias = async () => {
    const materias = await fetchData(
      `${API_BASE_URL}/materias`,
      "Erro ao buscar matérias",
      false // rota pública
    );
    const grid = document.getElementById("materiasGrid");
    if (!grid) return;
    grid.innerHTML = materias.map(m => `
      <button class="botao-materia" onclick="
        ${m.apostila_url
          ? `window.open('${m.apostila_url}','_blank')`
          : "alert('Apostila não disponível para esta matéria.')"}
      ">
        <img src="/static/img/${m.nome.toLowerCase()}.png" alt="${m.nome}" width="60"/>
        <span>${m.nome}</span>
      </button>
    `).join('');
  };

  // 5) Função genérica para listas
  const carregarLista = async (endpoint, elementId, tpl) => {
    const items = await fetchData(
      `${API_BASE_URL}/${endpoint}/${alunoId}`,
      `Erro ao buscar ${endpoint}`
    );
    const container = document.getElementById(elementId);
    if (!container) return;
    container.innerHTML = items.map(tpl).join('');
  };

  // 6) Interações de botões (meta, resumo, logout)
  const interacoesDashboard = () => {
    document.getElementById("btnConcluirMeta")?.addEventListener("click", e => {
      e.target.disabled = true;
      e.target.textContent = "Meta concluída! 🎉";
    });

    document.getElementById("btnDetalhesResumo")?.addEventListener("click", e => {
      const resumo = document.getElementById("resumoExpandido");
      resumo.innerHTML = `
        <p>📌 Você estudou <strong>3 matérias</strong> hoje.</p>
        <p>✅ Acertou <strong>8 de 10 questões</strong>.</p>
        <p>💡 Revise a matéria com mais erros amanhã.</p>
      `;
      resumo.style.display = "block";
      e.target.disabled = true;
      e.target.textContent = "Resumo detalhado!";
    });

    document.getElementById("btn-sair")?.addEventListener("click", () => {
      localStorage.clear();
      window.location.href = "/";
    });
  };

  // Executa todas as cargas em paralelo
  try {
    await Promise.all([
      carregarDadosAluno(),
      carregarDesempenho(),
      carregarMedalhas(),
      carregarMaterias(),
      carregarLista('agenda-provas', 'provasGrid',
        p => `<li><strong>${p.materia}</strong> — ${p.data_prova}: ${p.descricao}</li>`
      ),
      carregarLista('conquistas/listar', 'listaConquistas',
        c => `<li>${c.titulo} — ${c.data_conquista}</li>`
      ),
      carregarLista('motivacao/sugestoes', 'sugestoesIA',
        msg => `<li>${msg}</li>`
      ),
      carregarLista('estudo-diario', 'estudoDiarioContainer',
        (a, i) => `
          <div class="quiz-card">
            <p><strong>${i+1}.</strong> ${a}</p>
            <button class="btn-concluir">✔️ Concluir</button>
          </div>
        `
      )
    ]);

    interacoesDashboard();
    lucide.createIcons();
  } catch (err) {
    console.error(err);
    alert("Erro ao carregar informações. Tente novamente.");
  }
});
























document.addEventListener('DOMContentLoaded', async () => {
  const alunoId = localStorage.getItem("aluno_id");
  const nome = localStorage.getItem("nome");

  // Proteção
  if (!alunoId || isNaN(alunoId)) {
    alert("Você precisa estar logado para acessar o painel.");
    window.location.href = "index.html";
    return;
  }

  const carregarDadosAluno = async () => {
    const response = await fetch(`http://127.0.0.1:8000/aluno/${alunoId}`);
    const aluno = await response.json();

    document.getElementById('nomeAluno').textContent = `Olá, ${aluno.nome}! 👋`;
    document.getElementById('fotoAluno').src = aluno.foto_url || "https://via.placeholder.com/120";

    const saudacao = document.createElement('p');
    saudacao.textContent = `Pronto para aprender algo novo hoje? 📘`;
    saudacao.style.fontWeight = 'bold';
    saudacao.style.marginTop = '10px';
    document.querySelector('.perfil').appendChild(saudacao);
  };

  const carregarDesempenho = async () => {
    const response = await fetch(`http://127.0.0.1:8000/progresso/${alunoId}`);
    const progresso = await response.json();

    console.log("📊 Progresso bruto:", progresso);

    let labels, dados;
    if (!Array.isArray(progresso) && typeof progresso === 'object') {
      labels = Object.keys(progresso);
      dados = Object.values(progresso);
    } else if (Array.isArray(progresso)) {
      const dadosAgrupados = {};
      progresso.forEach(item => {
        if (!dadosAgrupados[item.materia]) {
          dadosAgrupados[item.materia] = 0;
        }
        dadosAgrupados[item.materia] += item.acertos;
      });
      labels = Object.keys(dadosAgrupados);
      dados = Object.values(dadosAgrupados);
    } else {
      alert("Formato de dados inesperado no desempenho.");
      return;
    }

    const ctx = document.getElementById('graficoDesempenho').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Acertos por Matéria',
          data: dados,
          backgroundColor: '#4a69bd'
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: true } },
        scales: { y: { beginAtZero: true, max: 10 } }
      }
    });
  };

  const carregarMedalhas = async () => {
    const response = await fetch(`http://127.0.0.1:8000/recompensas/aluno/${alunoId}`);
    const medalhas = await response.json();
    console.log("🏅 Medalhas recebidas:", medalhas);

    if (!Array.isArray(medalhas)) {
      alert("Erro ao carregar medalhas.");
      return;
    }

    const container = document.getElementById('medalhasContainer');
    container.innerHTML = "";

    medalhas.forEach(medalha => {
      const div = document.createElement('div');
      div.className = 'medalha';
      div.innerHTML = `<h3>${medalha.tipo}</h3><p>${medalha.descricao}</p>`;
      container.appendChild(div);
    });
  };

  try {
    await carregarDadosAluno();
    await carregarDesempenho();
    await carregarMedalhas();
  } catch (error) {
    console.error("Erro ao carregar dados:", error);
    alert("Erro ao carregar informações. Tente novamente.");
  }
});







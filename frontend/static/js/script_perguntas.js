// scripts/script_perguntas.js

document.addEventListener('DOMContentLoaded', () => {
    // Protege a rota: só acessa se estiver logado
    const alunoId = localStorage.getItem('aluno_id');
    if (!alunoId) {
      location.href = 'index.html';
      return;
    }
  
    fetchPerguntas();
  });
  
  async function fetchPerguntas() {
    const url = `${window.API_BASE_URL}/perguntas`;
    console.log('🔍 GET', url);
    try {
      const resp = await fetch(url);
      console.log('Status Perguntas:', resp.status);
      if (!resp.ok) {
        console.error('Falha ao buscar perguntas:', resp.status);
        return;
      }
      const perguntas = await resp.json();
      renderPerguntasCards(perguntas);
    } catch (err) {
      console.error('Erro na requisição de perguntas:', err);
    }
  }
  
  function renderPerguntasCards(perguntas) {
    const cont = document.getElementById('perguntas-container');
    cont.innerHTML = '';
    perguntas.forEach(p => {
      const card = document.createElement('div');
      card.className = 'pergunta-card';
      card.innerHTML = `
        <h3>${p.materia}</h3>
        <p><strong>Pergunta:</strong> ${p.enunciado}</p>
        <p><strong>Resposta:</strong> ${p.resposta_correta}</p>
        <p><em>Dificuldade: ${p.dificuldade}</em></p>
      `;
      cont.appendChild(card);
    });
  }
  
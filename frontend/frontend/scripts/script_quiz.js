// scripts/script_quiz.js

document.addEventListener('DOMContentLoaded', () => {
    const alunoId = localStorage.getItem('aluno_id');
    if (!alunoId) return location.href = 'index.html';
  
    montarQuiz();
  });
  
  async function montarQuiz() {
    const container = document.getElementById('quiz-container');
    container.innerHTML = '<p>Carregando pergunta...</p>';
  
    try {
      const resp = await fetch(`${window.API_BASE_URL}/perguntas/aleatoria`);
      if (!resp.ok) throw new Error(`Status ${resp.status}`);
      const p = await resp.json();
  
      container.innerHTML = `
        <div class="quiz-card">
          <h2>${p.materia}</h2>
          <p class="enunciado">${p.enunciado}</p>
          <form id="resposta-form">
            <input type="text" id="resposta-input" placeholder="Sua resposta" required />
            <button type="submit">Enviar</button>
          </form>
          <p id="feedback" class="feedback hidden"></p>
          <button id="next-btn" class="hidden">Próxima</button>
        </div>
      `;
  
      const form = document.getElementById('resposta-form');
      const feedback = document.getElementById('feedback');
      const nextBtn = document.getElementById('next-btn');
      const input = document.getElementById('resposta-input');
  
      form.addEventListener('submit', e => {
        e.preventDefault();
        const user = input.value.trim();
        if (!user) return;
        if (user.toLowerCase() === p.resposta_correta.toLowerCase()) {
          feedback.textContent = '✅ Acertou!';
          feedback.classList.remove('error');
          feedback.classList.add('success');
        } else {
          feedback.textContent = `❌ Errou! Resposta certa: ${p.resposta_correta}`;
          feedback.classList.remove('success');
          feedback.classList.add('error');
        }
        feedback.classList.remove('hidden');
        nextBtn.classList.remove('hidden');
      });
  
      nextBtn.addEventListener('click', () => {
        montarQuiz();
      });
  
    } catch (err) {
      container.innerHTML = `<p>Erro ao carregar quiz: ${err.message}</p>`;
    }
  }
  
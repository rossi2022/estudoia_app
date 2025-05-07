// File: frontend/static/js/script_login.js

document.addEventListener('DOMContentLoaded', () => {
  const loginForm     = document.getElementById('login-form');
  const errorBox      = document.getElementById('login-error');
  const API_BASE_URL  = `${window.location.origin}/api`;

  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorBox.textContent = '';

    const email = document.getElementById('email').value.trim();
    const senha = document.getElementById('senha').value;

    if (!email || !senha) {
      errorBox.textContent = 'Preencha todos os campos.';
      return;
    }

    try {
      const resp = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha })
      });

      let data;
      const contentType = resp.headers.get("content-type") || "";
      if (contentType.includes("application/json")) {
        data = await resp.json();
      } else {
        const text = await resp.text();
        throw new Error(text || 'Erro inesperado no servidor.');
      }

      if (!resp.ok) {
        const errorMessage = data?.detail || 'Erro no login';
        throw new Error(errorMessage);
      }

      const alunoId = parseInt(data.aluno_id, 10);
      if (!alunoId || isNaN(alunoId)) {
        throw new Error("ID do aluno inválido. Tente novamente.");
      }

      localStorage.setItem('token',    data.token);
      localStorage.setItem('aluno_id', alunoId.toString());
      localStorage.setItem('nome',     data.nome);

      // ✅ Redireciona para o painel do aluno
      window.location.href = '/dashboard';
    } catch (err) {
      console.error("Erro no login:", err);
      errorBox.textContent = `Login falhou: ${err.message}`;
    }
  });
});









  
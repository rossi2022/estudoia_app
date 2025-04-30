// scripts/script_login.js

// Executa após o DOM estar completo
document.addEventListener('DOMContentLoaded', () => {
  console.log('%cDOM carregado: anexando listener de login', 'color: green; font-weight: bold;');

  const form = document.getElementById('login-form');
  console.log('Form encontrado:', form);

  if (!form) {
    console.error('❌ #login-form não existe!');
    return;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log('%cEnviando formulário de login...', 'color: blue;');

    const email = form.email.value;
    const senha = form.senha.value;
    console.log('Credenciais:', { email, senha });

    try {
      const resp = await fetch(`${window.location.origin}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha }),
      });
      console.log('Status da resposta:', resp.status);

      const text = await resp.text();
      console.log('Resposta bruta:', text);

      if (!resp.ok) {
        alert(`Login falhou: ${resp.status} — ${text}`);
        return;
      }

      const data = JSON.parse(text);
      console.log('%cLogin bem-sucedido:', 'color: green;', data);

      localStorage.setItem('aluno_id', data.aluno_id);
      localStorage.setItem('nome', data.nome);
      window.location.href = 'dashboard.html';
    } catch (err) {
      console.error('✖ Erro no fetch:', err);
      alert('Erro de conexão ao servidor.');
    }
  });
});






  
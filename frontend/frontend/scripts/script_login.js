// Splash: oculta após 2 segundos
window.addEventListener('load', () => {
  setTimeout(() => {
    document.getElementById('splash').style.display = 'none';
    document.querySelector('.login-container').style.display = 'flex';
  }, 2000);
});

// Lógica de login
document.getElementById('loginForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  const email = document.getElementById('email').value;
  const senha = document.getElementById('senha').value;

  try {
    const response = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, senha }),
    });

    if (!response.ok) throw new Error("Login inválido");

    const data = await response.json();
    localStorage.setItem("aluno_id", data.aluno_id);
    localStorage.setItem("nome", data.nome);
    localStorage.setItem("token", data.token);

    window.location.href = "dashboard.html";
  } catch (error) {
    alert("Erro ao entrar: verifique seu email e senha.");
    console.error("Erro:", error);
  }
});

  
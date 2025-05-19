document.getElementById("login-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const senha = document.getElementById("senha").value;
  // Ajuste automático da base URL (usa a do Fly.io em produção ou a local)
  const API_URL = window.API_BASE_URL || "https://149.248.209.116/api";

  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, senha }),
    });

    const data = await response.json();

    if (response.ok) {
      // Salva token e dados do aluno no navegador
      localStorage.setItem("token", data.token);
      localStorage.setItem("aluno_id", data.aluno_id);
      localStorage.setItem("aluno_nome", data.nome);
      // Redireciona para o painel
      window.location.href = "/dashboard";
    } else {
      // Mostra mensagem de erro específica ou genérica
      const erro = data.detail || data.message || "Falha no login.";
      document.getElementById("login-error").textContent = erro;
    }
  } catch (error) {
    console.error("Erro ao tentar login:", error);
    document.getElementById("login-error").textContent = "Erro de conexão com o servidor.";
  }
});

document.getElementById("login-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const senha = document.getElementById("senha").value;

  try {
    const response = await fetch(window.API_BASE_URL + "/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, senha }),
    });

    const data = await response.json();

    if (response.ok) {
      localStorage.setItem("token", data.token);
      localStorage.setItem("aluno_id", data.aluno_id);
      window.location.href = "/dashboard";
    } else {
      document.getElementById("login-error").textContent = data.detail || "Falha no login.";
    }
  } catch (error) {
    console.error("Erro ao tentar login:", error);
    document.getElementById("login-error").textContent = "Erro de conexão com o servidor.";
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("formLoginProfessor");

  if (!form) {
    console.error("❌ Formulário de login do professor não encontrado.");
    return;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const senha = document.getElementById("senha").value.trim();

    if (!email || !senha) {
      alert("⚠️ Por favor, preencha todos os campos.");
      return;
    }

    try {
      const res = await fetch("/api/professores/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, senha })
      });

      if (!res.ok) {
        const erro = await res.json();
        alert(erro.detail || "❌ Erro ao fazer login.");
        return;
      }

      const dados = await res.json();
      localStorage.setItem("token", dados.token);
      localStorage.setItem("professor_id", dados.professor_id);
      localStorage.setItem("professor_nome", dados.nome);

      window.location.href = "/painel_professor";
    } catch (err) {
      console.error("❌ Erro na requisição de login:", err);
      alert("Erro ao conectar com o servidor. Tente novamente.");
    }
  });
});

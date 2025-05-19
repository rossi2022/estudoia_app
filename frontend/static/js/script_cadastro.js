document.getElementById("formCadastro").addEventListener("submit", async function (e) {
  e.preventDefault();

  const nome = document.getElementById("nome").value.trim();
  const email = document.getElementById("cadastro-email").value.trim();
  const senha = document.getElementById("cadastro-senha").value.trim();
  const foto = document.getElementById("foto").files[0];
  const mensagemErro = document.getElementById("mensagemErro");

  // 🔴 Validação de foto obrigatória
  if (!foto) {
    mensagemErro.textContent = "Por favor, envie uma foto de perfil.";
    return;
  }

  // 🔒 Validação de senha forte
  if (senha.length < 6 || !/\d/.test(senha) || !/[a-zA-Z]/.test(senha)) {
    mensagemErro.textContent = "A senha deve ter no mínimo 6 caracteres, com letras e números.";
    return;
  }

  // 🟢 Se passou, continua
  mensagemErro.textContent = "";

  const formData = new FormData();
  formData.append("nome", nome);
  formData.append("email", email);
  formData.append("senha", senha);
  formData.append("foto", foto);

  try {
    const response = await fetch(`${window.API_BASE_URL}/cadastro`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (response.ok) {
      alert("✅ Cadastro realizado com sucesso!");
      window.location.reload();
    } else {
      mensagemErro.textContent = data.detail || "Erro ao cadastrar.";
    }
  } catch (err) {
    console.error(err);
    mensagemErro.textContent = "Erro de rede ou servidor indisponível.";
  }
});

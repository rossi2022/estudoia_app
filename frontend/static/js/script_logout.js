const logoutBtn = document.getElementById('logout-btn');

if (logoutBtn) {
  logoutBtn.addEventListener('click', () => {
    // 🔐 Remove os dados do aluno armazenados
    localStorage.removeItem('aluno_id');
    localStorage.removeItem('nome');
    localStorage.removeItem('token');

    // 🚪 Redireciona para a página inicial
    window.location.href = '/';
  });
}


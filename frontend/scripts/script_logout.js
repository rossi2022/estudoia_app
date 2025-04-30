const logoutBtn = document.getElementById('logout-btn');
if (logoutBtn) {
  logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('aluno_id');
    localStorage.removeItem('nome');
    window.location.href = 'index.html';
  });
}

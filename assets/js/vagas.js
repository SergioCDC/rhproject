function toggleDescription(id) {
    var description = document.getElementById('vaga-description-' + id);
    if (description.style.display === 'none') {
        description.style.display = 'block';
    } else {
        description.style.display = 'none';
    }
}

function openForm() {
    // Verifica se o usuário está logado
    fetch('/is_logged_in')
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                // Se estiver logado, exibe o modal do formulário
                document.getElementById('inscricaoModal').style.display = 'block';
            } else {
                // Se não estiver logado, redireciona para a página de login
                window.location.href = '/login';
            }
        })
        .catch(error => {
            console.error('Erro ao verificar login:', error);
            window.location.href = '/login'; // Redireciona para a página de login em caso de erro
        });
}

function closeForm() {
    document.getElementById('inscricaoModal').style.display = 'none';
}

// Fecha o modal se o usuário clicar fora dele
window.onclick = function(event) {
    var modal = document.getElementById('inscricaoModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

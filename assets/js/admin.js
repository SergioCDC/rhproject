// document.addEventListener('DOMContentLoaded', function () {
//     const form = document.getElementById('vaga-form');
//     const vagasList = document.querySelector('#vagas-list tbody');

//     form.addEventListener('submit', function (event) {
//         event.preventDefault();

//         // Obter os valores do formulário
//         const titulo = document.getElementById('titulo').value;
//         const descricao = document.getElementById('descricao').value;
//         const requisitos = document.getElementById('requisitos').value;

//         // Cria um novo elemento de linha para a tabela de vagas
//         const novaVaga = document.createElement('tr');
//         novaVaga.innerHTML = `
//             <td>${titulo}</td>
//             <td>${descricao}</td>
//             <td>${requisitos}</td>
//         `;

//         // Adiciona a nova vaga à lista
//         vagasList.appendChild(novaVaga);

//         // Limpa o formulário após o envio
//         form.reset();
//     });
// });

function showEditForm(candidaturaId, nome, email, cpf, curso, vaga, dataCandidatura) {
    // Seleciona a linha correta com base no candidaturaId
    var linha = document.getElementById('linha-' + candidaturaId);

    // Cria o formulário de edição e insere no lugar da linha original
    linha.innerHTML = `
        <td colspan="7">
            <form method="POST" action="/admin/candidatura/${candidaturaId}/editar">
                <div>
                    <label for="nome">Nome:</label>
                    <input type="text" name="nome" value="${nome}" />
                </div>
                <div>
                    <label for="email">Email:</label>
                    <input type="email" name="email" value="${email}" />
                </div>
                <div>
                    <label for="cpf">CPF:</label>
                    <input type="text" name="cpf" value="${cpf}" />
                </div>
                <div>
                    <label for="curso">Curso:</label>
                    <input type="text" name="curso" value="${curso}" />
                </div>
                <div>
                    <label for="vaga">Vaga:</label>
                    <input type="text" name="vaga" value="${vaga}" />
                </div>
                <div>
                    <label for="dataCandidatura">Data da Candidatura:</label>
                    <input type="text" name="dataCandidatura" value="${dataCandidatura}" readonly />
                </div>
                <button type="submit" class="btn btn-primary">Salvar</button>
                <button type="button" class="btn btn-secondary" onclick="location.reload();">Cancelar</button>
            </form>
        </td>
    `;
}

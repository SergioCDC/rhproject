from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from project.models.database import inserir_vaga, listar_vagas, inserir_candidato, verificar_candidato, obter_vaga, atualizar_vaga, deletar_vaga_db, inserir_candidatura,verificar_cpf_existente
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, flash
from project.controllers.inscricao import processar_inscricao
from project.models.database import verificar_candidatura_existente, inserir_candidatura
from config.config import get_db_connection
from project.models.database import atualizar_candidatura
from project.controllers.login import login as login_controller



def register_routes(app):
    # Página inicial (index)
    @app.route('/')
    def index():
        vagas = listar_vagas()
        return render_template('index.html', vagas=vagas)

    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        if request.method == 'POST':
            form_data = request.form
            try:
                candidato_id = processar_inscricao(form_data)
                
                # Armazenar o ID do candidato na sessão
                session['usuario_logado'] = candidato_id
                session['candidato_nome'] = form_data.get('nome')  # Armazena o nome para exibição
                
                flash('Cadastro realizado com sucesso!', 'success')
                return redirect(url_for('vagas_logado'))  # Redireciona para a rota de vagas
            except ValueError as e:
                flash(str(e), 'danger')
                return redirect(url_for('cadastro'))
        return render_template('cadastro.html')


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return login_controller()



    # Recrutador
    @app.route('/recrutador', methods=['GET'])
    def recrutador():
        if not session.get('is_admin') and not session.get('is_recrutador'):
            flash("Acesso negado! Você não tem permissão para acessar esta página.", "danger")
            return redirect(url_for('login'))
        else:
            vagas = listar_vagas()
            return render_template('recrutador.html', vagas=vagas)

    @app.route('/recrutador/processar', methods=['POST'])
    def processar_vaga():
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        requisitos = request.form['requisitos']
        inserir_vaga(titulo, descricao, requisitos)
        return redirect(url_for('recrutador'))

    @app.route('/recrutador/deletar/<int:vaga_id>', methods=['POST'])
    def deletar_vaga(vaga_id):
        deletar_vaga_db(vaga_id)
        return redirect(url_for('recrutador'))

    @app.route('/recrutador/editar/<int:vaga_id>', methods=['GET', 'POST'])
    def editar_vaga(vaga_id):
        if request.method == 'POST':
            titulo = request.form['titulo']
            descricao = request.form['descricao']
            requisitos = request.form['requisitos']
            atualizar_vaga(vaga_id, titulo, descricao, requisitos)
            return redirect(url_for('recrutador'))
        vaga = obter_vaga(vaga_id)
        return render_template('editar_vaga.html', vaga=vaga)

    @app.route('/vagas_logado')
    def vagas_logado():     
        # Se o usuário estiver logado, continuar para a página de vagas
        vagas = listar_vagas()
        return render_template('vagas_logado.html', vagas=vagas)


    @app.route('/inscricao/<int:vaga_id>', methods=['POST'])
    def inscrever(vaga_id):
        print(f"Vaga ID: {vaga_id}")
        print(f"Usuário logado na sessão: {session.get('usuario_logado')}")

        # Verifica se a sessão contém o usuário logado corretamente
        if 'usuario_logado' not in session or session.get('usuario_logado') is None:
            return jsonify({'error': 'Usuário não logado.'}), 403

        candidato_id = session.get('usuario_logado')

        # Verifica se o candidato já se inscreveu para essa vaga
        if verificar_candidatura_existente(candidato_id, vaga_id):
            return jsonify({'error': 'Você já se inscreveu para esta vaga.'}), 400

        # Processa a inscrição
        try:
            inserir_candidatura(candidato_id, vaga_id)
            return jsonify({'success': 'Inscrição realizada com sucesso!'}), 200
        except Exception as e:
            print(f"Erro ao processar inscrição: {e}")
            return jsonify({'error': 'Erro ao processar inscrição.'}), 500



    @app.route('/admin/candidaturas', methods=['GET', 'POST'])
    def admin_candidaturas():
        # Verifica se o usuário logado é um administrador
        if not session.get('is_admin'):
            flash("Acesso negado! Você não tem permissão para acessar esta página.", "danger")
            return redirect(url_for('login'))
    
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        if request.method == 'POST':
            # Verifica se é uma operação de exclusão ou edição
            if 'deletar' in request.form:
                # Deletar candidatura
                candidatura_id = request.form['id']
                query = "DELETE FROM candidaturas WHERE id = %s"
                cursor.execute(query, (candidatura_id,))
                connection.commit()
                flash('Candidatura deletada com sucesso!', 'success')
            
            elif 'editar' in request.form:
                # Editar dados do candidato
                candidato_id = request.form['candidato_id']
                nome = request.form['nome']
                email = request.form['email']
                cpf = request.form['cpf']
                curso = request.form['curso']

                # Atualizar a tabela `candidatos`
                query = """
                UPDATE candidatos
                SET nome = %s, email = %s, cpf = %s, curso = %s
                WHERE id = %s
                """
                cursor.execute(query, (nome, email, cpf, curso, candidato_id))
                connection.commit()
                flash('Candidato atualizado com sucesso!', 'success')

        # Query para listar candidaturas
        query = """
        SELECT 
            candidaturas.id,
            candidatos.id AS candidato_id,
            candidatos.nome AS nome_candidato,
            candidatos.email AS email_candidato,
            candidatos.cpf,
            candidatos.curso,
            vagas.titulo AS titulo_vaga,
            candidaturas.data_candidatura
        FROM candidaturas
        JOIN candidatos ON candidaturas.candidato_id = candidatos.id
        JOIN vagas ON candidaturas.vaga_id = vagas.id
        """
        cursor.execute(query)
        candidaturas = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('admin.html', candidaturas=candidaturas)
    

    @app.route('/candidaturas', methods=['GET'])
    def pesquisa_candidaturas():    
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        # Verifica se o usuário logado é administrador ou recrutador
        if not session.get('is_admin') and not session.get('is_recrutador'):
            flash("Acesso negado! Você não tem permissão para acessar esta página.", "danger")
            return redirect(url_for('login'))

        # Consulta para listar candidaturas
        query_candidaturas = """
        SELECT 
            candidaturas.id,
            candidatos.id AS candidato_id,
            candidatos.nome AS nome_candidato,
            candidatos.email AS email_candidato,
            candidatos.cpf,
            candidatos.curso,
            vagas.titulo AS titulo_vaga,
            candidaturas.data_candidatura
        FROM candidaturas
        JOIN candidatos ON candidaturas.candidato_id = candidatos.id
        JOIN vagas ON candidaturas.vaga_id = vagas.id
        """
        cursor.execute(query_candidaturas)
        candidaturas = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('candidaturas.html', candidaturas=candidaturas)
    
    @app.route('/logout')
    def logout():
        # Limpa a sessão do usuário
        session.clear()
        flash("Você foi deslogado com sucesso!", "success")
        return redirect(url_for('index')) 
    


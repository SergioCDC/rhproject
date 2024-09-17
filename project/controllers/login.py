from flask import render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from project.models.database import get_db_connection

# Lista de e-mails com privilégios de admin e recrutadores
ADMIN_EMAILS = ['sergio@cdcia.com.br']  # Atualize com seus e-mails de administradores
RECRUTADOR_EMAILS = ['sejacf@cfcontabilidade.com']  # Atualize com seus e-mails de recrutadores

def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Verificar se o email existe e pegar o hash da senha do banco
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM candidatos WHERE email = %s"
        cursor.execute(query, (email,))
        usuario = cursor.fetchone()
        cursor.close()
        connection.close()

        if usuario:
            if check_password_hash(usuario['senha'], senha):
                # Salvar o ID do usuário na sessão
                session['usuario_logado'] = usuario['id']  # ID do usuário
                session['usuario'] = usuario['nome']  # Nome do usuário

                # Se o email estiver na lista de admin, redirecionar para a página de admin
                if email in ADMIN_EMAILS:
                    session['is_admin'] = True
                    session['is_recrutador'] = False  # Não é recrutador
                    return redirect(url_for('admin_candidaturas'))
                
                # Se o email estiver na lista de recrutadores, redirecionar para a página de recrutadores
                elif email in RECRUTADOR_EMAILS:
                    session['is_admin'] = False  # Não é administrador
                    session['is_recrutador'] = True  # É recrutador
                    return redirect(url_for('recrutador'))
                
                else:
                    # Usuário comum
                    session['is_admin'] = False
                    session['is_recrutador'] = False  # Não é recrutador
                    return redirect(url_for('vagas_logado'))
            else:
                return render_template('login.html', error="Senha incorreta.")
        else:
            return render_template('login.html', error="Email ou senha incorretos.")
    
    return render_template('login.html')

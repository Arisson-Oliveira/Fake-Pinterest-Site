# Importa funções e módulos necessários do Flask
from flask import render_template, url_for, redirect
# Importa a aplicação Flask, banco de dados e bcrypt do módulo fakepinterest
from fakepinterest import app, database, bcrypt
# Importa funcionalidades de login do Flask-Login
from flask_login import login_required, login_user, logout_user, current_user
# Importa os formulários do módulo fakepinterest.forms
from fakepinterest.forms import FormLogin, FormCriarConta, Form_Foto
# Importa os modelos de dados do módulo fakepinterest.models
from fakepinterest.models import Usuario, Foto
# Importa o módulo os para manipulação de caminhos de arquivos
import os
# Importa a função secure_filename para assegurar que o nome do arquivo seja seguro
from werkzeug.utils import secure_filename

# Define a rota para a homepage, permitindo métodos GET e POST
@app.route("/", methods=["GET", "POST"])
def homepage():
    # Cria uma instância do formulário de login
    formlogin = FormLogin()
    # Verifica se o formulário foi submetido e é válido
    if formlogin.validate_on_submit():
        # Consulta o banco de dados para encontrar o usuário pelo e-mail fornecido
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first() 
        # Verifica se o usuário existe e se a senha está correta
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            # Loga o usuário
            login_user(usuario)
            # Redireciona para o perfil do usuário logado
            return redirect(url_for("perfil", id_usuario=usuario.id))
    # Renderiza o template da homepage, passando o formulário de login
    return render_template("homepage.html", form=formlogin)

# Define a rota para criar uma nova conta, permitindo métodos GET e POST
@app.route("/criarconta", methods=["GET", "POST"])
def criar_conta():
    # Cria uma instância do formulário de criação de conta
    formcriarconta = FormCriarConta()
    # Verifica se o formulário foi submetido e é válido
    if formcriarconta.validate_on_submit():
        # Gera o hash da senha fornecida
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        # Cria um novo usuário com os dados fornecidos
        usuario = Usuario(username=formcriarconta.username.data, senha=senha, email=formcriarconta.email.data)
        # Adiciona o usuário ao banco de dados
        database.session.add(usuario)
        # Confirma a transação no banco de dados
        database.session.commit()
        # Loga o usuário recém-criado
        login_user(usuario, remember=True)
        # Redireciona para o perfil do usuário logado
        return redirect(url_for("perfil", id_usuario=usuario.id))
    # Renderiza o template de criação de conta, passando o formulário de criação de conta
    return render_template("criarconta.html", form=formcriarconta)

# Define a rota para o perfil do usuário, permitindo métodos GET e POST
# A rota requer que o usuário esteja logado
@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    # Verifica se o usuário está visualizando seu próprio perfil
    if int(id_usuario) == int(current_user.id):
        # Cria uma instância do formulário de foto
        form_foto = Form_Foto()
        # Verifica se o formulário de foto foi submetido e é válido
        if form_foto.validate_on_submit():
            # Obtém o arquivo de foto do formulário
            arquivo = form_foto.foto.data
            # Gera um nome seguro para o arquivo
            nome_seguro = secure_filename(arquivo.filename)
            # Define o caminho completo onde o arquivo será salvo
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], nome_seguro)
            # Salva o arquivo na pasta fotos_posts
            arquivo.save(caminho)
            # Cria uma nova instância da classe Foto com os dados fornecidos
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            # Adiciona a nova foto ao banco de dados
            database.session.add(foto)
            # Confirma a transação no banco de dados
            database.session.commit()
        # Renderiza o template do perfil do usuário logado, passando o usuário atual e o formulário de foto
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        # Consulta o banco de dados para encontrar o usuário pelo ID fornecido
        usuario = Usuario.query.get(int(id_usuario))
        # Renderiza o template do perfil do usuário visualizado, passando o usuário e sem formulário de foto
        return render_template("perfil.html", usuario=usuario, form=None)

# Define a rota para logout
# A rota requer que o usuário esteja logado
@app.route("/logout")
@login_required
def logout():
    # Desloga o usuário
    logout_user()
    # Redireciona para a homepage
    return redirect(url_for("homepage"))

# Define a rota para o feed de fotos
@app.route("/feed")
def feed():
    # Consulta o banco de dados para obter todas as fotos, ordenadas pela data de criação em ordem decrescente
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    # Renderiza o template do feed, passando as fotos obtidas
    return render_template("feed.html", fotos=fotos)

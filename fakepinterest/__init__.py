# Importa a classe Flask do módulo flask
from flask import Flask
# Importa a classe SQLAlchemy do módulo flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# Importa a classe LoginManager do módulo flask_login
from flask_login import LoginManager
# Importa a classe Bcrypt do módulo flask_bcrypt para hashing de senhas
from flask_bcrypt import Bcrypt
import os

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Configura a URI do banco de dados SQLite para a aplicação
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# Define a chave secreta para a aplicação Flask, usada para segurança, como em sessões e CSRF
app.config['SECRET_KEY'] = 'ajgdas7d65w67rwueftg7tf87t87'
# Configura a pasta de upload para armazenar as fotos dos posts
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"

# Cria uma instância do SQLAlchemy, passando a aplicação Flask, para manipulação do banco de dados
database = SQLAlchemy(app)
# Cria uma instância do Bcrypt, passando a aplicação Flask, para hashing de senhas
bcrypt = Bcrypt(app)
# Cria uma instância do LoginManager, passando a aplicação Flask, para gerenciamento de logins
login_manager = LoginManager(app)
# Define a página de login padrão para redirecionar usuários não autenticados
login_manager.login_view = "homepage"

# Importa as rotas da aplicação do módulo fakepinterest
from fakepinterest import routes

# Importa o objeto 'database' e 'login_manager' do módulo fakepinterest
from fakepinterest import database, login_manager
# Importa a classe datetime do módulo datetime para manipulação de datas e horas
from datetime import datetime
# Importa a classe UserMixin do módulo flask_login para fornecer implementações padrão para a classe de usuário
from flask_login import UserMixin

# Função para carregar o usuário a partir de seu ID
@login_manager.user_loader
def load_usuario(id_usuario):
    # Consulta o banco de dados para encontrar o usuário pelo ID e retorna o objeto do usuário
    return Usuario.query.get(int(id_usuario))

# Classe que representa a tabela 'Usuario' no banco de dados, herda de database.Model e UserMixin
class Usuario(database.Model, UserMixin):
    # Define a coluna 'id' como chave primária, de tipo inteiro
    id = database.Column(database.Integer, primary_key=True)
    # Define a coluna 'username' como string, não nula
    username = database.Column(database.String, nullable=False)
    # Define a coluna 'email' como string, não nula e única (não pode haver dois usuários com o mesmo e-mail)
    email = database.Column(database.String, nullable=False, unique=True)
    # Define a coluna 'senha' como string, não nula
    senha = database.Column(database.String, nullable=False)
    # Define um relacionamento com a classe 'Foto', backref cria um atributo 'usuario' em 'Foto', lazy carrega os dados sob demanda
    fotos = database.relationship("Foto", backref="usuario", lazy=True)

# Classe que representa a tabela 'Foto' no banco de dados
class Foto(database.Model):
    # Define a coluna 'id' como chave primária, de tipo inteiro
    id = database.Column(database.Integer, primary_key=True)
    # Define a coluna 'imagem' como string, com valor padrão "default.png"
    imagem = database.Column(database.String, default="default.png")
    # Define a coluna 'data_criacao' como DateTime, não nula, com valor padrão da data e hora atual
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    # Define a coluna 'id_usuario' como inteiro, chave estrangeira que referencia a coluna 'id' da tabela 'usuario', não nula
    id_usuario = database.Column(database.Integer, database.ForeignKey("usuario.id"), nullable=False)

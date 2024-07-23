# Importa a classe FlaskForm do módulo flask_wtf, que facilita a criação de formulários no Flask
from flask_wtf import FlaskForm
# Importa os campos de formulário do módulo wtforms
from wtforms import StringField, PasswordField, SubmitField, FileField
# Importa validadores para os campos de formulário do módulo wtforms.validators
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
# Importa o modelo Usuario do módulo fakepinterest.models para validações personalizadas
from fakepinterest.models import Usuario

# Classe de formulário para login, herdando de FlaskForm
class FormLogin(FlaskForm):
    # Campo de e-mail com validadores de presença de dados e formato de e-mail
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    # Campo de senha com validador de presença de dados
    senha = PasswordField("Senha", validators=[DataRequired()])
    # Botão de confirmação para enviar o formulário
    botao_confirmacao = SubmitField("Fazer Login")

    # Método de validação personalizado para verificar se o e-mail existe no banco de dados
    def validate_email(self, email):
        # Consulta o banco de dados para encontrar um usuário com o e-mail fornecido
        usuario = Usuario.query.filter_by(email=email.data).first()
        # Se o usuário não existir, levanta um erro de validação
        if not usuario:
            raise ValidationError("Usuário não existe. Crie uma conta para continuar")

# Classe de formulário para criação de conta, herdando de FlaskForm
class FormCriarConta(FlaskForm):
    # Campo de e-mail com validadores de presença de dados e formato de e-mail
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    # Campo de nome de usuário com validador de presença de dados
    username = StringField('Nome de usuário', validators=[DataRequired()])
    # Campo de senha com validadores de presença de dados e comprimento da senha
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    # Campo de confirmação de senha com validadores de presença de dados e igualdade com o campo de senha
    confirmacao_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("senha")])
    # Botão de confirmação para enviar o formulário
    botao_confirmacao = SubmitField('Criar Conta')

    # Método de validação personalizado para verificar se o e-mail já está cadastrado no banco de dados
    def validate_email(self, email):
        # Consulta o banco de dados para encontrar um usuário com o e-mail fornecido
        usuario = Usuario.query.filter_by(email=email.data).first()
        # Se o usuário já existir, levanta um erro de validação
        if usuario:
            raise ValidationError("E-mail já cadastrado, faça login para continuar")

# Classe de formulário para envio de foto, herdando de FlaskForm
class Form_Foto(FlaskForm):
    # Campo de arquivo para upload de foto com validador de presença de dados
    foto = FileField("Foto", validators=[DataRequired()])
    # Botão de confirmação para enviar o formulário
    botao_confirmacao = SubmitField("Enviar")

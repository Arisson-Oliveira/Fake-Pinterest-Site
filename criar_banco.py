# importa todas as database e a aplicação
from fakepinterest import database, app
from fakepinterest.models import Usuario, Foto

# comando para a criação do banco de dados
with app.app_context():
    database.create_all()
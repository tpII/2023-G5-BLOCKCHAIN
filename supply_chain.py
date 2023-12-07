# Importa la instancia de Flask llamada app
from app import app, db
from app.models import User

# Contexto para flask shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
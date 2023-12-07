# app/__init__.py

# Objeto de Flask
from flask import Flask
# Objeto de configuración
from config import Config
# Configurar CORS
from flask_cors import CORS
# Habilita funcionalidad de socket
import eventlet

# DB ORM
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Manejo de login
from flask_login import LoginManager

# Parchea librerias para que sean compatibles con eventlet
eventlet.monkey_patch()

# Instancia de la clase Flask
app = Flask(__name__)

# CORS para toda la app
CORS(app)

# Seteo la configuración de la app
app.config.from_object(Config)

# Instancia de DB
db = SQLAlchemy(app)
# Instancia del engine de migración
migrate = Migrate(app, db)

# Instancia de LoginManager
login = LoginManager(app)
# Redirige a login si no esta logeado cuando quiere ver endpoints con @login_required
login.login_view = 'login'

# Para solventar circular imports esto va abajo del todo (debido a que el modulo
# routes importa la variable app de este modulo)
# Almacena las rutas de la app
from app import routes, models, mqtt
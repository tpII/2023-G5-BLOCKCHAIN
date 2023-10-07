# app/models.py

from app import db, login
# Hashing de password
from werkzeug.security import generate_password_hash, check_password_hash
# Mixin de clase usuario
from flask_login import UserMixin

# Hereda de UserMixin y db.model, clase base para todos los modelos de sql-alchemy
class User(UserMixin, db.Model):
    # Se puede utilizar un tablename para evitar usar 'user' (palabra reservada postgres)
    __tablename__ = 'supply_chain_user'

    # Campos se crean como instancias de columnas
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # Indica como imprimir objetos de esta clase
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    # Generar hash a traves de password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Permite a flask-login cargar el usuario desde la DB
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))


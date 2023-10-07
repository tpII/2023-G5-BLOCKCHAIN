# app/routes.py

from flask import render_template, flash, redirect, url_for, request
# Importa instancia de app y db
from app import app, db
# Importar clases de formulario
from app.forms import LoginForm, RegistrationForm, AssetForm
# Manejo de usuarios
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
# Manejo de URLs
from werkzeug.urls import url_parse

# Decoradores (modifican la funcion que tienen a continuación)
# Asocian URLs con funciones
# Indice
@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html", title='Home Page')

# Iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Por si un usuario autenticado quiere ir a /login
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # Si el formulario es valido
    if form.validate_on_submit():
        # Busca si existe el username
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o contraseña invalidos')
            return redirect(url_for('login'))
        # Si existe y password correcto
        login_user(user, remember=form.remember_me.data)
        # Redirige a una next_page (si la hay)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

# Cerrar sesión
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Registro de usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    # Si el formulario es valido
    if form.validate_on_submit():
        # Se instancia un usuario
        user = User(username=form.username.data)
        # Se genera una contraseña
        user.set_password(form.password.data)
        # Se agrega a la DB
        db.session.add(user)
        db.session.commit()
        # Mensaje de exito
        flash('El registro fue exitoso!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/new_asset", methods=['GET', 'POST'])
def new_asset():
    form = AssetForm()
    if form.llenar_boton.data and form.validate_on_submit():
        print('APRETASTE LLENAR BOTON')
    if form.enviar_boton.data and form.validate_on_submit():
        print('APRETASTE ENVIAR FORMULARIO')

    return render_template('new_asset.html', form=form)
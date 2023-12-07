# app/routes.py

from datetime import datetime
import json
import os
from flask import render_template, flash, redirect, url_for, request
# Importa instancia de app y db
from app import app, db
# Importar clases de formulario
from app.forms import CreateAssetForm, LoginForm, ReadAssetForm, RegistrationForm, TransferAssetForm, UpdateAssetForm
# Manejo de usuarios
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
# Manejo de URLs
from werkzeug.urls import url_parse

# Manejo de peticiones
import requests

# Obtener organización segun el rol
def get_org():
    if current_user.is_authenticated:
        if current_user.role == "Productor":
            return "Org1MSP"
        elif current_user.role == "Transportador":
            return "Org2MSP"
        else:
            return "Org3MSP"

# Obtener API_KEY segun el rol
def get_api_key():
    if current_user.is_authenticated:
        if current_user.role == "Productor":
            return str(os.environ.get('API_KEY_PRODUCTOR'))
        elif current_user.role == "Transportador":
            return str(os.environ.get('API_KEY_TRANSPORTADOR'))
        else:
           return str(os.environ.get('API_KEY_CLIENTE'))
    else:
       return str(os.environ.get('API_KEY_CLIENTE'))
        
# Decoradores (modifican la funcion que tienen a continuación)
# Asocian URLs con funciones
# Indice
@app.route('/index')
@login_required
def index():
    return render_template("index.html", title='Home Page')

# Iniciar sesión
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Por si un usuario autenticado quiere ir a /login
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # Si el formulario es valido
    if form.validate_on_submit():
        if 'client_login' in request.form:  # Verificar si el botón de acceso como invitado fue presionado
            client_user = User.query.filter_by(username='cliente').first()
            print(client_user)
            if not client_user:
                client_user = User(username='cliente')  
                # Se genera una contraseña
                client_user.set_password('cliente')
                # Se agrega el rol
                client_user.role = "Cliente"
                # Se agrega a la DB
                db.session.add(client_user)
                db.session.commit()

            login_user(client_user)
            print(client_user)
            #next_page = request.args.get('next', url_for('index'))
            return redirect(url_for('index'))
        # Busca si existe el username
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o contraseña invalidos', 'error')
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
    flash('Usted ha cerrado la sesión', 'success')  
    return redirect(url_for('login'))

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
        # Se agrega el rol
        user.role = form.role.data
        # Se agrega a la DB
        db.session.add(user)
        db.session.commit()
        # Mensaje de exito
        flash('El registro fue exitoso!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Creacion/Actualización/Lectura

def handle_success(response):
    respuesta_api = response.json()
    flash(f"Respuesta de la API: {respuesta_api}", 'success')

def handle_job_created(response, headers):
    job_id = response.json()['jobId']
    headers["Content-Type"] = 'text/html'
    url = f"{os.environ.get('API_ADDRESS')}/api/jobs/{job_id}"
    response = requests.get(url, headers=headers)
    print(response.text)
    respuesta_job = response.json()
    print(respuesta_job)

    if "transactionError" in respuesta_job:
        flash(f"Error en la solicitud. {respuesta_job['transactionError']}", 'error')
    else:
        flash("La transacción se envió de forma exitosa", 'success')

def handle_error(response):
    if response.status_code == 401:
        flash("Error: No autorizado. Se requiere autenticación.", 'error')
    elif response.status_code == 403:
        flash("Error: Prohibido. No tienes permisos para acceder a este recurso.", 'error')
    elif response.status_code == 404:
        flash("Error: Recurso no encontrado.", 'error')
    else:
        flash(f"Error en la solicitud. Código: {response.status_code}", 'error')

@app.route("/read_asset", methods=['GET', 'POST'])
def read_asset():
    form = ReadAssetForm()

    if request.method == 'POST' and form.enviar_boton.data and form.validate_on_submit():
        rfid_value = form.rfid_tag.data

        url = f"{os.environ.get('API_ADDRESS')}/api/assets/{rfid_value}"
        headers = {
            "X-api-key": get_api_key(),
        }
        try:
            response = requests.get(url, headers=headers)

            if response is None:
                raise requests.RequestException("No se recibió respuesta.")

            if response.status_code == 200:
                    respuesta_api = response.json()
                    flash(f"Respuesta de la API: {respuesta_api}", 'success')
                    if respuesta_api['Owner']  == "Org1MSP":
                        respuesta_api['Owner'] = "Productor"
                    elif respuesta_api['Owner'] == "Org2MSP":
                        respuesta_api['Owner'] = "Transportador"
                    elif respuesta_api['Owner'] == "Org3MSP":
                        respuesta_api['Owner'] = "Cliente"
                    coordenadas = []
                    coordenadas.append({'latitude': respuesta_api['Latitude'], 'longitude': respuesta_api['Longitude']})
                    return render_template('read_asset.html', form=form, respuesta_api=respuesta_api, coordenadas=coordenadas)
            else:
                handle_error(response)
                return render_template('read_asset.html', title="Read",form=form)

        except requests.RequestException as e:
            flash(f"Error en la solicitud: {e}", 'error')

    return render_template('read_asset.html', form=form)

@app.route("/new_asset", methods=['GET', 'POST'])
def new_asset():
    form = CreateAssetForm()

    if request.method == 'POST' and form.enviar_boton.data and form.validate_on_submit():
        rfid_value = form.rfid_tag.data
        precio = form.precio.data
        bodega = form.bodega.data
        uva = form.uva.data
        cosecha = form.cosecha.data
        temperatura = form.temperatura.data
        humedad = form.humedad.data
        latitud = form.latitud.data
        longitud = form.longitud.data

        url = f"{os.environ.get('API_ADDRESS')}/api/assets"
        headers = {
            "X-api-key": get_api_key(),
        }

        body = {
            "Role": "admin",
            "ID": rfid_value,
            "Price": precio,
            "Winery": bodega,
            "Varietal": uva,
            "Year": cosecha,
            "Temperature": temperatura,
            "Humidity": humedad,
            "Latitude": latitud,
            "Longitude": longitud,
            "Owner": "Org1MSP"
        }

        try:
            response = requests.post(url, json=body, headers=headers)

            if response is None:
                raise requests.RequestException("No se recibió respuesta.")
            
            print(response.json())
            if response.status_code == 200:
                handle_success(response)
            elif response.status_code == 202:
                handle_job_created(response, headers)
            else:
                handle_error(response)

        except requests.RequestException as e:
            print(e)
            flash(f"Error en la solicitud: {e}", 'error')

    return render_template('new_asset.html', form=form)

@app.route("/update_asset/<string:asset_id>", methods=['GET', 'POST'])
def update_asset(asset_id):
    form = UpdateAssetForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Actualiza los campos del activo con los valores del formulario
        url = f"{os.environ.get('API_ADDRESS')}/api/assets/{asset_id}"
        headers = {
            "X-api-key": get_api_key(),
        }

        precio = form.precio.data
        bodega = form.bodega.data
        uva = form.uva.data
        cosecha = form.cosecha.data
        temperatura = form.temperatura.data
        humedad = form.humedad.data
        latitud = form.latitud.data
        longitud = form.longitud.data
        owner = form.owner.data

        body = {
            "Role": "admin",
            "ID": asset_id,
            "Price": precio,
            "Winery": bodega,
            "Varietal": uva,
            "Year": cosecha,
            "Temperature": temperatura,
            "Humidity": humedad,
            "Latitude": latitud,
            "Longitude": longitud,
            "Owner": owner
        }

        try:
            response = requests.put(url, json=body, headers=headers)

            if response is None:
                raise requests.RequestException("No se recibió respuesta.")
            
            if response.status_code == 200:
                handle_success(response)
            elif response.status_code == 202:
                handle_job_created(response, headers)
                return redirect(url_for('index'))
            else:
                handle_error(response)

        except requests.RequestException as e:
            flash(f"Error en la solicitud: {e}", 'error')

       # Realiza una petición GET para obtener los detalles del activo
    url = f"{os.environ.get('API_ADDRESS')}/api/assets/{asset_id}"
    headers = {
        "X-api-key": get_api_key(),
    }
    
    try:
        response = requests.get(url, headers=headers)

        if not response.ok:
            handle_error(response)
            flash(f"Error al obtener los detalles del activo. Código: {response.status_code}", 'error')
            return redirect(url_for('index'))
        response_json = response.json()
        # Crea una instancia del formulario y llena los campos con los datos del activo
        form.precio.data = response_json['Price']
        form.bodega.data = response_json['Winery']
        form.uva.data = response_json['Varietal']
        form.cosecha.data = response_json['Year']
        form.humedad.data = response_json['Humidity']
        form.temperatura.data = response_json['Temperature']
        form.latitud.data = response_json['Latitude']
        form.longitud.data = response_json['Longitude']
        form.owner.data = response_json['Owner']

        coordenadas = ({'latitude': response_json['Latitude'], 'longitude': response_json['Longitude']})

    except requests.RequestException as e:
        flash(f"Error en la solicitud: {e}", 'error')
        return redirect(url_for('index'))

    return render_template('update_asset.html', form=form, asset_id=asset_id, coordenadas=coordenadas)

@app.route("/transfer_asset/<string:asset_id>", methods=['GET', 'POST'])
def transfer_asset(asset_id):

    form = TransferAssetForm()

    if get_org() == "Org1MSP":
        form.owner.choices = [('Org2MSP', 'Transportador')]
    elif get_org() == "Org2MSP":
        form.owner.choices = [('Org1MSP', 'Productor'),('Org3MSP', 'Cliente')]
    elif get_org() == "Org3MSP":
        form.owner.choices = [('Org2MSP', 'Transportador')]


    if request.method == 'POST' and form.validate_on_submit():
        # Actualiza los campos del activo con los valores del formulario
        url = f"{os.environ.get('API_ADDRESS')}/api/assets/{asset_id}"
        headers = {
            "X-api-key": get_api_key(),
        }

        owner = form.owner.data

        body = [{
            "Role": "admin",
            "op": "replace",
            "path": "/Owner",
            "value": owner,
        }]

        try:
            response = requests.patch(url, json=body, headers=headers)

            if response is None:
                raise requests.RequestException("No se recibió respuesta.")
            
            if response.status_code == 200:
                handle_success(response)
            elif response.status_code == 202:
                handle_job_created(response, headers)
                return redirect(url_for('index'))
            else:
                handle_error(response)

        except requests.RequestException as e:
            flash(f"Error en la solicitud: {e}", 'error')

    return render_template('transfer_asset.html', form=form, asset_id=asset_id)

@app.route("/asset_history/<string:asset_id>", methods=['GET', 'POST'])
def asset_history(asset_id):
    url = f"{os.environ.get('API_ADDRESS')}/api/assets/history/{asset_id}"
    headers = {
        "X-api-key": get_api_key(),
    }
    try:
        response = requests.get(url, headers=headers)

        if response is None:
            raise requests.RequestException("No se recibió respuesta.")
        if response.status_code == 200:
            response = response.json()
            flash(f"Respuesta de la API: EXITOSA", 'success')
        # Procesar datos antes de pasarlos a la plantilla
            coordenadas = []
            for entry in response:
                data = entry['data']
                data_dict = json.loads(data)
                if data_dict['Owner']  == "Org1MSP":
                    data_dict['Owner'] = "Productor"
                elif data_dict['Owner'] == "Org2MSP":
                    data_dict['Owner'] = "Transportador"
                elif data_dict['Owner'] == "Org3MSP":
                    data_dict['Owner'] = "Cliente"
                seconds = entry['timestamp']['seconds']
                nanos = entry['timestamp']['nanos']
                timestamp = datetime.fromtimestamp(seconds + nanos / 1e9)

                entry['timestamp'] = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                entry['data'] = data_dict

                coordenadas.append({'latitude': data_dict['Latitude'], 'longitude': data_dict['Longitude'], 'time': entry['timestamp'], 'owner': data_dict['Owner']})
            coordenadas.reverse
            return render_template("asset_history.html", response=response, coordenadas=coordenadas)
        else:
            handle_error(response)
            return render_template("asset_history.html", response=response)

    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")

    return render_template("asset_history.html", response=response)

@app.route('/assets')
def assets():
    url = f"{os.environ.get('API_ADDRESS')}/api/assets"
    headers = {
        "X-api-key": get_api_key(),
    }
    try:
        response = requests.get(url, headers=headers)

        if response is None:
            raise requests.RequestException("No se recibió respuesta.")
        if response.status_code == 200:
            filtered_assets = [asset for asset in response.json() if asset.get('Owner') == get_org()]
            flash(f"Respuesta de la API: EXITOSA", 'success')
            return render_template("assets.html", response=filtered_assets)
        else:
            handle_error(response)
            return render_template("assets.html", response=response)

    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")

    return render_template("assets.html", title='Assets', response=response)

@app.route('/assets_historial')
def assets_historial():
    url = f"{os.environ.get('API_ADDRESS')}/api/assets"
    headers = {
        "X-api-key": get_api_key(),
    }
    try:
        response = requests.get(url, headers=headers)

        if response is None:
            raise requests.RequestException("No se recibió respuesta.")
        if response.status_code == 200:
            flash(f"Respuesta de la API: EXITOSA", 'success')
            response = response.json()
            for asset in response:
                if asset['Owner']  == "Org1MSP":
                    asset['Owner'] = "Productor"
                elif asset['Owner'] == "Org2MSP":
                    asset['Owner'] = "Transportador"
                elif asset['Owner'] == "Org3MSP":
                    asset['Owner'] = "Cliente"
            return render_template("assets_historial.html", response=response)
        else:
            handle_error(response)
            return render_template("assets_historial.html", response=response)

    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")

    return render_template("assets_historial.html", title='Assets historial', response=response)

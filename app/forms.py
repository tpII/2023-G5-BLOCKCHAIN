# app/forms.py

from flask_wtf import FlaskForm
from wtforms import FloatField, HiddenField, SelectField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import User

# Formulario de login
class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordar')
    submit = SubmitField('Iniciar sesión')
    client_login = SubmitField('Acceder como cliente')

# Formulario de registro
class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password2 = PasswordField(
        'Repetir contraseña', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Rol', choices=[('Productor', 'Productor'), ('Transportador', 'Transportador')])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Ese nombre de usuario está en uso.')

# Formulario de lectura de asset
class ReadAssetForm(FlaskForm):
    rfid_tag = StringField('Rfid', validators=[DataRequired()])
    llenar_boton = SubmitField('Escanear RFID')
    enviar_boton = SubmitField('Enviar Formulario')

# Formulario de creación de asset
class CreateAssetForm(FlaskForm):
    rfid_tag = StringField('Rfid', validators=[DataRequired()])
    llenar_boton_rfid = SubmitField('Escanear RFID')
    precio = FloatField('Precio', validators=[DataRequired()])
    bodega = StringField('Bodega', validators=[DataRequired()])
    uva = StringField('Tipo de uva', validators=[DataRequired()])
    cosecha = StringField('Cosecha', validators=[DataRequired()])
    temperatura = FloatField('Temperatura', validators=[DataRequired()])
    humedad = FloatField('Humedad', validators=[DataRequired()])
    llenar_boton_dht = SubmitField('Escanear DHT')
    latitud = FloatField('Latitud', validators=[DataRequired()])
    longitud = FloatField('Longitud', validators=[DataRequired()])
    enviar_boton = SubmitField('Enviar Formulario')

class UpdateAssetForm(FlaskForm):
    precio = FloatField('Precio', validators=[DataRequired()])
    bodega = StringField('Bodega', validators=[DataRequired()])
    uva = StringField('Tipo de uva', validators=[DataRequired()])
    cosecha = StringField('Cosecha', validators=[DataRequired()])
    temperatura = FloatField('Temperatura', validators=[DataRequired()])
    humedad = FloatField('Humedad', validators=[DataRequired()])
    llenar_boton_dht = SubmitField('Escanear DHT')
    latitud = FloatField('Latitud', validators=[DataRequired()])
    longitud = FloatField('Longitud', validators=[DataRequired()])
    owner = HiddenField()
    actualizar_boton = SubmitField('Actualizar Formulario')

class TransferAssetForm(FlaskForm):
    owner = SelectField('Dueño', choices=[])
    transferir_boton = SubmitField('Transferir asset')


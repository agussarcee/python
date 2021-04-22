from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DecimalField
from wtforms.validators import Required, NumberRange


class LoginForm(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[Required()])
    password = PasswordField('Contraseña', validators=[Required()])
    enviar = SubmitField('Ingresar')


class RegistrarForm(LoginForm):
    password_check = PasswordField('Verificar Contraseña', validators=[Required()])
    enviar = SubmitField('Registrarse')


class CargarForm(FlaskForm):
    nombre = StringField('Nombre del cliente', validators=[Required()])
    edad = StringField('Edad', validators=[Required()])
    direccion = StringField('Dirección', validators=[Required()])
    pais = StringField('Pais', validators=[Required()])
    documento = StringField('DNI', validators=[Required()])
    fecha = StringField('Fecha (YYYY-MM-DD)', validators=[Required()])
    correo = StringField('Correo electronico', validators=[Required()])
    trabajo = StringField('Trabajo', validators=[Required()])
    enviar = SubmitField('Cargar')

class BuscarForm(FlaskForm):
    pais = StringField('Busqueda', validators=[Required()])
    enviar = SubmitField('Buscar')

class EdadForm(FlaskForm):
    edadmin = DecimalField('Desde:', validators=[Required(), NumberRange(min=0, max=150, message="Solo edades positivas")])
    edadmax = DecimalField('Hasta:', validators=[Required(), NumberRange(min=0, max=150, message="Solo edades positivas")])
    enviar = SubmitField('Buscar')

class FechaForm(FlaskForm):
    fecha = StringField('Fecha: (el formato para ingresar es YYYY-MM-DD)', validators=[Required()])
    enviar = SubmitField('Buscar')
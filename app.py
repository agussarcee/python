import csv
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_bootstrap import Bootstrap

from forms import LoginForm, RegistrarForm, CargarForm, BuscarForm, EdadForm, FechaForm


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'un string que funcione como llavee'


@app.route('/')
def index():
    return render_template('index.html', fecha_actual=datetime.utcnow())


@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500


@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios.csv') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    flash('Bienvenido')
                    session['username'] = formulario.usuario.data
                    return render_template('ingresado.html')
                registro = next(archivo_csv, None)
            else:
                flash('Revisá nombre de usuario y contraseña')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios.csv', 'r') as archivo:
                csv_reader = csv.reader(archivo)
                for row in csv_reader:
                    if row [0] == formulario.usuario.data and row [1] == formulario.password.data:
                        flash('Usuario ya existe')
                        return redirect(url_for('registrar'))
            with open('usuarios.csv', 'a', newline='') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')
    return render_template('registrar.html', form=formulario)


@app.route('/listado_de_clientes')
def tabla():
    if 'username' in session:
        with open("clientes.csv", encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            esto = []
            for row in csv_reader:
                esto.append (row)
        return render_template('tabla.html', esto = esto, cantidad = len(esto)) 
    else:
        return redirect(url_for('index'))

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/cargar_cliente', methods=['GET', 'POST'])
def carga():
    if 'username' in session:
        formulario = CargarForm()
        if formulario.validate_on_submit():
            with open('clientes.csv', 'a', newline='') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.nombre.data, formulario.edad.data, 
                            formulario.direccion.data, formulario.pais.data,
                            formulario.documento.data, formulario.fecha.data,
                            formulario.correo.data, formulario.trabajo.data]
                archivo_csv.writerow(registro)
            flash('Cliente cargado correctamente')
            return redirect(url_for('tabla'))
        return render_template('carga.html', nuevo=formulario)
    else:
        return redirect(url_for('index'))

@app.route('/busqueda_pais', methods=['GET', 'POST'])
def busqueda_pais():
    if 'username' in session:
        formulario = BuscarForm()
        if formulario.validate_on_submit():
            busqueda = formulario.pais.data.capitalize()
            with open("clientes.csv", encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                esto = []
                nohay = 0
                for row in csv_reader:
                    pais = row["País"]
                    if busqueda in pais and pais not in esto:
                        esto.append(pais)
                        nohay = nohay + 1
                return render_template('busqueda_pais.html', form=formulario, esto=esto, nohay=nohay)
        return render_template('busqueda_pais.html', form=formulario)
    else:
        return redirect(url_for('index'))


@app.route('/tabla_pais', methods=['GET','POST'])
def tabla_pais():
    if 'username' in session:
        pais = request.args.get('variable')
        with open("clientes.csv", encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            esto = []
            for row in csv_reader:
                if row["País"] == pais:
                    esto.append(row)
        return render_template('tabla.html', esto = esto, cantidad = len(esto))
    else:
        return redirect(url_for('index'))

@app.route('/edad_cliente', methods=['GET', 'POST'])
def edad_cliente():
    if 'username' in session:
        formulario = EdadForm()
        if formulario.validate_on_submit():
            edadmin = int (formulario.edadmin.data)
            edadmax = int (formulario.edadmax.data)
            with open("clientes.csv", encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                esto = []
                for row in csv_reader:
                    edad = int (row["Edad"])
                    if edad>=edadmin and edad<=edadmax:
                        esto.append(row)
                return render_template('tabla.html', esto = esto, cantidad = len(esto))
        return render_template('busqueda_edad.html', form=formulario)
    else:
        return redirect(url_for('index'))


@app.route('/fecha_cliente', methods=['GET', 'POST'])
def fecha_cliente():
    if 'username' in session:
        formulario = FechaForm()
        if formulario.validate_on_submit():
            fecha = formulario.fecha.data
            with open("clientes.csv", encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                esto = []
                for row in csv_reader:
                    if fecha == row ["Fecha Alta"]:
                        esto.append(row)
                return render_template('tabla.html', esto = esto, cantidad = len(esto))
        return render_template('busqueda_fecha.html', form=formulario)
    else:
        return redirect(url_for('index'))


@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect # libreria para proteccion
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash # encriptacion de contraseñas
from config import *
from config import config
from models.ModelUser import ModelUser #scripts models
from models.entities.User import User # scripts entidades
import smtplib
from email.message import EmailMessage# enviar correo gmail

import mercadopago
#==============================================================================
#==============================================================================
#Inicia estrucuta flask e instancian funciones
app = Flask(__name__)
csrf = CSRFProtect()
db = MySQL(app)
sdk = mercadopago.SDK("TEST-4584654371452389-110715-c5febaac639ea0265cc5ed424727fa6c-191633463")

preference_data = {
        "items": [
            {
                "id":"001",
                "title": "Mi producto",
                "quantity": 1,
                "unit_price": 5.76,
                "currency_id":"MX"
            }
        ]
    }

preference_response = sdk.preference().create(preference_data)
preference = preference_response["response"]


login_manager_app = LoginManager(app)
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('login'))
#==============================================================================
@app.route('/mercadopago', methods=['GET', 'POST'])
def mercadopago():
    sdk = mercadopago.SDK("TEST-4584654371452389-110715-c5febaac639ea0265cc5ed424727fa6c-191633463")

    # Crea un ítem en la preferencia
    preference_data = {
        "items": [
            {
                "id":"001",
                "title": "Mi producto",
                "quantity": 1,
                "unit_price": 5.76,
                "currency_id":"MX"
            }
        ]
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]

#===========================================================================
#funcion para confirmar gmail de usuario
def ConfirmacionGmail(gmail):
    remitente = "renehiguera15@gmail.com"
    destinatario = gmail
    mensaje = "¡<strong>Confirma tu cuenta en</strong>,http://127.0.0.1:7000/confirmacion<em>Porfavor</em>!"
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "¡Usa WebCoop!"
    email.set_content(mensaje, subtype="html")
    #smtp = smtplib.SMTP_SSL("smtp.ejemplo.com")
    # O si se usa TLS:
    # smtp = SMTP("smtp.ejemplo.com", port=587)
    # smtp.starttls()
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(remitente, "accorzuwpwvhqhlp")
    server.sendmail(remitente, destinatario, email.as_string())
    server.quit()
#============================================================================
def Restablecimiento(gmail):
    remitente = "renehiguera15@gmail.com"
    destinatario = gmail
    mensaje = "¡<strong>Restablece tu contraseña aqui</strong>,http://127.0.0.1:5000/NPassword<em>Porfavor</em>!"
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "¡Hola usuario de WebCoop!"
    email.set_content(mensaje, subtype="html")
    #smtp = smtplib.SMTP_SSL("smtp.ejemplo.com")
    # O si se usa TLS:
    # smtp = SMTP("smtp.ejemplo.com", port=587)
    # smtp.starttls()
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(remitente, "accorzuwpwvhqhlp")
    server.sendmail(remitente, destinatario, email.as_string())
    server.quit()
    print("hereee2")

#funcion establecida para recoger datos usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        gmail = request.form['gmail']
        matricula = request.form['matricula']
        password = request.form['username']
        fullname = request.form['fullname']
        print(username)
        print(gmail)
        print(matricula)
        print(password)
        print(fullname)

        if request.form['password'] == request.form['confipassword'] and username != "" and gmail != "" and matricula != "" and fullname != "":
            password = generate_password_hash(request.form['password'])
            NewUser = User(0,username,gmail,matricula,password, fullname)
            #ModelUser.registro(db, NewUser) 
            ConfirmacionGmail(gmail)
            ConfirmacionUsuario(NewUser)
            return render_template('auth/guia.html')
        else: 
            flash("campo no valido...")
            return  render_template('auth/login.html')
    else:
     return render_template('auth/login.html')
#=====================================================================
#funcion para dar de alta usuario con datos recogidos anteriormente
@app.route('/register', methods=['GET', 'POST'])
def ConfirmacionUsuario(NewUser):
    if request.method == 'POST':
        ModelUser.registro(db, NewUser)
        return render_template('auth/login.html')
#====================================================================
#funcion para que usuario inicie sesion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['username'])
        # print(request.form['password'])
        user = User(0,0,0, request.form['matricula'], request.form['password'])
        #user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                print("Hola de login")
                return render_template('auth/home.html')
               # return redirect(url_for('home'))
            else:
                flash("contraseña incorrecta...")
                return render_template('auth/login.html')
        elif request.form['matricula'] == "admin12" and request.form['password'] == "admin12":
            return render_template('auth/admins.html')
        else:
            flash("Usuario no encontrado...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')
#=========================================================
@app.route('/guia2', methods=['GET', 'POST'])
def guia2():
    if request.method == 'POST':
        return render_template('auth/guia2.html')
#=========================================================
@app.route('/RestablecimientoPassword', methods=['GET', 'POST'])
def RestablecimientoPassword():
    if request.method == 'POST':
        matricula = request.form['matricula']
        cursor = db.connection.cursor()
        sql = """SELECT id, username, gmail, matricula, password, fullname FROM clientes WHERE matricula = '{}'""".format(matricula)
        cursor.execute(sql)
        row = cursor.fetchone()
        print(row[2])
        global GmailRestablecimientoPassword
        GmailRestablecimientoPassword = row[2]
        db.connection.commit()
        Restablecimiento(GmailRestablecimientoPassword)
        print("hereee1")
        flash("Mensaje enviado a tu email...")
        return render_template('auth/login.html')
    else: return render_template('auth/login.html')
@app.route('/NewPassword', methods=['GET', 'POST'])
def NewPassword():
    if request.method == 'POST':
        password = request.form['password']
        confipassword = request.form['confipassword']
        if password == confipassword:
           password = generate_password_hash(request.form['password'])
           cursor = db.connection.cursor()
           sql = f"UPDATE clientes SET password = '{password}' WHERE gmail ='{GmailRestablecimientoPassword}'"
           cursor.execute(sql)
           db.connection.commit() 
           return render_template('auth/login.html')
        else:
            return render_template('auth/login.html')
    elif request.method == "GET":
        return render_template('auth/login.html')
    else: return render_template('auth/login.html')
#============================================================
@app.route('/Compra', methods=['GET', 'POST'])
def Compra():
    if request.method == 'POST':
        return render_template('auth/compra.html')




@app.route('/PagarCarrito', methods=['GET', 'POST'])
def PagarCarrito():
    if request.method == 'POST':
     return render_template('auth/pedidos.html')
@app.route('/CallPedidos', methods=['GET', 'POST'])
def CallPedidos():
    if request.method == 'POST':
     return render_template('auth/pedidos.html')
    
#funcion para cerrar sesiones 

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/pago')
def pago():
    return render_template('pago.html')

@app.route('/compra')
def compra():
    return render_template('compra.html')
@app.route('/caja')
def caja():
    return render_template('caja.html')
@app.route('/guia')
def guia():
    return render_template('guia.html')

@app.route('/confirmacion')
def confirmacion():
    return render_template('confirmacion.html')

@app.route('/NPassword')
def NPassword():
    return render_template('NPassword.html')

@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"

def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404
    #return render_template('compra.html')
#===============================================================================
#inicia el server
if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(port = 7000)
    

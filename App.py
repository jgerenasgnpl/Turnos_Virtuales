from flask import Flask, render_template, request, redirect, url_for, session, flash
from Models import db, Turno
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime, timezone  # Ajuste para manejo de UTC
import os

# Zona horaria de Colombia
colombia_tz = timezone.utc

app = Flask(__name__)
app.secret_key = os.urandom(24) # Esto configura una clave secreta para la sesión
app.config['SECRET_KEY'] = 'Alemania2024*' 
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://@5CD0455FKS\\MSSQLSERVER01/Turno_virtuales?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
# Ruta principal para seleccionar regional
@app.route('/')
def select_regional():
    return render_template('select_regional.html')
# Ruta para mostrar las opciones de campaña después de seleccionar la regional
@app.route('/inicio/<regional>', methods=['GET', 'POST'])
def select_campaign(regional):
    campaigns = {
        'Bogota': ['NPL', 'Adamantine', 'Jcap', 'Credivalores'],
        'Cali': ['NPL', 'Jcap'],
        'Barranquilla': ['NPL', 'Adamantine']
    }

    if request.method == 'POST':
        selected_campaign = request.form.get('campaign')
        
        # Guardar en session
        session['regional'] = regional
        session['campaign'] = selected_campaign

        return redirect(url_for('inicio', regional=regional, campaign=selected_campaign))

    return render_template('select_campaign.html', regional=regional, campaigns=campaigns.get(regional, []))

@app.route('/inicio')
def inicio():
    regional = session.get('regional')
    campaign = session.get('campaign')
    return render_template('inicio.html', regional=regional, campaign=campaign)

@app.route('/gestionar_turnos/<regional>/<campaign>')
def gestionar_turnos_especifico(regional, campaign):
    turnos = Turno.query.filter_by(regional=regional, campaign=campaign, atendido=False).all()
    return render_template('manage.html', turnos=turnos, regional=regional, campaign=campaign)

@app.route('/solicitar_turno/<regional>/<campaign>', methods=['GET', 'POST'])
def solicitar_turno(regional, campaign):
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cedula = request.form.get('cedula')
        telefono = request.form.get('telefono')
        correo = request.form.get('correo')
        motivo = request.form.get('motivo')
        # Obtener el próximo número de turno para esta combinación de regional y campaña
        ultimo_turno = Turno.query.filter_by(regional=regional, campaign=campaign).order_by(Turno.numero_turno_regional.desc()).first()
        numero_turno_regional = 1 if not ultimo_turno else ultimo_turno.numero_turno_regional + 1
        # Crear un nuevo turno
        nuevo_turno = Turno(
            nombre=nombre,
            cedula=cedula,
            telefono=telefono,
            correo=correo,
            motivo=motivo,
            regional=regional,
            campaign=campaign,
            numero_turno_regional=numero_turno_regional,
            fecha_creacion=datetime.now(timezone.utc)
        )
        # Guardar en la base de datos
        db.session.add(nuevo_turno)
        db.session.commit()
        # Redirigir a la página de confirmación
        return redirect(url_for('confirmacion_turno', turno_numero=nuevo_turno.numero_turno_regional, regional=regional, campaign=campaign))

    return render_template('form.html', regional=regional, campaign=campaign)

@app.route('/listado_turnos/<regional>/<campaign>')
def listado_turnos(regional, campaign):
    turnos_pendientes = Turno.query.filter_by(regional=regional, campaign=campaign, atendido=False).all()
    for turno in turnos_pendientes:
        if turno.fecha_creacion:
            # Asegura que ambos datetime tengan la misma zona horaria
            fecha_creacion_utc = turno.fecha_creacion.replace(tzinfo=timezone.utc)  # Convertir a UTC si es naive
            diferencia_tiempo = datetime.now(timezone.utc) - fecha_creacion_utc
            turno.tiempo_pendiente = diferencia_tiempo
    
    return render_template('listado_turnos.html', turnos=turnos_pendientes, regional=regional, campaign=campaign)   

@app.route('/confirmacion_turno/<int:turno_numero>')
def confirmacion_turno(turno_numero):
    turno = Turno.query.filter_by(numero_turno_regional=turno_numero).first()
    if not turno:
        return "Turno no encontrado", 404
    
    return render_template('confirmacionTurno.html', turno=turno)

@app.route('/atender_turno/<int:id>', methods=['POST', 'GET'])
def atender_turno(id):
    turno = Turno.query.get(id)  # Obtén el turno por su ID específico

    if not turno:
        return "Turno no encontrado", 404

    if request.method == 'POST':
        print("Datos recibidos del formulario:", request.form)
        tipo_gestion = request.form.get('tipo_gestion')
        turno.tipo_gestion = tipo_gestion
        turno.pago_cuotas = request.form.get('pago_cuotas')
        turno.valor_acuerdo = request.form.get('valor_acuerdo')
        turno.observacion = request.form.get('observacion')
        turno.fecha_gestion = datetime.now(timezone.utc) 
        turno.atendido = True

        db.session.commit()

        # Verificar si la tipificación es "acuerdo y pago de deuda"
        if tipo_gestion == "acuerdo y pago de deuda":
            # Contar cuántos turnos de "acuerdo y pago de deuda" han sido atendidos
            conteo_pagos = Turno.query.filter_by(tipo_gestion="acuerdo y pago de deuda", atendido=True).count()

            # Verificar si el conteo es múltiplo de 20
            if conteo_pagos % 20 == 0:
                turno.ganador = 1  # Marcar el turno como ganador en la base de datos
                db.session.commit()  # Guarda los cambios
                flash("¡Felicidades! Has ganado el premio.", "success")
                return redirect(url_for('jugar_tragamonedas', premio="🏆"))
            else:
                turno.ganador = 0  # Marcar como no ganador
                db.session.commit()
                flash("¡Gracias por tu participación!", "info")
                return redirect(url_for('jugar_tragamonedas', premio="💼"))

        return redirect(url_for('gestionar_turnos_especifico', regional=turno.regional, campaign=turno.campaign))

    return render_template('attend.html', turno=turno)

@app.route('/jugar_tragamonedas/<premio>', methods=['GET'])
def jugar_tragamonedas(premio):
    # Renderiza la página de tragamonedas y pasa el premio como variable
    return render_template('tragamonedas.html', premio=premio)

if __name__ == '__main__':
    app.run(debug=True)

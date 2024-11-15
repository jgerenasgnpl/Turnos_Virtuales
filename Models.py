from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Turno(db.Model):
    __tablename__ = 'Data_Turnos'  # Aquí defines el nombre de la tabla

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero_turno_regional = db.Column(db.Integer, nullable=False)  # Contador regional
    nombre = db.Column(db.String(50), nullable=False)
    cedula = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(50), nullable=False)
    motivo = db.Column(db.String(100), nullable=False)
    atendido = db.Column(db.Boolean, default=False)
    tipo_gestion = db.Column(db.String(50))
    pago_cuotas = db.Column(db.String(50))
    regional = db.Column(db.String(50))  # Campo para la regional
    campaign = db.Column(db.String(50))  # Campo para la campaña
    valor_acuerdo = db.Column(db.Float)
    observacion = db.Column(db.String(255))
    fecha_gestion = db.Column(db.DateTime, nullable=True)
    fecha_creacion = db.Column(db.DateTime, default= datetime.utcnow)  # Nuevo campo de fecha de registro
    contador_pago_deuda = db.Column(db.Integer, default=0)  # Nuevo campo para contador
    ganador = db.Column(db.Boolean, default=False)  # Nuevo campo para indicar si es ganador
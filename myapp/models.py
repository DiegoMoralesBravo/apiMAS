from .extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    occupation = db.Column(db.String(100))
    password = db.Column(db.String(100))

class PlantEntry(db.Model):
    __tablename__ = 'plant_entries'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100))
    nombre = db.Column(db.String(100))
    frecuenciaRiego = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    recomendaciones = db.Column(db.Text)
    lastWateredTime = db.Column(db.DateTime, default=datetime.utcnow)

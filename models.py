from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(80), nullable=False)
    mac_address = db.Column(db.String(17), nullable=False, unique=True)
    device_type = db.Column(db.String(80), nullable=False)
    assigned_ip = db.Column(db.String(15))
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Device {self.device_name}>"

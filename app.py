from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, MacAddress
from flask_migrate import Migrate
from forms import AddDeviceForm, EditDeviceForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:pass@localhost/devices'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(80), nullable=False)
    mac_address = db.Column(db.String(17), nullable=False, unique=True)
    device_type = db.Column(db.String(80), nullable=False)
    assigned_ip = db.Column(db.String(15))
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime)

@app.route('/')
def index():
    devices = Device.query.all()
    return render_template('index.html', title='Device List', devices=devices)

@app.route('/add-device', methods=['GET', 'POST'])
def add_device():
    form = AddDeviceForm()

    if form.validate_on_submit():
        device = Device(
            device_name=form.device_name.data,
            mac_address=form.mac_address.data,
            device_type=form.device_type.data,
            assigned_ip=form.assigned_ip.data
        )
        db.session.add(device)
        try:
            db.session.commit()
            flash('Device added successfully!')
            return redirect(url_for('index'))
        except IntegrityError as e:
            db.session.rollback()
            error_message = str(e.orig)  # Extract the error message
            if "Duplicate entry" in error_message:
                return jsonify({"error": "duplicate"}), 409  # Conflict
            else:
                return jsonify({"error": "unknown"}), 500  # Internal Server Error

    return render_template('add_device.html', form=form)

@app.route('/edit-device/<int:id>', methods=['GET', 'POST'])
def edit_device(id):
    device = Device.query.get_or_404(id)

    if request.method == 'GET':
        form = EditDeviceForm(current_device_type=device.device_type, obj=device)
    else:
        form = EditDeviceForm(request.form, obj=device)
        
        if form.validate_on_submit():
            device.device_name = form.device_name.data
            device.mac_address = form.mac_address.data
            device.device_type = form.device_type.data
            device.assigned_ip = form.assigned_ip.data
            device.date_modified = datetime.utcnow()
            db.session.commit()
            flash('Device updated successfully!')
            return redirect(url_for('index'))

    return render_template('edit_device.html', title='Edit Device', form=form, device=device)

@app.route('/delete-device/<int:id>', methods=['GET', 'POST'])
def delete_device(id):
    device = Device.query.get_or_404(id)
    db.session.delete(device)
    db.session.commit()
    flash('Device deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

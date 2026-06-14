from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, request
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from models import db, Device
from flask_wtf.csrf import generate_csrf
from forms import AddDeviceForm, EditDeviceForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

DEVICE_ICONS = {
    'Laptop':  '💻',
    'Desktop': '🖥️',
    'Phone':   '📱',
    'Tablet':  '📲',
    'Server':  '🗄️',
    'TV':      '📺',
    'Router':  '📡',
    'Watch':   '⌚',
    'Misc':    '🔌',
}

@app.template_global()
def device_icon(device_type):
    return DEVICE_ICONS.get(device_type, '🔲')

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    devices = Device.query.order_by(Device.date_added.desc()).all()
    return render_template('index.html', title='Device List', devices=devices, delete_csrf=generate_csrf())


@app.route('/add-device', methods=['GET', 'POST'])
def add_device():
    form = AddDeviceForm()
    if form.validate_on_submit():
        device = Device(
            device_name=form.device_name.data,
            mac_address=form.mac_address.data,
            device_type=form.device_type.data,
            assigned_ip=form.assigned_ip.data or None,
        )
        db.session.add(device)
        try:
            db.session.commit()
            flash(f'Device "{device.device_name}" added successfully.', 'success')
            return redirect(url_for('index'))
        except IntegrityError:
            db.session.rollback()
            flash('A device with that MAC address already exists.', 'error')
    return render_template('add_device.html', title='Add Device', form=form)


@app.route('/edit-device/<int:id>', methods=['GET', 'POST'])
def edit_device(id):
    device = db.get_or_404(Device, id)
    if request.method == 'GET':
        form = EditDeviceForm(current_device_type=device.device_type, obj=device)
    else:
        form = EditDeviceForm(obj=device)
        if form.validate_on_submit():
            device.device_name = form.device_name.data
            device.mac_address = form.mac_address.data
            device.device_type = form.device_type.data
            device.assigned_ip = form.assigned_ip.data or None
            device.date_modified = datetime.utcnow()
            try:
                db.session.commit()
                flash(f'Device "{device.device_name}" updated.', 'success')
                return redirect(url_for('index'))
            except IntegrityError:
                db.session.rollback()
                flash('A device with that MAC address already exists.', 'error')
    return render_template('edit_device.html', title='Edit Device', form=form, device=device)


@app.route('/delete-device/<int:id>', methods=['POST'])
def delete_device(id):
    device = db.get_or_404(Device, id)
    name = device.device_name
    db.session.delete(device)
    db.session.commit()
    flash(f'Device "{name}" deleted.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

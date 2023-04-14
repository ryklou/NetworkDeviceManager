from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, MacAddress

class EditDeviceForm(FlaskForm):
    device_name = StringField('Device Name', validators=[DataRequired()])
    mac_address = StringField('MAC Address', validators=[DataRequired(), MacAddress()])
    device_type = SelectField('Device Type', validators=[DataRequired()], choices=[('', 'Select a Device Type'), ('Laptop', 'Laptop'), ('Desktop', 'Desktop'), ('Phone', 'Phone'), ('Tablet', 'Tablet'), ('Server', 'Server'), ('TV', 'TV'), ('Router', 'Router'), ('Misc', 'Misc.'), ('Watch', 'Watch')])
    assigned_ip = StringField('Assigned IP')
    submit = SubmitField('Save')

    def __init__(self, current_device_type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if current_device_type:
            self.device_type.default = current_device_type
            self.process()  # Update the form with the new default value

class AddDeviceForm(FlaskForm):
    device_name = StringField('Device Name', validators=[DataRequired()])
    mac_address = StringField('MAC Address', validators=[DataRequired(), MacAddress()])
    device_type = SelectField('Device Type', validators=[DataRequired()], choices=[('', 'Select a Device Type'), ('Laptop', 'Laptop'), ('Desktop', 'Desktop'), ('Phone', 'Phone'), ('Tablet', 'Tablet'), ('Server', 'Server'), ('TV', 'TV'), ('Router', 'Router'), ('Misc', 'Misc.'), ('Watch', 'Watch')])
    assigned_ip = StringField('Assigned IP')
    submit = SubmitField('Add')

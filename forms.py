from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, MacAddress

class EditDeviceForm(FlaskForm):
    device_name = StringField('Device Name', validators=[DataRequired()])
    mac_address = StringField('MAC Address', validators=[DataRequired(), MacAddress()])
    device_type = StringField('Device Type', validators=[DataRequired()])
    assigned_ip = StringField('Assigned IP')
    submit = SubmitField('Save')

from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms import ValidationError


# noinspection PyMethodMayBeStatic
class HostForm(Form):
    fqdn = StringField('FQDN or IP', validators=[DataRequired()])
    port = StringField('TCP Port')
    friendly_name = StringField('Friendly Name')
    submit = SubmitField('Submit')
    
    def validate_port(self, field):
        if len(field.data) > 0:
            try:
                int(field.data)
            except ValueError:
                raise ValidationError('Port provided is not valid')

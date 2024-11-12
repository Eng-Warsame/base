from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ClientForm(FlaskForm):
    clientname = StringField("Client Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    status = SelectField("Status", choices=[("active","Active"), ('inactive',"InActive")])
    submit = SubmitField("Submit")

    
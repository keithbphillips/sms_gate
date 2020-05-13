from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    phone_num = StringField('Phone#', validators=[DataRequired()])
    sms_text = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

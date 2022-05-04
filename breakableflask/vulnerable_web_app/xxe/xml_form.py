from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class XMLForm(FlaskForm):
    xml = TextAreaField('XML', validators=[DataRequired()])
    submit = SubmitField('Submit')
from wtforms import Form, StringField, HiddenField, RadioField
from wtforms import validators
from model import calon


class VoteForm(Form):
    
    key = HiddenField('Key', [validators.DataRequired()])
    pilihan = RadioField('Pilihan', [validators.DataRequired()], coerce=int)

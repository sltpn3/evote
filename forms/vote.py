from wtforms import Form, StringField, HiddenField, RadioField
from wtforms import validators


class VoteForm(Form):
    key = HiddenField('Key', [validators.DataRequired()])
    pilihan = RadioField('Pilihan', [validators.DataRequired()])

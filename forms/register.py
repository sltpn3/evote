from wtforms import Form, StringField, HiddenField, RadioField
from wtforms import validators
from model import calon


class RegisterForm(Form):
    name = StringField('Nama', [validators.DataRequired()], render_kw={"placeholder": "Masukkan Nama"})

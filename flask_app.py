from flask import Flask, request, render_template, flash, send_from_directory
from forms.vote import VoteForm
from controller.evote import EvoteController
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_url_path='')
app.secret_key = b'MzgSuSc4yGm7zTx'
Bootstrap(app)


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('', path)


@app.route('/', methods=['GET'])
def welcome():
    return render_template('index.html')


@app.route('/votes', methods=['GET', 'POST'])
def votes():
    form = VoteForm(request.form)
    form.pilihan.choices = evote.pilihan_choices()
    status = {}
    if request.method == 'POST' and form.validate():
        print(request.form.get('pilihan'))
        return render_template('success.html')

    else:
        print(form.validate())
        print (form.errors)
        print(form.key)
        if form.key._value():
            status = {'key_ok': True}
        for pilihan in form.pilihan.choices:
            print(pilihan)
        return render_template('votes.html', form=form, status=status)


evote = EvoteController(config_file='config.conf')

if __name__ == "__main__":
    app.run('0.0.0.0', '9001')

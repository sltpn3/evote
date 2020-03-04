from flask import Flask, request, render_template, flash, send_from_directory
from forms.vote import VoteForm
from forms.register import RegisterForm
from controller.evote import EvoteController
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_url_path='')
app.secret_key = b'MzgSuSc4yGm7zTx'
app.config['TESTING'] = True
Bootstrap(app)


@app.template_filter('print_alamat')
def print_alamat(alamat):
    if alamat:
        if alamat[:3] == 'AAI':
            return alamat.replace('AAI', 'Alam Asri Indah')
        if alamat[:3] == 'AAH':
            return alamat.replace('AAH', 'Alam Asri Hijau')
        if alamat[:3] == 'AAR':
            return alamat.replace('AAR', 'Alam Asri Raya')
        if alamat[:3] == 'AAL':
            return alamat.replace('AAL', 'Alam Asri Lestari')
    return 'N/A'


@app.template_filter('status_memilih')
def status_memilih(status):
    if int(status) == 0:
        return 'Belum memilih'
    elif int(status) == 1:
        return 'Sudah memilih'


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('', path)


@app.route('/', methods=['GET'])
def welcome():
    return render_template('index.html')


@app.route('/voter/<int:_id>', methods=['GET'])
def voter(_id):
    voter = evote.get_voter(_id)
    return render_template('voter.html', voter=voter)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    voters = None
    if request.method == 'GET':
        pass
    elif request.method == 'POST' and form.validate():
        voters = evote.search_voters_by_name(request.form.get('name'))
    return render_template('register.html', form=form, voters=voters)


@app.route('/votes', methods=['GET', 'POST'])
def votes():
    form = VoteForm(request.form)
    form.pilihan.choices = evote.pilihan_choices()
    status = {}
    if request.method == 'POST' and form.validate():
        return render_template('success.html')
    else:
        if form.key._value():
            status = {'key_ok': True}
        return render_template('votes.html', form=form, status=status)


evote = EvoteController(config_file='config.conf')

if __name__ == "__main__":
    app.run('0.0.0.0', '9001')

from flask import Flask, request, render_template, flash
from forms.vote import VoteForm
from controller.evote import EvoteController

app = Flask(__name__)
app.secret_key = b'MzgSuSc4yGm7zTx'


@app.route('/votes', methods=['GET', 'POST'])
def votes():
    form_vote = VoteForm(request.form)
    form_vote.pilihan.choices = evote.pilihan_choices()
    status = {}
    if request.method == 'POST' and form_vote.validate():
        return render_template('success.html')
#         event_id = request.form.get('event_id', None)
#         email_subject = request.form.get('email_subject', None)
#         email_content = request.form.get('email_content', None)
#         timestamp = request.form.get('timestamp', None)
#         try:
#             jublia.post_save_emails(event_id, email_subject, email_content, timestamp)
#             flash('Data Saved')
#         except Exception, e:
#             '''Usually we send it to error tracking tool such as sentry'''
#             print e
#             flash('Error Saving Data')
#         return render_template('save_emails.html', form=form)
    else:
        print(form_vote.validate())
        print (form_vote.errors)
        print(form_vote.key)
        if form_vote.key._value():
            status = {'key_ok': True}
        for pilihan in form_vote.pilihan.choices:
            print(pilihan)
        return render_template('votes.html', form=form_vote, status=status)


evote = EvoteController(config_file='config.conf')

app.run('0.0.0.0', '9001')

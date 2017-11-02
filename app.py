from flask import Flask, render_template, redirect, url_for
from firebase import firebase
from config import firebase_path
from flask_wtf import FlaskForm as Form
from flask_wtf.csrf import CSRFProtect
from wtforms.fields import StringField, DateField
from wtforms_components import TimeField
from wtforms.validators import DataRequired
from datetime import date, time
from uuid import uuid4

app = Flask(__name__)
firebase = firebase.FirebaseApplication(firebase_path, None)
app.secret_key = "secret" #secureAF

class NewEvent(Form):
    owner_name = StringField('Your Name', validators=[DataRequired()])
    event_name = StringField('Event Name', validators=[DataRequired()])
    event_date = DateField('Event Date (yyyy-mm-dd)', validators=[DataRequired()])
    event_start = TimeField('Start Time (hh:mm) in 24 hour time', validators=[DataRequired()])
    event_end = TimeField('End Time (hh:mm) in 24 hour time', validators=[DataRequired()])

    # returns updated dictionary representation with dates,times serialized
    def serialize_entry(self):
        data = self.data
        for field in data:
            value = data[field]
            if type(value) is time or type(value) is date:
                print value.isoformat()
                data[field] = value.isoformat()
        return data


@app.route("/test")
def test():
    return firebase.get('/test', None)


@app.route("/", methods=['GET', 'POST'])
def index():
    form = NewEvent()
    if form.validate_on_submit():
        new_key = str(uuid4())
        firebase.put('/events', new_key, form.serialize_entry())
        return redirect(url_for('view_event', event_id=new_key))
    return render_template('index.html', form=form)


@app.route("/<event_id>", methods=['GET'])
def view_event(event_id):
    return str(firebase.get('/events/' + str(event_id), None))


if __name__ == '__main__':
    app.run()

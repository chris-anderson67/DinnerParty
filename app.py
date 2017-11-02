from flask import Flask, render_template
from firebase import firebase
from config import firebase_path
from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, DateField
from wtforms_components import TimeField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
import datetime
import json
import random

app = Flask(__name__)
firebase = firebase.FirebaseApplication(firebase_path, None)
app.secret_key = "secret"

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
            if type(value) is datetime.time or type(value) is datetime.date:
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
        curr_entries = firebase.get('/events')
        new_key = random.randint(1, 100000000)
        while (new_key not in curr_entries.keys):
            new_key = random.randint(1, 100000000)

        firebase.put('/events', new_key, form.serialize_entry())
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run()

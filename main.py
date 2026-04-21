from flask import Flask ,render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
# Note: using two // will indicate the use of a driver on this computer
# This is especially important if used 'pip install mysql-connector-python' command
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ithertzwhenIP#1984@localhost/nursingHomeDB.sql'

db = SQLAlchemy(app)

class DatabaseTest(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    # date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template('base.html')

@app.route('/content', methods=['POST', 'GET'])
def tableIndex():
    if(request.method == 'POST'):
        # Grab the task and place it into the DB
        return "Hello World"
    else:
        # Otherwise, just view the page
        return render_template('base.html')

@app.route('/home/patient-options', methods=['POST'])
def patient_options():
    pressed = request.form.get('bt')
    if(pressed == 'patient-table'):
        return render_template('patient.html')
    elif(pressed == 'patient-family'):
        return render_template('family.html')
    elif(pressed == 'patient-rooms'):
        return render_template('room.html')
    elif(pressed == 'patient-payment'):
        return render_template('summary.html')
    else:
        return render_template('base.html')

@app.route('/home/faculty-options', methods=['POST'])
def faculty_options():
    pressed = request.form.get('bt')
    if(pressed == 'faculty-table'):
        return render_template('faculty.html')
    elif(pressed == 'faculty-assign'):
        return render_template('assignment.html')
    else:
        return render_template('base.html')

@app.route('/home/medication-options', methods=['POST'])
def medication_options():
    pressed = request.form.get('bt')
    if(pressed == 'medication-table'):
        return render_template('medication.html')
    elif(pressed == 'medication-patient'):
        return render_template('patientMed.html')
    else:
        return render_template('base.html')

if(__name__ == '__main__'):
    app.run(debug=True)
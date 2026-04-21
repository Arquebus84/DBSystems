from flask import Flask ,render_template, url_for, request
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
    
@app.route('/', methods=['POST', 'GET'])
def index():
    if(request.method == 'POST'):
        # Grab the task and place it into the DB
        return "Hello World"
    else:
        # Otherwise, just view the page
        return render_template('base.html')
    
# @app.route('/patient-contents', methods=['PATIENT', 'FAMILY', 'ROOM', 'PAYMENT'])
# def patientIndex():
#     if(request.method == 'PATIENT'):
#         return 'access patient methods'
#     else:
#         return render_template('base.html')
    

# # @app.route('/familyTable')
# def facultyTable():
#     pass
# # @app.route('/patientRoomTable')
# def facultyTable():
#     pass
# # @app.route('/paymentSummaryTable')
# def facultyTable():
#     pass


# # @app.route('/facultyTable')
# def facultyTable():
#     pass
# # @app.route('/assignmentTable')
# def facultyTable():
#     pass

# # @app.route('/medicationTable')
# def facultyTable():
#     pass
# # @app.route('/patientMedTable')
# def facultyTable():
#     pass

if(__name__ == '__main__'):
    app.run(debug=True)
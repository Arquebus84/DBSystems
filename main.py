from flask import Flask ,render_template, url_for, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy 

import mysql.connector
from flask import Flask

app = Flask(__name__)

try:
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='ithertzwhenIP#1984',
        database='nursingHomeDB'
    )

    cursor = db.cursor()

except mysql.connector.Error as e:
    medications = ["#"]
    print(e)
    
def getPatientTable():
    return 'SELECT p.patientID AS ID, p.firstName AS firstName, p.lastName AS lastName, p.patientPriority AS priority, ' \
    'p.conditionDesc AS conditionDesc, tf.familyLastName AS familyContact ' \
    'FROM patient p JOIN trusted_family tf ' \
    'ON p.familyID = tf.familyID'
def getFamilyTable():
    return 'SELECT tf.familyLastName AS familyName, pn.phoneNumber AS phoneNumber ' \
    'FROM trusted_family tf JOIN phone_number pn WHERE tf.phoneNumberID = pn.numberID'
def getRoomTable():
    return 'SELECT r.patientRoomNumber AS roomNumber, p.firstName AS firstName, p.lastName AS lastName ' \
    'FROM patient_room r JOIN patient p WHERE r.patientID = p.patientID'
def getPaymentTable():
    return 'SELECT ROUND(sum(sys.price * sys.tax * 0.01 + sys.price), 2) AS netPayment, p.firstName AS firstName, p.lastName AS lastName ' \
    'FROM payment_summary psum JOIN patient p JOIN payment_system sys ' \
    'WHERE p.patientID = psum.patientID AND psum.paymentID = sys.paymentID GROUP BY p.firstName, p.lastName'

def getFacultyTable():
    return 'SELECT f.facultyID, f.facultyLastName, ft.facultyType ' \
    'FROM faculty f JOIN faculty_type ft ON f.facultyTypeID = ft.facultyTypeID'
def getAssignTable():
    return 'select f.facultyLastName AS facultyName, p.firstName AS firstName, p.lastName AS lastName, pr.patientRoomNumber AS roomNum, ' \
    'case ' \
    'when (pr.patientRoomNumber >= 3000) then ifnull(ar.floorNumber, 3) ' \
    'when (pr.patientRoomNumber >= 2000) then ifnull(ar.floorNumber, 2) ' \
    'else ifnull(ar.floorNumber, 1) ' \
    'end AS FloorNumber from assigned_room ar ' \
    'join patient_room pr join patient p join faculty f ' \
    'where ar.patientRoomID = pr.patientRoomID AND ar.facultyID = f.facultyID AND pr.patientID = p.patientID'

def getMedicationTable():
    return 'SELECT m.medicationType, p.price, p.tax FROM medication m JOIN payment_system p WHERE p.paymentID = m.paymentID'
def getPatientMedTable():
    return 'SELECT p.firstName AS firstName, p.lastName AS lastName, med.medicationType AS medication ' \
            'FROM patient_med pmed '\
            'JOIN medication med '\
            'JOIN patient p '\
            'WHERE pmed.patientID = p.patientID AND pmed.medicationID = med.medicationID'


#     _medication = StringField("Add Medication")
#     _price = StringField("Add Price")
#     _tax = StringField("Add Tax")
#     _submit = SubmitField("Submit")

@app.route('/')
@app.route('/home')
def index():
    return render_template('base.html')

@app.route('/home/add', methods=['POST', 'GET'])
def addMedication():
    return render_template('medication.html', medications=medications)

    # medType = None
    # form = MedForm()                            #The form in render_template will be equal to this form in this file
    # if(form.validate_on_submit()):
    #     med = Medication.query.filter_by(_medication=form._medication.data).first()
    #     if(med is None):
    #         med = Medication(_medication=form._medication.data)
    #         db.session.add(med)
    #         db.session.commit()
    #     medType = form._medication.data
    #     form._medication.data=''
    #     form._price.data=''
    #     form._tax.data=''
    #     print("Medication Added")
    # medications = Medication.query.group_by(Medication.medType)
    # return render_template('medication.html', 
    #                        form=form,
    #                        medType=medType,
    #                        medications=medications)

# def tableIndex():
#     if(request.method == 'POST'):
#         # Grab the data
#         dbContent = request.form['medication']  # Request the name of the row in medication.html
#         newMed = DatabaseTest(med = dbContent)

#         #Push data into the DB
#         try:
#             db.session.add(newMed)
#             db.session.commit()
#             return redirect('/')
#         except Exception as e:
#             print(e)
#             return 'Issue found when adding new data'
#     else:
#         # Otherwise, just view the page
#         newRow = DatabaseTest.query.order_by(DatabaseTest.id).all()
#         return render_template('medication.html', medication=newRow)

@app.route('/home/patient-options', methods=['POST'])
def patient_options():
    pressed = request.form.get('bt')
    if(pressed == 'patient-table'):
        cursor.execute(getPatientTable())
        patients = cursor.fetchall()
        return render_template('patient.html', patients=patients)
    elif(pressed == 'patient-family'):
        cursor.execute(getFamilyTable())
        family = cursor.fetchall()
        return render_template('family.html', family=family)
    elif(pressed == 'patient-rooms'):
        cursor.execute(getRoomTable())
        room = cursor.fetchall()
        return render_template('room.html', room=room)
    elif(pressed == 'patient-payment'):
        cursor.execute(getPaymentTable())
        summary = cursor.fetchall()
        return render_template('summary.html', summary=summary)
    else:
        return render_template('base.html')

@app.route('/home/faculty-options', methods=['POST'])
def faculty_options():
    pressed = request.form.get('bt')
    if(pressed == 'faculty-table'):
        cursor.execute(getFacultyTable())
        faculty = cursor.fetchall()
        return render_template('faculty.html', faculty=faculty)
    elif(pressed == 'faculty-assign'):
        cursor.execute(getAssignTable())
        assign = cursor.fetchall()
        return render_template('assignment.html', assign=assign)
    else:
        return render_template('base.html')

@app.route('/home/medication-options', methods=['POST'])
def medication_options():
    pressed = request.form.get('bt')
    if(pressed == 'medication-table'):
        cursor.execute(getMedicationTable())
        medications = cursor.fetchall()
        return render_template('medication.html', medications=medications)
    
    elif(pressed == 'medication-patient'):
        cursor.execute(getPatientMedTable())
        patient_medications = cursor.fetchall()
        return render_template('patientMed.html', patient_medications=patient_medications)
    
    else:
        return render_template('base.html')

if(__name__ == '__main__'):
    app.run(debug=True)

from flask import Flask ,render_template, url_for, request, redirect

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
    
#region Get tables for each button event
def getPatientTable():
    return 'SELECT p.patientID AS ID, p.firstName AS firstName, p.lastName AS lastName, p.patientPriority AS priority, ' \
    'p.conditionDesc AS conditionDesc, tf.familyLastName AS familyContact ' \
    'FROM patient p JOIN trusted_family tf ' \
    'ON p.familyID = tf.familyID'
def getFamilyTable():
    return 'SELECT tf.familyID, tf.familyLastName AS familyName, pn.phoneNumber AS phoneNumber ' \
    'FROM trusted_family tf JOIN phone_number pn WHERE tf.phoneNumberID = pn.numberID'
def getRoomTable():
    return 'SELECT r.patientRoomID, r.patientRoomNumber AS roomNumber, p.firstName AS firstName, p.lastName AS lastName ' \
    'FROM patient_room r JOIN patient p WHERE r.patientID = p.patientID'
def getPaymentTable():
    return 'SELECT ROUND(sum(sys.price * sys.tax * 0.01 + sys.price), 2) AS netPayment, p.firstName AS firstName, p.lastName AS lastName ' \
    'FROM payment_summary psum JOIN patient p JOIN payment_system sys ' \
    'WHERE p.patientID = psum.patientID AND psum.paymentID = sys.paymentID GROUP BY p.firstName, p.lastName'

def getFacultyTable():
    return 'SELECT f.facultyID, f.facultyLastName, ft.facultyType ' \
    'FROM faculty f JOIN faculty_type ft ON f.facultyTypeID = ft.facultyTypeID'
def getFacultyTypeTable():
    return 'SELECT ft.facultyTypeID, ft.facultyType FROM faculty_type ft'
def getAssignTable():
    return 'SELECT ar.patientRoomID, f.facultyLastName AS facultyName, p.firstName AS firstName, p.lastName AS lastName, pr.patientRoomNumber AS roomNum, ' \
    'case ' \
    'when (pr.patientRoomNumber >= 3000) then ifnull(ar.floorNumber, 3) ' \
    'when (pr.patientRoomNumber >= 2000) then ifnull(ar.floorNumber, 2) ' \
    'else ifnull(ar.floorNumber, 1) ' \
    'end AS FloorNumber from assigned_room ar ' \
    'join patient_room pr join patient p join faculty f ' \
    'where ar.patientRoomID = pr.patientRoomID AND ar.facultyID = f.facultyID AND pr.patientID = p.patientID'

def getMedicationTable():
    return 'SELECT m.medicationID, m.medicationType, p.price, p.tax FROM medication m JOIN payment_system p WHERE p.paymentID = m.paymentID'
def getPatientMedTable():
    return 'SELECT p.firstName AS firstName, p.lastName AS lastName, med.medicationType AS medication ' \
            'FROM patient_med pmed '\
            'JOIN medication med '\
            'JOIN patient p '\
            'WHERE pmed.patientID = p.patientID AND pmed.medicationID = med.medicationID'
#endregion

#region Add tuples
def addPatientRow(fName, lName, priority, condition, familyID):
    query = 'INSERT INTO patient (firstName, lastName, patientPriority, conditionDesc, familyID) ' \
    'VALUES (%s, %s, %s, %s, %s)'
    values = [fName, lName, priority, condition, familyID]
    cursor.execute(query, values)
    db.commit()

# def addFacultyRow(facultyLastName, facultyTypeID):
#     query = 'INSERT INTO faculty (facultyLastName, facultyTypeID) VALUES (%s, %s)'
#     values = [facultyLastName, facultyTypeID]
#     cursor.execute(query, values)
#     db.commit()
def addFacultyTypeRow(facultyType):
    query = 'INSERT INTO faculty_type (facultyType) VALUES (%s)'
    values = [facultyType]
    cursor.execute(query, values)
    db.commit()

def addAssignmentRow(patientRoomID, facultyID):
    query = 'INSERT INTO assigned_room (patientRoomID, facultyID) VALUES (%s, %s)'
    values = [patientRoomID, facultyID]
    cursor.execute(query, values)
    db.commit()
#endregion

@app.route('/')
@app.route('/home')
def index():
    return render_template('base.html')

#region oldCode
# @app.route('/home/add', methods=['POST', 'GET'])
# def addMedication():
#     return render_template('medication.html', medications=medications)

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

# TODO: Trash this function
def tableIndex():
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
    pass
#endregion

# Adding new rows
@app.route('/home/patient-options/addPatient', methods=['POST', 'GET'])
def newPatientRow():
    if(request.method == 'POST'):
        patientFName=request.form['fName']
        patientLName=request.form['lName']
        patientPriority=request.form['priority']
        patientCondition=request.form['condition']
        patientFamily=request.form['familyID']
        addPatientRow(patientFName, patientLName, patientPriority, patientCondition, patientFamily)
    cursor.execute(getPatientTable())
    patients = cursor.fetchall()
    cursor.execute(getFamilyTable())
    family = cursor.fetchall()
    return render_template('patient.html', patients=patients, family=family)
@app.route('/home/patient-options/addFamily', methods=['POST', 'GET'])
def newFamilyRow():
    if(request.method == 'POST'):
        pass
@app.route('/home/patient-options/addRoom', methods=['POST', 'GET'])
def newRoomRow():
    if(request.method == 'POST'):
        pass

@app.route('/home/faculty-options/addFaculty', methods=['POST', 'GET'])
# def newFacultyRow():
#     if(request.method == 'POST'):
#         facultyLastName = request.form['facultyLastName']
#         facultyTypeID = request.form['facultyTypeID']
#         addFacultyRow(facultyLastName, facultyTypeID)
#     cursor.execute(getFacultyTable())
#     faculty = cursor.fetchall()
#     cursor.execute(getFacultyTypeTable())
#     facultyType = cursor.fetchall()
#     return render_template('faculty.html', faculty=faculty, facultyType=facultyType)

@app.route('/home/faculty-options/addFacultyType', methods=['POST', 'GET'])
def newFacultyTypeRow():
    if(request.method == 'POST'):
        facultyType=request.form['facultyType']
        addFacultyTypeRow(facultyType)
    cursor.execute(getFacultyTypeTable())
    facultyType = cursor.fetchall()
    return render_template('facultyType.html', facultyType=facultyType)

@app.route('/home/faculty-options/addAssignment', methods=['POST', 'GET'])
def newAssignmentRow():
    if(request.method == 'POST'):
        patientRoomID = request.form['patientRoomID']
        facultyID = request.form['facultyID']
        addAssignmentRow(patientRoomID, facultyID)
    cursor.execute(getAssignTable())
    assign = cursor.fetchall()
    cursor.execute(getRoomTable())
    room = cursor.fetchall()
    cursor.execute(getFacultyTable())
    faculty = cursor.fetchall()
    return render_template('assignment.html', assign=assign, room=room, faculty=faculty)

# Deleting rows
@app.route('/home/faculty-options/deleteFacultyType/<int:id>', methods=['POST', 'GET'])
def deleteFaculty(id):
    # Delete specific row and update the autoincrement to the highest value
    try:
        query1 = 'DELETE FROM faculty WHERE facultyID = %s'
        query2 = 'ALTER TABLE faculty AUTO_INCREMENT = 1'
        values = [id]
        cursor.execute(query1, values)
        cursor.execute(query2)
        db.commit()
    except:
        return "failed to delete"
    
    return redirect('/home')
@app.route('/home/faculty-options/deleteFacultyType/<int:id>', methods=['POST', 'GET'])
def deleteFacultyType(id):
    # Delete specific row and update the autoincrement to the highest value
    try:
        query1 = 'DELETE FROM faculty_type WHERE facultyTypeID = %s'
        query2 = 'ALTER TABLE faculty_type AUTO_INCREMENT = 1'
        values = [id]
        cursor.execute(query1, values)
        cursor.execute(query2)
        db.commit()
    except:
        return "failed to delete"
    
    return redirect('/home')

# Options for each button
@app.route('/home/patient-options', methods=['POST', 'GET'])
def patient_options():
    pressed = request.form.get('bt')
    if(pressed == 'patient-table'):
        cursor.execute(getPatientTable())
        patients = cursor.fetchall()
        cursor.execute(getFamilyTable())
        family = cursor.fetchall()
        return render_template('patient.html', patients=patients, family=family)
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
        cursor.execute(getFacultyTypeTable())
        facultyType = cursor.fetchall()
        return render_template('faculty.html', faculty=faculty, facultyType=facultyType)
    elif(pressed == 'faculty-type-table'):
        cursor.execute(getFacultyTypeTable())
        facultyType = cursor.fetchall()
        return render_template('facultyType.html', facultyType=facultyType)
    elif(pressed == 'faculty-assign'):
        cursor.execute(getAssignTable())
        assign = cursor.fetchall()
        cursor.execute(getRoomTable())
        room = cursor.fetchall()
        cursor.execute(getFacultyTable())
        faculty = cursor.fetchall()
        return render_template('assignment.html', assign=assign, room=room, faculty=faculty)
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

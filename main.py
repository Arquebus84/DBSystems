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
    'ON p.familyID = tf.familyID \
    ORDER BY p.patientID'
def getFamilyTable():
    return 'SELECT tf.familyID, tf.familyLastName AS familyName, pn.phoneNumber AS phoneNumber ' \
    'FROM trusted_family tf JOIN phone_number pn WHERE tf.phoneNumberID = pn.numberID'
def getRoomTable():
    return 'SELECT r.patientRoomID, r.patientRoomNumber AS roomNumber, p.firstName AS firstName, p.lastName AS lastName ' \
    'FROM patient_room r JOIN patient p WHERE r.patientID = p.patientID'
def getPaymentTable():
    return 'SELECT ROUND(sum(sys.price * sys.tax * 0.01 + sys.price), 2) AS netPayment, p.firstName AS firstName, p.lastName AS lastName '\
        'FROM payment_summary psum '\
        'JOIN patient p '\
        'JOIN payment_system sys '\
        'JOIN patient_med pmed ' \
        'WHERE psum.paymentID = sys.paymentID AND pmed.patientID = p.patientID '\
        'GROUP BY p.firstName, p.lastName'

def getFacultyTable():
    return 'SELECT f.facultyID, f.facultyLastName, ft.facultyType ' \
    'FROM faculty f JOIN faculty_type ft ON f.facultyTypeID = ft.facultyTypeID'
def getFacultyTypeTable():
    return 'SELECT ft.facultyTypeID, ft.facultyType FROM faculty_type ft'
def getAssignTable():
    return 'SELECT ar.assignedRoomID, f.facultyLastName AS facultyName, p.firstName AS firstName, p.lastName AS lastName, pr.patientRoomNumber AS roomNum, ' \
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
    return 'SELECT pmed.patientMedID, p.firstName AS firstName, p.lastName AS lastName, med.medicationType AS medication ' \
            'FROM patient_med pmed '\
            'JOIN medication med '\
            'JOIN patient p '\
            'WHERE pmed.patientID = p.patientID AND pmed.medicationID = med.medicationID'
#endregion

#region Add tuples
def addPatientRow(firstName, lastName, priority, condition, familyID):
    query = 'INSERT INTO patient (firstName, lastName, patientPriority, conditionDesc, familyID) ' \
    'VALUES (%s, %s, %s, %s, %s)'
    values = [firstName, lastName, priority, condition, familyID]
    cursor.execute(query, values)
    db.commit()
def addFamilyRow(familyLastName, phoneNumber):
    # Update the phone number table to account for matching numbers
    numberID = None
    query1 = 'SELECT numberID from phone_number WHERE phone_number.phoneNumber = %s'
    value = [phoneNumber]
    cursor.execute(query1, value)
    for x in cursor:
        numberID = str(x[0])
    if (numberID is None):
        cursor.fetchall()
        query2 = 'INSERT IGNORE INTO phone_number (phoneNumber) VALUES (%s)'
        cursor.execute(query2, value)
        cursor.fetchall()
        cursor.execute(query1, value)
        for n in cursor:
            numberID = str(n[0])
    cursor.fetchall()
    query3 = 'INSERT INTO trusted_family (familyLastName, phoneNumberID) VALUES (%s, %s)'
    value2 = [familyLastName, numberID]
    cursor.execute(query3, value2)
    db.commit()
def addRoomRow(patientRoomNumber, patientID):
    query = 'INSERT INTO patient_room (patientRoomNumber, patientID) VALUES (%s, %s)'
    values = [patientRoomNumber, patientID]
    cursor.execute(query, values)
    db.commit()
def addFacultyRow(facultyLastName, facultyTypeID):
    query = 'INSERT INTO faculty (facultyLastName, facultyTypeID) VALUES (%s, %s)'
    values = [facultyLastName, facultyTypeID]
    cursor.execute(query, values)
    db.commit()
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
def addMedicationRow(medicationType, price, tax):
    ID = None
    query2 = None
    # Check if the price and tax already exist
    query1='SELECT paymentID from payment_system WHERE price = %s AND tax = %s'
    values1 = [price, tax]
    cursor.execute(query1, values1)
    for x in cursor:
        ID = str(x[0])  #Grab the first data, paymentID
    if(ID == None):
        cursor.fetchall()
        query2 = 'INSERT IGNORE INTO payment_system (price, tax) VALUES (%s, %s)'
        cursor.execute(query2, values1)
        for n in cursor:
            ID = str(n[0])
    cursor.fetchall()
    query3='INSERT INTO medication (medicationType, paymentID) VALUES (%s, %s)'
    values2=[medicationType, ID]
    cursor.execute(query3, values2)
    db.commit()
def addPatientMedRow(patientID, medicationID):
    query = 'INSERT INTO patient_med (patientID, medicationID) VALUES (%s, %s)'
    values = [patientID, medicationID]
    cursor.execute(query, values)
    db.commit()
#endregion

# Home Route
@app.route('/')
@app.route('/home')
def index():
    return render_template('base.html')

# Adding new rows
@app.route('/home/patient-options/addPatient', methods=['POST', 'GET'])
def newPatientRow():
    if(request.method == 'POST'):
        patientFName=request.form['firstName']
        patientLName=request.form['lastName']
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
        familyLastName = request.form['familyLastName']
        phoneNumber = request.form['phoneNumber']
        addFamilyRow(familyLastName, phoneNumber)
    cursor.execute(getFamilyTable())
    family=cursor.fetchall()
    return render_template('family.html', family=family)
@app.route('/home/patient-options/addRoom', methods=['POST', 'GET'])
def newRoomRow():
    if(request.method == 'POST'):
        roomNumber = request.form['roomNumber']
        patientID = request.form['patientID']
        addRoomRow(roomNumber, patientID)
    cursor.execute(getRoomTable())
    room = cursor.fetchall()
    cursor.execute(getPatientTable())
    patient = cursor.fetchall()
    return render_template('room.html', room=room, patient=patient)

@app.route('/home/faculty-options/addFaculty', methods=['POST', 'GET'])
def newFacultyRow():
    if(request.method == 'POST'):
        facultyLastName = request.form['facultyLastName']
        facultyTypeID = request.form['facultyTypeID']
        addFacultyRow(facultyLastName, facultyTypeID)
    cursor.execute(getFacultyTable())
    faculty = cursor.fetchall()
    cursor.execute(getFacultyTypeTable())
    facultyType = cursor.fetchall()
    return render_template('faculty.html', faculty=faculty, facultyType=facultyType)

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

@app.route('/home/medication-options/addMedication', methods=['POST', 'GET'])
def newMedicationRow():
    if(request.method == 'POST'):
        medicationType = request.form['medicationType']
        price = request.form['price']
        tax = request.form['tax']
        addMedicationRow(medicationType, price, tax)
    cursor.execute(getMedicationTable())
    medications = cursor.fetchall()
    return render_template('medication.html', medications=medications)

@app.route('/home/medication-options/addPatientMedication', methods=['POST', 'GET'])
def newPatientMed():
    if(request.method == 'POST'):
        patient = request.form['patient']
        medication = request.form['medication']
        addPatientMedRow(patient, medication)
    cursor.execute(getPatientMedTable())
    patient_medications = cursor.fetchall()
    cursor.execute(getPatientTable())
    patients = cursor.fetchall()
    cursor.execute(getMedicationTable())
    medications = cursor.fetchall()
    return render_template('patientMed.html', patient_medications=patient_medications, patients=patients, medications=medications)

# Deleting rows
@app.route('/home/patient-options/deletePatient/<int:id>', methods=['POST', 'GET']) # Possibly modify
def deletePatient(id):
    # Deleting patient will also have to search for patientRoom paymentSummary and patientMed related to the patient 
    # Also search for assigned_room; which depends on patientRoomID (room 1:1 with patient)
    values = [id]
    try:
        # Search for assigned_room
        query0 = 'SELECT patientRoomID FROM patient_room WHERE patientID = %s'
        cursor.execute(query0, values)
        roomID = None
        for x in cursor:
            roomID = x[0]
        cursor.fetchall()
        if(roomID != None):
            query1 = 'DELETE FROM assigned_room WHERE patientRoomID = %s'
            value2 = [roomID]
            cursor.execute(query1, value2)
            cursor.fetchall()
            query2 = 'DELETE FROM patient_room WHERE patientRoomID = %s'
            cursor.execute(query2, value2)
            cursor.fetchall()
        query3 = 'DELETE FROM payment_summary WHERE patientID = %s'
        cursor.execute(query3, values)
        cursor.fetchall()
        query4 = 'DELETE FROM patient_med WHERE patientID = %s'
        cursor.execute(query4, values)
        cursor.fetchall()
        query5 = 'DELETE FROM patient WHERE patientID = %s'
        query6 = 'ALTER TABLE patient AUTO_INCREMENT = 1'
        cursor.execute(query5, values)
        cursor.fetchall()
        cursor.execute(query6)
        db.commit()
    except:
        return "failed to delete"
    return redirect('/home')
@app.route('/home/patient-options/deleteFamily/<int:id>', methods=['POST', 'GET'])
def deleteFamily(id):
    #Delete patients by id if trusted_family is deleted
    try:
        values = [id]
        query0 = 'SELECT patientID FROM patient WHERE familyID = %s'

        query1 = 'DELETE FROM trusted_family WHERE familyID = %s'
        query2 = 'ALTER TABLE trusted_family AUTO_INCREMENT = 1'
        cursor.execute(query1, values)
        cursor.execute(query2)
        db.commit()
    except:
        return 'failed to delete'
    return redirect('/home')
@app.route('/home/patient-options/deleteRoom/<int:id>', methods=['POST', 'GET'])
def deleteRoom(id):
    try:
        query1 = 'DELETE FROM patient_room WHERE patientRoomID = %s'
        query2 = 'ALTER TABLE patient_room AUTO_INCREMENT = 1'
        values = [id]
        cursor.execute(query1, values)
        cursor.execute(query2)
        db.commit()
    except:
        return 'failed to delete'

@app.route('/home/faculty-options/deleteFaculty/<int:id>', methods=['POST', 'GET'])
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
@app.route('/home/faculty-options/deleteAssignment/<int:id>', methods=['POST', 'GET']) 
def deleteAssign(id):
    try:
        query1 = 'DELETE FROM assigned_room WHERE assignedRoomID = %s'
        query2 = 'ALTER TABLE assigned_room AUTO_INCREMENT = 1'
        values=[id]
        cursor.execute(query1,values)
        cursor.execute(query2)
        db.commit()
    except:
        return 'failed to delete'

@app.route('/home/medication-options/deleteMedication/<int:id>', methods=['POST', 'GET']) 
def deleteMedication(id):
    # Delete specific row and update the autoincrement to the highest value
    try:
        query1 = 'DELETE FROM medication WHERE medicationID = %s'
        query2 = 'ALTER TABLE medication AUTO_INCREMENT = 1'
        values = [id]
        cursor.execute(query1, values)
        cursor.execute(query2)
        db.commit()
    except:
        return "failed to delete"
    
    return redirect('/home')

@app.route('/home/medication-options/deletePatientMedication/<int:id>', methods=['POST', 'GET'])
def deletePatientMed(id):
    try:
        query1 = 'DELETE FROM patient_med WHERE patientMedID = %s'
        query2 = 'ALTER TABLE patient_med AUTO_INCREMENT = 1'
        values = [id]
        cursor.execute(query1, values)
        cursor.execute(query2)
        db.commit()
    except:
        return 'failed to delete'

# Navigation Options for each button ==> Opens each table
# region options
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
        cursor.execute(getPatientTable())
        patient = cursor.fetchall()
        return render_template('room.html', room=room, patient=patient)
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
        cursor.execute(getPatientTable())
        patients = cursor.fetchall()
        cursor.execute(getMedicationTable())
        medications = cursor.fetchall()
        return render_template('patientMed.html', patient_medications=patient_medications, patients=patients, medications=medications)
    
    else:
        return render_template('base.html')
# endregion

if(__name__ == '__main__'):
    app.run(debug=True)

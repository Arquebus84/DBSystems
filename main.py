from flask import Flask ,render_template, url_for, request, redirect
from model.database import dbConnect

import controller.InsertControls.InsertRows 
import controller.getControls.GetTables

# Connect with Flask
app = Flask(__name__)

# Connect to DB
db = dbConnect()
cursor = db.cursor()

# Get table commands
getTable = controller.getControls.GetTables
addRow = controller.InsertControls.InsertRows

# Home Route
@app.route('/')
@app.route('/home')
def index():
    return render_template('base.html')

# Navigation Options for each button ==> Opens each table
# region options
@app.route('/home/patient-options', methods=['POST', 'GET'])
def patient_options():
    pressed = request.form.get('bt')
    if(pressed == 'patient-table'):
        cursor.execute(getTable.getPatientTable())
        patients = cursor.fetchall()
        cursor.execute(getTable.getAllFamilyTable())
        family = cursor.fetchall()
        return render_template('patient.html', patients=patients, family=family)
    elif(pressed == 'patient-family'):
        cursor.execute(getTable.getFamilyTable())
        family = cursor.fetchall()
        return render_template('family.html', family=family)
    elif(pressed == 'patient-rooms'):
        cursor.execute(getTable.getRoomTable())
        room = cursor.fetchall()
        cursor.execute(getTable.getPatientTable())
        patient = cursor.fetchall()
        return render_template('room.html', room=room, patient=patient)
    elif(pressed == 'patient-payment'):
        cursor.execute(getTable.getPaymentTable())
        summary = cursor.fetchall()
        return render_template('summary.html', summary=summary)
    else:
        return render_template('base.html')

@app.route('/home/faculty-options', methods=['POST'])
def faculty_options():
    pressed = request.form.get('bt')
    if(pressed == 'faculty-table'):
        cursor.execute(getTable.getFacultyTable())
        faculty = cursor.fetchall()
        cursor.execute(getTable.getFacultyTypeTable())
        facultyType = cursor.fetchall()
        return render_template('faculty.html', faculty=faculty, facultyType=facultyType)
    elif(pressed == 'faculty-type-table'):
        cursor.execute(getTable.getFacultyTypeTable())
        facultyType = cursor.fetchall()
        return render_template('facultyType.html', facultyType=facultyType)
    elif(pressed == 'faculty-assign'):
        cursor.execute(getTable.getAssignTable())
        assign = cursor.fetchall()
        cursor.execute(getTable.getRoomTable())
        room = cursor.fetchall()
        cursor.execute(getTable.getFacultyTable())
        faculty = cursor.fetchall()
        return render_template('assignment.html', assign=assign, room=room, faculty=faculty)
    else:
        return render_template('base.html')

@app.route('/home/medication-options', methods=['POST'])
def medication_options():
    pressed = request.form.get('bt')
    if(pressed == 'medication-table'):
        cursor.execute(getTable.getMedicationTable())
        medications = cursor.fetchall()
        return render_template('medication.html', medications=medications)
    
    elif(pressed == 'medication-patient'):
        cursor.execute(getTable.getPatientMedTable())
        patient_medications = cursor.fetchall()
        cursor.execute(getTable.getPatientTable())
        patients = cursor.fetchall()
        cursor.execute(getTable.getMedicationTable())
        medications = cursor.fetchall()
        return render_template('patientMed.html', patient_medications=patient_medications, patients=patients, medications=medications)
    
    else:
        return render_template('base.html')
# endregion


# Adding new rows
@app.route('/home/patient-options/addPatient', methods=['POST', 'GET'])
def newPatientRow():
    if(request.method == 'POST'):
        patientFName=request.form['firstName']
        patientLName=request.form['lastName']
        patientPriority=request.form['priority']
        patientCondition=request.form['condition']
        patientFamily=request.form['familyID']
        addRow.addPatientRow(patientFName, patientLName, patientPriority, patientCondition, patientFamily)
    cursor.execute(getTable.getPatientTable())
    patients = cursor.fetchall()
    cursor.execute(getTable.getAllFamilyTable())
    family = cursor.fetchall()
    return render_template('patient.html', patients=patients, family=family)

@app.route('/home/patient-options/addFamily', methods=['POST', 'GET'])
def newFamilyRow():
    if(request.method == 'POST'):
        familyLastName = request.form['familyLastName']
        phoneNumber = request.form['phoneNumber']
        addRow.addFamilyRow(familyLastName, phoneNumber)
    cursor.execute(getTable.getFamilyTable())
    family=cursor.fetchall()
    return render_template('family.html', family=family)
@app.route('/home/patient-options/addRoom', methods=['POST', 'GET'])
def newRoomRow():
    if(request.method == 'POST'):
        roomNumber = request.form['roomNumber']
        patientID = request.form['patientID']
        addRow.addRoomRow(roomNumber, patientID)
    cursor.execute(getTable.getRoomTable())
    room = cursor.fetchall()
    cursor.execute(getTable.getPatientTable())
    patient = cursor.fetchall()
    return render_template('room.html', room=room, patient=patient)

@app.route('/home/faculty-options/addFaculty', methods=['POST', 'GET'])
def newFacultyRow():
    if(request.method == 'POST'):
        facultyLastName = request.form['facultyLastName']
        facultyTypeID = request.form['facultyTypeID']
        addRow.addFacultyRow(facultyLastName, facultyTypeID)
    cursor.execute(getTable.getFacultyTable())
    faculty = cursor.fetchall()
    cursor.execute(getTable.getFacultyTypeTable())
    facultyType = cursor.fetchall()
    return render_template('faculty.html', faculty=faculty, facultyType=facultyType)

@app.route('/home/faculty-options/addFacultyType', methods=['POST', 'GET']) 
def newFacultyTypeRow():
    if(request.method == 'POST'):
        facultyType=request.form['facultyType']
        addRow.addFacultyTypeRow(facultyType)
    cursor.execute(getTable.getFacultyTypeTable())
    facultyType = cursor.fetchall()
    return render_template('facultyType.html', facultyType=facultyType)

@app.route('/home/faculty-options/addAssignment', methods=['POST', 'GET'])
def newAssignmentRow():
    if(request.method == 'POST'):
        patientRoomID = request.form['patientRoomID']
        facultyID = request.form['facultyID']
        addRow.addAssignmentRow(patientRoomID, facultyID)
    cursor.execute(getTable.getAssignTable())
    assign = cursor.fetchall()
    cursor.execute(getTable.getRoomTable())
    room = cursor.fetchall()
    cursor.execute(getTable.getFacultyTable())
    faculty = cursor.fetchall()
    return render_template('assignment.html', assign=assign, room=room, faculty=faculty)

@app.route('/home/medication-options/addMedication', methods=['POST', 'GET'])
def newMedicationRow():
    if(request.method == 'POST'):
        medicationType = request.form['medicationType']
        price = request.form['price']
        tax = request.form['tax']
        addRow.addMedicationRow(medicationType, price, tax)
    cursor.execute(getTable.getMedicationTable())
    medications = cursor.fetchall()
    return render_template('medication.html', medications=medications)

@app.route('/home/medication-options/addPatientMedication', methods=['POST', 'GET'])
def newPatientMed():
    if(request.method == 'POST'):
        patient = request.form['patient']
        medication = request.form['medication']
        addRow.addPatientMedRow(patient, medication)
    cursor.execute(getTable.getPatientMedTable())
    patient_medications = cursor.fetchall()
    cursor.execute(getTable.getPatientTable())
    patients = cursor.fetchall()
    cursor.execute(getTable.getMedicationTable())
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
    
    return render_template('facultyType.html') #redirect('/home/faculty-options')
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

if(__name__ == '__main__'):
    app.run(debug=True)
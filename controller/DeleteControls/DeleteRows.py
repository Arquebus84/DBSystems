from model.database import dbConnect
from flask import Flask ,render_template, url_for, request, redirect, Blueprint


db = dbConnect()
cursor = db.cursor()

delete_bp = Blueprint('delete_bp', __name__)

@delete_bp.route('/home/patient-options/deletePatient/<int:id>', methods=['POST', 'GET']) # Possibly modify
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
    return redirect('/home/patient-options/addPatient')

@delete_bp.route('/home/patient-options/deleteFamily/<int:id>', methods=['POST', 'GET'])
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
    return redirect('/home/patient-options/addFamily')

@delete_bp.route('/home/patient-options/deleteRoom/<int:id>', methods=['POST', 'GET'])
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
    return redirect('/home/patient-options/addRoom')

@delete_bp.route('/home/faculty-options/deleteFaculty/<int:id>', methods=['POST', 'GET'])
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
    return redirect('/home/faculty-options/addFaculty')

@delete_bp.route('/home/faculty-options/deleteFacultyType/<int:id>', methods=['POST', 'GET'])
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
    return redirect('/home/faculty-options/addFacultyType')

@delete_bp.route('/home/faculty-options/deleteAssignment/<int:id>', methods=['POST', 'GET']) 
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
    return redirect('/home/faculty-options/addAssignment')

@delete_bp.route('/home/medication-options/deleteMedication/<int:id>', methods=['POST', 'GET']) 
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
    return redirect('/home/medication-options/addMedication')

@delete_bp.route('/home/medication-options/deletePatientMedication/<int:id>', methods=['POST', 'GET'])
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
    return redirect('/home/medication-options/addPatientMedication')

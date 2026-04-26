from model.database import dbConnect

db = dbConnect()
cursor = db.cursor()


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
        cursor.fetchall()
        cursor.execute(query1, values1)
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
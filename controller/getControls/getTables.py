

def getPatientTable():
    return 'SELECT p.patientID AS ID, p.firstName AS firstName, p.lastName AS lastName, p.patientPriority AS priority, ' \
    'p.conditionDesc AS conditionDesc, tf.familyLastName AS familyContact ' \
    'FROM patient p JOIN trusted_family tf ' \
    'WHERE p.familyID = tf.familyID ' \
    'ORDER BY p.patientID'

def getFamilyTable():
    return 'SELECT tf.familyID, tf.familyLastName AS familyName, pn.phoneNumber AS phoneNumber ' \
    'FROM trusted_family tf JOIN phone_number pn WHERE tf.phoneNumberID = pn.numberID'
def getAllFamilyTable():
    return 'SELECT tf.familyID, tf.familyLastName ' \
    'FROM trusted_family tf ORDER BY tf.familyID'

def getRoomTable():
    return 'SELECT r.patientRoomID, r.patientRoomNumber AS roomNumber, p.firstName AS firstName, p.lastName AS lastName ' \
    'FROM patient_room r JOIN patient p WHERE r.patientID = p.patientID'

def getPaymentTable(): 
    return 'SELECT ROUND(sum(sys.price * sys.tax * 0.01 + sys.price), 2) AS netPayment, p.firstName AS firstName, p.lastName AS lastName '\
        'FROM payment_system sys '\
        'JOIN patient p '\
        'JOIN patient_med pmed ' \
        'JOIN medication med ' \
        'WHERE med.paymentID = sys.paymentID AND pmed.patientID = p.patientID AND pmed.medicationID = med.medicationID '\
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
    return 'SELECT m.medicationID, m.medicationType, p.price, p.tax ' \
    'FROM medication m ' \
    'JOIN payment_system p WHERE p.paymentID = m.paymentID'

def getPatientMedTable():
    return 'SELECT pmed.patientMedID, p.firstName AS firstName, p.lastName AS lastName, med.medicationType AS medication ' \
            'FROM patient_med pmed '\
            'JOIN medication med '\
            'JOIN patient p '\
            'WHERE pmed.patientID = p.patientID AND pmed.medicationID = med.medicationID'

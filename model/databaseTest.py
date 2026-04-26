import mysql.connector
from flask import Flask

app = Flask(__name__)

def check_connection():
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ithertzwhenIP#1984',
            database='nursingHomeDB'
        )
        cursor = db.cursor()
        #region first test
        # ID = None
        # query1= 'Select paymentID, price, tax from payment_system'
        # query2 = 'SELECT paymentID FROM payment_system WHERE price = %s AND tax = %s'
        # values = ('10.5', '1.64')
        # cursor.execute(query2, values)
        # # cursor.fetchall()
        # for x in cursor:
        #     ID = str(x[0])
        #     print(ID)
        # if ID is None:
        #     cursor.fetchall()
        #     query3 = 'Insert IGNORE into payment_system (price, tax) values (%s, %s)'
        #     cursor.execute(query3, values)
        #     cursor.fetchall()
        #     cursor.execute(query1)
        #     for n in cursor:
        #         ID = str(n[0])
        #         print(ID, str(n[1]), str(n[2]))
        # print(ID)
        # for x in cursor:
        #     print(x)
        # db.commit()
        # endregion
        
        #region second test
        # numberID = None
        # query1 = 'SELECT numberID, phoneNumber FROM phone_number WHERE phone_number.phoneNumber = %s'
        # value = ['326-123-9876']
        # cursor.execute(query1, value)
        # # cursor.fetchall()
        # for x in cursor:
        #     numberID = str(x[0])
        # print(numberID)
        # if (numberID is None):
        #     cursor.fetchall()
        #     print('recalculating')
        #     query2 = 'INSERT IGNORE INTO phone_number (phoneNumber) VALUES (%s)'
        #     cursor.execute(query2, value)
        #     cursor.fetchall()
        #     cursor.execute(query1, value)
        #     for c in cursor:
        #         numberID = str(c[0])
        #         print(c)
        #     print(numberID)
        # # cursor.fetchall()
        # # # print(numberID)
        # # query3 = 'INSERT IGNORE INTO trusted_family (familyLastName, phoneNumberID) VALUES (%s, %s)'
        # # value2 = ['Ventura', numberID]
        # # cursor.execute(query3, value2)
        # # cursor.fetchall()
        # # cursor.execute('SELECT familyLastName, phoneNumberID from trusted_family')
        # # for x in cursor:
        # #     print(x)
        # db.commit()
        #endregion

        #region Search for assigned_room
        # values = [5]
        # query0 = 'SELECT patientRoomID FROM patient_room WHERE patientID = %s'
        # cursor.execute(query0, values)
        # roomID = None
        # for x in cursor:
        #     roomID = x[0]
        # print(roomID)
        # if(roomID != None):
        #     query1 = 'DELETE FROM assigned_room WHERE patientRoomID = %s'
        #     value2 = [roomID]
        #     cursor.execute(query1, value2)
        #     cursor.fetchall()
        #     query2 = 'DELETE FROM patient_room WHERE patientRoomID = %s'
        #     cursor.execute(query2, value2)
        #     cursor.fetchall()
        # query3 = 'DELETE FROM payment_summary WHERE patientID = %s'
        # cursor.execute(query3, values)
        # cursor.fetchall()
        # query4 = 'DELETE FROM patient_med WHERE patientID = %s'
        # cursor.execute(query4, values)
        # cursor.fetchall()
        # query5 = 'DELETE FROM patient WHERE patientID = %s'
        # query6 = 'ALTER TABLE patient AUTO_INCREMENT = 1'
        # cursor.execute(query5, values)
        # cursor.fetchall()
        # cursor.execute(query6)
        # db.commit()
        #endregion


        # search for payment system
        medicationType='Ibuprofen'
        price=11.70
        tax=3.1
        ID = None
        query2 = None
        # Check if the price and tax already exist
        query1='SELECT sys.paymentID from payment_system sys WHERE price = %s AND tax = %s'
        values1 = [price, tax]
        cursor.execute(query1, values1)
        for x in cursor:
            ID = x[0]  #Grab the first data, paymentID
        print(ID)
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

        return 'Valid'
    except mysql.connector.Error as e:
        print(e)
        return "Not valid"

check_connection()

# @app.route('/')
# def index():
#     is_connected = check_connection()
#     if(is_connected):
#         return '<h4>Connected Successfully<h4>'
#     else:
#         return '<h4>Not Connected<h4>'
    
# if(__name__ == '__main__'):
#     app.run(debug=True)

# cursor = db.cursor()
# cursor.execute("SELECT f.facultyLastName, ft.facultyType FROM faculty f JOIN faculty_type ft WHERE f.facultyTypeID = ft.facultyTypeID")

# for x in cursor:
#     print(x)
from model.database import dbConnect
from flask import Flask ,render_template, url_for, request, redirect


db = dbConnect()
cursor = db.cursor()


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
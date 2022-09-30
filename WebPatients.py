from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/hospitaldb'
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    name = db.Column(db.String(80), nullable=False)
    phonenumber = db.Column(db.BigInteger(), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bedtype = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    patientstatus = db.Column(db.String(80), nullable=False)

    @staticmethod
    def add_patient(name, phonenumber, age, bedtype, address, state, city, patientstatus):
        new = Patient(name = name, phonenumber = phonenumber,
                      age = age, bedtype = bedtype, address = address,
                      state = state, city = city, patientstatus = patientstatus)
        db.session.add(new)
        db.session.commit()

    @staticmethod
    def get_patient():
        return Patient.query.all()

    @staticmethod
    def get_patient2(phonenumber):
        return Patient.query.filter_by(phonenumber=phonenumber).first()

    @staticmethod
    def delete_patient_by_id(phonenumber):
        mv=Patient.query.filter_by(phonenumber=phonenumber).delete()
        db.session.commit()
        return(mv)

    @staticmethod
    def update_Patient_by_id(id, name, phonenumber, age, bedtype, address, state, city, patientstatus):
        mv = Patient.query.filter_by(phonenumber=phonenumber).first()
        if mv:
            mv.name = name
            mv.phonenumber = phonenumber
            mv.age = age
            mv.bedtype = bedtype
            mv.address = address
            mv.state = state
            mv.city = city
            mv.patientstatus = patientstatus
            db.session.commit()
            return (mv)
        else:
            print("No Patient with this phone num")
            return None

    @staticmethod
    def patient_data(phonenumber=None):
        phone = request.form["phonenumber"]
        patient = Patient.query.filter_by(phonenumber=phonenumber).first()
        patient_data = {}
        if patient:
            patient_data = {'id': patient.id, 'name': patient.name, 'phonenumber': patient.phonenumber,
                            'age': patient.age, 'bedtype': patient.bedtype,
                            'address': patient.address, 'state': patient.state,
                            'city': patient.city, 'patientstatus': patient.patientstatus,
                            }
        return patient_data


#------------------------------------------- Resources ------------------------------------------------------#

# Default page -- Home -- Done
@app.route("/")
def homepage():
    return render_template("home.html")


# Selecting all data -- Done
@app.route("/getAllPatients", methods = ['GET'])
def getAllPatients():
    data = Patient.get_patient()
    return render_template("AllPatients.html", data=data)


# Getting patient data from phonenumber -- Done
@app.route("/get_patient_by_id", methods = ['GET','POST'])
def get_patient_by_id():
    if request.method == 'POST':
        phone = request.form['phonenumber']

        dd = request.get_json()
        data = Patient.get_patient2(dd.phonenumber)
        print(data)
        res=[]
        if data != None:
            res.append({"name":data.name, "phonenumber":data.phonenumber,
                        "age": data.age, "bedtype": data.bedtype, "address": data.address,
                        "state": data.state, "city": data.city, "patientstatus": data.patientstatus})
            return redirect(url_for('FindPatient'))
        else:
            return render_template('FindPatient.html')
    else:
        return render_template('FindPatient.html')


# Inserting data -- Done
@app.route("/register_patient", methods = ['GET','POST'])
def register_patient():
    if request.method == 'POST':
        name = request.form['name']
        phonenumber = request.form['phonenumber']
        age = request.form['age']
        bedtype = request.form['bedtype']
        address = request.form['address']
        state = request.form['state']
        city = request.form['city']
        patientstatus = request.form['patientstatus']

        pat = Patient.query.filter_by(phonenumber=phonenumber).first()

        if pat == None:
            patient = Patient(name=name, phonenumber=phonenumber, age=age, bedtype=bedtype, address=address, state=state,
                               city=city, patientstatus=patientstatus)
            db.session.add(patient)
            db.session.commit()
            #flash('Patient creation initiated successfully')
            return render_template('Register.html')

        else:
            #flash('Patient with this ID already exists')
            return render_template('Register.html')
    else:
        return render_template('Register.html')


# Updating data -- Done
@app.route("/edit_patient", methods = ['GET','POST'])
def edit_patient():
    return render_template("UpdatePatient.html");
    pass

    # if request.method == 'POST':
    #     phonenumber = request.form['phonenumber']
    #
    #     data = Patient.query.filter_by(phonenumber=phonenumber).first()
    #
    #     if data:
    #         patient_data = {'name':data.name, 'phonenumber':data.phonenumber,
    #                 'age':data.age, 'bedtype':data.bedtype, 'address':data.address,
    #                 'state':data.state, 'city':data.city, 'patientstatus':data.patientstatus
    #                 }
    #         return render_template("UpdatePatient.html", update_msg=patient_data)
    #     else:
    #         return render_template("UpdatePatient.html", msg="Patient not Found")


# Deleting data -- Done
@app.route("/delete_patient", methods = ['GET','POST'])
def delete_patient():
    if request.method == 'POST':
        phonenumber = request.form["phonenumber"]
        patient = Patient.query.filter_by(phonenumber=phonenumber).first()

        if patient:
            Patient.query.filter_by(phonenumber=phonenumber).delete()
            db.session.commit()
            #return render_template("DeletePatient.html", msg = patient.name +" Deleted successfully")
            return render_template("DeletePatient.html")
        else:
            #return render_template("DeletePatient.html", msg = "Patient not found")
            return render_template("DeletePatient.html")
    else:
        return render_template("DeletePatient.html")

# Active Patient -- Done
@app.route('/active_patient', methods = ['GET','POST'])
def active_patient():
    # if request.method == 'GET':
    #     patients_list = Patient.get_patient()
    #     active_patients = []
    #
    #     for patient in patients_list:
    #         if patient['patientstatus'] == 'Active':
    #             active_patients.append(patient)
    #     return render_template("ActivePatient.html", patient=active_patients)
    data = Patient.get_patient()
    return render_template("ActivePatient.html", data=data)



if __name__ == "__main__":
    app.run(port=5002)
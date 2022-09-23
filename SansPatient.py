from flask import Flask, request, jsonify
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

#     @staticmethod
#     def put_Patient_by_id(id):
#         mv=Patient.query.filter_by(id=id).put()
#         db.session.commit()
#         return(mv)

    @staticmethod
    def update_Patient_by_id(id, name, phonenumber, age, bedtype, address, state, city, patientstatus):
        mv = Patient.query.filter_by(phonenumber=phonenumber).first()
        mv.name = name
        mv.phonenumber = phonenumber
        mv.age = age
        mv.bedtype = bedtype
        mv.address = address
        mv.state = state
        mv.city = city
        mv.patientstatus = patientstatus
        db.session.commit()
        #return (mv)

class UpdatePatient(Resource):
    def put(self, phonenumber):
        data = request.get_json()
        Patient.update_Patient_by_id(id, data["name"],data["phonenumber"],
                                     data["age"],data["bedtype"],data["address"],
                                     data["state"],data["city"],data["patientstatus"])
        if data:
            data.update({"id":data.get('id'), "name": data.get('name'), "phonenumber":data.get('phonenumber'),
                         "age":data.get('age'),"bedtype":data.get('bedtype'),"address":data.get('address'),
                         "state":data.get('state'),"city":data.get('city'),"patientstatus":data.get('patientstatus')})
            return jsonify({'message': 'Updated', 'status': HTTPStatus.OK})
        else:
            return jsonify({'message':'Not found', 'status':HTTPStatus.NOT_FOUND})

class AllPatients(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        Patient.add_patient(name = data["name"], phonenumber = data["phonenumber"],
                            age = data["age"], bedtype = data["bedtype"], address = data["address"],
                            state = data["state"], city = data["city"], patientstatus = data["patientstatus"])
        return jsonify({'message':'Patient Added', 'status':HTTPStatus.OK})

    def get(self):
        data = Patient.get_patient()
        print(data)
        li = []
        dic = {}
        for i in data:
            li.append({"name":i.name, "phonenumber":i.phonenumber,
                       "age":i.age, "bedtype":i.bedtype, "address":i.address,
                       "state":i.state, "city":i.city, "patientstatus":i.patientstatus})
        return(jsonify(li))


class one_Patient(Resource):
    def delete(self, phonenumber):
        data = Patient.delete_patient_by_id(phonenumber)
        if data:
            return jsonify({'message':'Deleted', 'status':HTTPStatus.OK})
        else:
            return jsonify({'message':'Not found', 'status':HTTPStatus.NOT_FOUND})

    def get(self, phonenumber):
        data = Patient.get_patient2(phonenumber)
        print(data)
        res=[]
        if data != None:
            res.append({"name":data.name, "phonenumber":data.phonenumber,
                        "age": data.age, "bedtype": data.bedtype, "address": data.address,
                        "state": data.state, "city": data.city, "patientstatus": data.patientstatus})
            return(jsonify(res))
        else:
            return jsonify({'message':'Not found', 'status':HTTPStatus.NOT_FOUND})


api.add_resource(AllPatients, "/getAllPatients")
#api.add_resource(AllPatients, "/Register_patient")
api.add_resource(one_Patient, "/Patients/<int:phonenumber>")
api.add_resource(UpdatePatient, "/update_patient/<int:phonenumber>")

if __name__ == "__main__":
    app.run()
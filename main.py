from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination, get_page_parameter
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Datopic123#@localhost/employee'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sdipankar@datopic.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
db = SQLAlchemy(app)


class Employee(db.Model):
    __table_args__ = {'schema': 'public'}
    __tablename__ = 'employees'
    id = db.Column('id', db.Integer, nullable=False, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(40))
    lname = db.Column(db.String(40))
    email = db.Column(db.String(40))
    employee_id=db.Column(db.Integer)

    def __init__(self, fname, lname, email,employee_id):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.employee_id = employee_id

    def update(self, fname=None, lname=None, email=None, employee_id=None):
        self.fname = fname if fname is not None else self.fname
        self.lname = lname if lname is not None else self.lname
        self.email = email if email is not None else self.email
        self.employee_id = employee_id if employee_id is not None else self.employee_id
        db.session.flush()


# class Employee2(db.Model):
#     __table_args__ = {'schema': 'public'}
#     __tablename__ = 'check_login'
#     id = db.Column('id', db.Integer, nullable=False, primary_key=True, foreing_key=True)
#     password = db.column(db.Integer, nullable=False)
#     email = db.column(db.String, nullable=False)
#
#     def __init__(self, id, email, password):
#         self.id = id
#         self.email = email
#         self.password = password
#
#
# @app.route("/details2", methods=["POST"])
# def details2():
#     content = request.json
#     id = content.get('id')
#     email = content.get('email')
#     password = content.get('password')
#
#     check_login = Employee2(id, email, password)
#     db.session.add(check_login)
#     db.session.commit()
#
#     result = db.session.query(Employee2)
#     for res in result:
#         pass
#
#     return "Successfully created row"


@app.route('/details', methods=['POST'])
def details():
    content = request.json
    fname = content.get('fname')
    lname = content.get('lname')
    email = content.get('email')
    employee_id=content.get('employee_id')

    employee = Employee(fname, lname, email,employee_id)
    db.session.add(employee)
    db.session.commit()

    employeeResult = db.session.query(Employee).filter(Employee.id == 3)
    for result in employeeResult:
        print(result.fname)

    return "True"


@app.route('/details/<int:id>', methods=['PUT', 'POST'])
def update_user(id):
    content = request.json
    employeeResult = db.session.query(Employee).filter(Employee.id == id).first()
    if employeeResult is not None:
        employeeResult.update(fname=content.get('fname'), lname=content.get('lname'), email=content.get('email'), employee_id=content.get('employee_id'))
        db.session.commit()
    else:
        return "False"

    return "True"



# @app.route('/details/<int:id>', methods=['GET'])
# def get_user(id):
#     # content = request.json
#     employeeResult = db.session.query(Employee).filter(Employee.id == id).first()
#     if employeeResult is not None:
#         print(employeeResult.fname, employeeResult.fname)
#     else:
#         return "not found"
#
#     return "True"


@app.route('/details/print', methods=['GET'])
def get_user():
    employees = Employee.query.all()
    dc = []
    for employee in employees:
        result = {
            'Employee_id:': employee.id,
            'First_Name:': employee.fname,
            'Last_Name:': employee.lname,
            'Age': employee.age
        }
        dc.append(result)

    return dc


@app.route('/details/fname', methods=['GET'])
def get_user_name():
    employees = Employee.query.all()
    dc = []
    for employee in employees:
        result = {
            'Employee_id:': employee.id,
            'First_Name:': employee.fname,
            'Last_Name:': employee.lname,
            'Age': employee.age
        }

        dc.append(result)
    # print(dc)

    return dc


# @app.route('/details/search', methods=['POST'])
# def search():
#     content=request.json
#     fname = content.get('fname')
#     employees = Employee.query.all()
#     dc = []
#     for employee in employees:
#         # result = {
#         #     'Employee_id:': employee.id,
#         #     'First_Name:': employee.fname,
#         #     'Last_Name:': employee.lname,
#         #     'Age': employee.age
#         # }
#         if fname==employee.fname:
#             dc.append(employee.fname)
#
#     return dc

@app.route('/details/search', methods=['POST'])
def search():
    content = request.json
    fname = content.get('fname')
    pageNumber = content.get('pageNumber')
    PageSize = content.get('PageSize')
    result = Employee.query.filter(Employee.fname.ilike(f'%{fname}%')).order_by(Employee.fname).paginate(
        page=pageNumber, per_page=PageSize)
    # page = request.args.get(get_page_parameter(), type=int, default=1)
    # users = Employee.find(...)
    # pagination = Pagination(page=page, total=users.count(), search=search, record_name='users')
    dc = []
    for employee in result:
        result = {
            'Employee_id:': employee.id,
            'First_Name:': employee.fname,
            'Last_Name:': employee.lname,
            'Age': employee.age
        }

        dc.append(result)

    return dc


@app.route('/details/<int:id>', methods=["DELETE"])
def delete_user(id):
    # content = request.json
    data = db.session.query(Employee).filter(Employee.id == id).first()
    if data is not None:
        db.session.delete(data)
        db.session.commit()

    return "Success"


# @app.route('/details/<string:fname>', methods= ["GET"])
# def list(fname):
#     lst=[]
#     data=db.session.query(Employee).filter(Employee.fname == fname).first()
#     if data is not None:
#         for i in range(data):
#             lst=data
#             print(lst)
#     else:
#         print("EM")
#     return "True"

@app.route("/mail", methods=["GET"])
def index():
    msg = Message('Hello', sender='sdipankar@datopic.com', recipients=['shekhardipankar420@gmail.com'])
    msg.body = "Hello my name is shekhar dipankar work on Datopic."
    mail.send(msg)
    return "Sent"


if __name__ == '__main__':
    app.run(debug=True)

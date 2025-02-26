from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    position = db.Column(db.String(50))
    department = db.Column(db.String(50))
    hire_date = db.Column(db.Date)

db.create_all()

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    new_employee = Employee(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        position=data['position'],
        department=data['department'],
        hire_date=data['hire_date']
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employee added!'}), 201

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([{
        'id': emp.id,
        'first_name': emp.first_name,
        'last_name': emp.last_name,
        'email': emp.email,
        'phone': emp.phone,
        'position': emp.position,
        'department': emp.department,
        'hire_date': emp.hire_date.isoformat()
    } for emp in employees])

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.json
    employee = Employee.query.get_or_404(id)
    employee.first_name = data['first_name']
    employee.last_name = data['last_name']
    employee.email = data['email']
    employee.phone = data['phone']
    employee.position = data['position']
    employee.department = data['department']
    employee.hire_date = data['hire_date']
    db.session.commit()
    return jsonify({'message': 'Employee updated!'})

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted!'})

if __name__ == '__main__':
    app.run(debug=True)

#For Run this app
python app.py

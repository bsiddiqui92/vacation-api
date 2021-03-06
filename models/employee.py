from db import db

class EmployeeModel(db.Model):
	__tablename__ = 'employee'

	employee_id		= db.Column('employee_id', db.Integer, primary_key=True)
	department_id	= db.Column('department_id', db.Integer, db.ForeignKey('department.department_id'))
	first_name		= db.Column('first_name', db.String(30))
	last_name		= db.Column('last_name', db.String(30))
	email			= db.Column('email', db.String(60))

	department = db.relationship('DepartmentModel', \
								primaryjoin='DepartmentModel.department_id==EmployeeModel.department_id')
	
	def __init__(self, 	employee_id=None,
						department_id=None, 
						first=None, 
						last=None, 
						email=None):
		self.employee_id = employee_id
		self.department_id = department_id
		self.first_name = first
		self.last_name = last
		self.email = email

	def json(self):
		return {'employee_id': self.employee_id,
				'department_id': self.department_id, 
				'first_name': self.first_name, 
				'last_name': self.last_name, 
				'email': self.email}
		
	@classmethod
	def find_by_id(cls, _id):
		return cls.query.filter_by(employee_id=_id).first()

	@classmethod
	def find_by_email(cls, email):
		try: 
			return EmployeeModel.query.filter_by(email=email).first()
		except Exception as error:
			raise ValueError(error)


	def insert(self):
		try:
			db.session.add(self)
			db.session.commit()		
		except Exception as error:
			raise ValueError(error)

	# def update(self):

	def delete(self, employee):
		try:
			EmployeeModel.query.filter_by(employee_id=employee).delete()
			db.session.commit()
		except Exception as error:
			raise ValueError(error)
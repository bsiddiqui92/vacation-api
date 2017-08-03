from db import db

class EmployeeModel(db.Model):
	__tablename__ = 'employee'

	employee_id = db.Column('employee_id', db.Integer, primary_key=True)
	first_name = db.Column('first_name', db.String(30))
	last_name = db.Column('last_name', db.String(30))
	email = db.Column('email', db.String(60))

	def __init__(self, first, last, email):
		self.first_name = first
		self.last_name = last
		self.email = email

	@classmethod
	def get_all(cls):
		employees = cls.query.all()
		result = []
		for employee in employees:
			emp = {
				'first_name': employee.first_name, 
				'last_name': employee.last_name, 
				'email': employee.email
			} 
			result.append(emp)

		return result


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

	def delete(self):
		try:
			db.session.delete(self)
			db.session.commit()
		except Exception as error:
			raise ValueError(error)
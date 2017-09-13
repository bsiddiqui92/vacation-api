from db import db

class DepartmentModel(db.Model):
	__tablename__ = 'department'

	department_id		= db.Column('department_id', db.Integer, primary_key=True)
	department_name		= db.Column('department_name', db.String(60))
	department_color	= db.Column('department_color', db.String(20))

	department = db.relationship('EmployeeModel', \
								backref=db.backref('EmployeeModel'), \
								primaryjoin='DepartmentModel.department_id==EmployeeModel.department_id')


	def __init__(self, department_id=None, department_name=None, department_color=None):
		self.department_id = department_id
		self.department_name = department_name
		self.department_color = department_color

	def json(self):
		return {'department_id': self.department_id, 
				'department_name': self.department_name, 
				'department_color': self.department_color}


	
	
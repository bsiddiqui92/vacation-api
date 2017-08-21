from db import db


class RequestModel(db.Model):
	__tablename__ = 'request'

	request_id	= db.Column('request_id', db.Integer, primary_key=True)
	employee_id	= db.Column('employee_id',  db.Integer, db.ForeignKey('employee.employee_id'))
	date_from	= db.Column(db.Date())
	date_until	= db.Column(db.Date())
	time_from	= db.Column(db.Time())
	time_until	= db.Column(db.Time())
	comments	= db.Column(db.String(5000))
	status		= db.Column(db.String(10))

	employee = db.relationship('EmployeeModel', backref=db.backref('EmployeeModel'), primaryjoin='EmployeeModel.employee_id==RequestModel.employee_id')

	def json(self):
		return {'employee_id': self.employee_id, 
				'date_from': self.date_from, 
				'date_until': self.date_until, 
				'time_from': self.time_from, 
				'time_until': self.time_until, 
				'comments': self.comments}

	def __init__(self, employee_id, date_from, date_until, time_from, time_until, comments, status):
		self.employee_id = employee_id
		self.date_from = date_from
		self.date_until = date_until
		self.time_from = time_from
		self.time_until = time_until
		self.comments = comments
		self.status = status

	@classmethod
	def get_request_by_id(cls, request_id):
		try:
			return cls.query.filter_by(request_id=request_id).first()
		except Exception as error:
			raise ValueError(error.message)

	@classmethod
	def get_vacation(cls, status):
		try:
			# if employee_id:
			# 	results = cls.query \
			# 	                .filter_by(status=status) \
			# 	                .filter_by(employee_id=employee_id) \
			# 	                .all()
			# else:
			results = cls.query.filter_by(status=status) \
			                .all()

			requests = []
			for result in results:
				request = {
					"employee_id": result.employee_id,
					"date_from": str(result.date_from), 
					"date_until": str(result.date_until)
				}
				requests.append(request)

			return requests
		except Exception as error:
			raise ValueError(str(error))

	@classmethod
	def get_employee_vacation(cls, employee_id, status):
		if status == 'all':
			return cls.query.filter_by(employee_id=employee_id).all()
		else:
			return cls.query.filter_by(employee_id=employee_id).filter_by(status=status).all()


	def insert(self):
		try:
			db.session.add(self)
			db.session.commit()
		except Exception as error:
			raise ValueError(error)


from db import db


class RequestModel(db.Model):
	__tablename__ = 'request'

	request_id		= db.Column('request_id', db.Integer, primary_key=True)
	employee_id		= db.Column('employee_id',  db.Integer, db.ForeignKey('employee.employee_id'))
	date_from		= db.Column(db.Date())
	date_until		= db.Column(db.Date())
	time_from		= db.Column(db.Time())
	time_until		= db.Column(db.Time())
	comments		= db.Column(db.String(5000))
	status			= db.Column(db.String(10))
	deny_comments 	= db.Column(db.String(5000))

	employee = db.relationship('EmployeeModel', \
								primaryjoin='EmployeeModel.employee_id==RequestModel.employee_id')
								
								

	# department = db.relationship('DepartmentModel', secondary=""\
	# 							 	backref=db.backref('EmployeeModel'),\
	# 							 	primaryjoin='EmployeeModel.employee_id==RequestModel.employee_id')


	def json(self):
		return {'employee_id': self.employee_id, 
				'date_from': self.date_from, 
				'date_until': self.date_until, 
				'time_from': self.time_from, 
				'time_until': self.time_until, 
				'comments': self.comments, 
				'status': self.status,
				'deny_comments': self.deny_comments}

	def __init__(self, employee_id, date_from, date_until, time_from, time_until, comments, status, deny_comments=None):
		self.employee_id = employee_id
		self.date_from = date_from
		self.date_until = date_until
		self.time_from = time_from
		self.time_until = time_until
		self.comments = comments
		self.status = status
		self.deny_comments = deny_comments

	@classmethod
	def get_request_by_id(cls, request_id):
		try:
			return cls.query.filter_by(request_id=request_id).first()
		except Exception as error:
			raise ValueError(error.message)

	@classmethod
	def get_vacation(cls, status):
		try:
			if status == 'all':
				results = db.session.execute(	
					'SELECT * FROM request r '
					'INNER JOIN employee e '
					'ON e.employee_id = r.employee_id '
					'INNER JOIN department d '
					'ON d.department_id = e.department_id '    
					'WHERE r.status = "approved" '
					'OR r.status = "pending"' )
			else: 
				results = db.session.execute(	
					"""SELECT * FROM request r 
					INNER JOIN employee e 
					ON e.employee_id = r.employee_id 
					INNER JOIN department d 
					ON d.department_id = e.department_id 
					WHERE r.status= '%s'""" % (status)) 

			db.session.commit()

			#format request data
			requests = []
			for result in results:
				#if pending show with grey color
				if result.status == 'pending': 
					currColor = 'LightSlateGrey'
				else:
					currColor = result.department_color

				conflicts = cls.get_conflicts(	str(result.date_from), \
												str(result.date_until), \
												result.employee_id)
				request = {
					"request_id": result.request_id,
					"title": result.first_name + " "+result.last_name,
					"start": str(result.date_from), 
					"end": str(result.date_until),
					"comments": result.comments,
					"color": currColor, 
					"conflicts": conflicts
				}
				requests.append(request)

			return requests
		except Exception as error:
			raise ValueError(str(error))

	
	@classmethod
	def get_conflicts(cls, start, end, employee):
		start = str(start)
		end = str(end)
		try: 
			results = db.session.execute(
				"""	SELECT * FROM request r
					INNER JOIN employee e 
				   	ON e.employee_id = r.employee_id 
					INNER JOIN department d 
					ON d.department_id = e.department_id
				   	WHERE (r.date_from between '%s' and '%s'
				   	OR r.date_until between '%s' and '%s')
				   	AND r.employee_id <>  %s""" % (start, end, start, end, employee))
			db.session.commit()


			conflicts = []
			for result in results:
				#if pending show with grey color
				if result.status == 'pending': 
					currColor = 'LightSlateGrey'
				else: 
					currColor = result.department_color


				request = {
					"request_id": result.request_id,
					"title": result.first_name + " "+result.last_name,
					"start": str(result.date_from), 
					"end": str(result.date_until),
					"comments": result.comments,
					"color": currColor 
				}
				conflicts.append(request)

			if not conflicts: 
				return 'false'
			else:
				return conflicts
		except Exception as error: 
			raise ValueError(str(error))

	@classmethod
	def get_employee_vacation(cls, employee_id, status):
		if employee_id == None and status == None:
			return cls.query.all()
		elif status == 'all':
			return cls.query.filter_by(employee_id=employee_id).filter_by(status="approved").\
																filter_by(status="pending").\
																all()
		else:
			return cls.query.filter_by(employee_id=employee_id).filter_by(status=status).all()

	def insert(self):
		try:
			db.session.add(self)
			db.session.commit()
		except Exception as error:
			raise ValueError(error)

	@classmethod
	def approve_request(cls, request_id): 
		request = cls.query.filter_by(request_id=request_id).first()
		request.status = 'approved'
		db.session.commit()

	@classmethod
	def deny_request(cls, data): 
	
		if data['request_id']:
			request = cls.query.filter_by(request_id=data['request_id']).first()
			request.status = 'denied'
			request.deny_comments = data['deny_comments']
		else: 
			request = cls.query.filter_by(request_id=request_id).first()
			request.status = 'denied'
		
		db.session.commit()






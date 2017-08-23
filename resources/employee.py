from flask_restful import Resource, reqparse
from models.employee import EmployeeModel
import json


class Employee(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('employee_id',
        type=str,
        required=False,
        help="This field cannot be blank."
    )
	parser.add_argument('first_name',
        type=str,
        required=False,
        help="This field cannot be blank."
    )

	parser.add_argument('last_name',
    	type=str,
        required=False,
        help="This field cannot be blank."
    )
	
	parser.add_argument('email',
        type=str,
        required=False,
        help="This field cannot be blank."
    )


	def get(self, field, value):

		if field == 'id':
			result = EmployeeModel.find_by_id(value)
		elif field == 'email':
			result = EmployeeModel.find_by_email(value)
		else:
			raise ValueError('Incorrect value supplied for field name.')
		
		if result:
			return {"data": {
						"first_name": result.first_name, 
						"last_name": result.last_name, 
						"email": result.email}
					}, 200
		else:
			return {"message": "Could not find user with given email"}, 404

	def post(self):
		try:

			data = Employee.parser.parse_args()

			#check if user already exists in system
			if EmployeeModel.find_by_email(data['email']):
				return {"message": "User with given email already exists"}, 400

			employee = EmployeeModel(data['first_name'], data['last_name'], data['email'])
			employee.insert()

			return {"message": "Employee Added Successfully."}, 201
		except Exception as error:
			return {"message": error}, 500


	def put(self):
		try:
			data = Employee.parser.parse_args()
			employee = EmployeeModel(data['first_name'], data['last_name'], data['email'])
			test = employee.insert()

			return {"message": "Employee Added Successfully."}, 201
		except Exception as error:
			return {"message": error}, 500

	def delete(self):

		try:
			data = Employee.parser.parse_args()
			employee = EmployeeModel()
			test = employee.delete(data['employee_id'])
			return {"message": "Employee Removed Successfully."}, 201
		except Exception as error:
			return {"message": str(error)}, 500


class GetAllEmployees(Resource):

	def get(self):
		try:
			#result = EmployeeModel.get_all(); 
			 return {'items': list(map(lambda x: x.json(), EmployeeModel.query.all()))}
		except Exception as error:
			return {"message": str(error)}, 500

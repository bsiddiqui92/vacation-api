from flask_restful import Resource, reqparse
from models.employee import EmployeeModel


class Employee(Resource):

	def get(self, field, value):
		if field == 'email':
			employee = EmployeeModel.find_by_email(value) 
		elif field == 'id':
		else:

	def post(self, field, value): 
	def put(self, field, value):
	def delete(self, field, value):



class GetEmployee(Resource):

	def get(self, email):
		result = Employee.find_by_email(email)
		return {"data": {
					"first_name": result.first_name, 
					"last_name": result.last_name, 
					"email": result.email}
				}, 200

class AddEmployee(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('email', 
		type=str, 
		required=True, 
		help="This field cannot be blank"
	)

	def post(self):
		data = AddEmployee.parser.parse_args()

		connection = pymysql.connect('localhost', 'root', '', 'vacation')
		cursor = connection.cursor()

		query = "INSERT INTO employee (email) VALUES (?)"
		cursor.execute(query, (data['email']))

		connection.commit()
		connection.close()

		return {"message": "Employee Added Successfully."}, 201


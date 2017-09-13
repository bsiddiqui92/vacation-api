from flask_restful import Resource, reqparse
from models.request import RequestModel
from models.employee import EmployeeModel
from models.department import DepartmentModel


class getAllDepartments(Resource):

	def get(self):
		try:
			#result = EmployeeModel.get_all(); 
			 return {'items': list(map(lambda x: x.json(), DepartmentModel.query.all()))}
		except Exception as error:
			return {"message": str(error)}, 500


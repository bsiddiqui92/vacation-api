from flask_restful import Resource, reqparse
from models.request import RequestModel
#from models.employee import EmployeeModel

class Vacation(Resource): 

    parser = reqparse.RequestParser()
    parser.add_argument('employee_id',
        type=str,
        required=False,
        help="This field cannot be blank."
    )

    parser.add_argument('date_from',
    	type=str,
        required=False,
        help="This field cannot be blank."
    )

    parser.add_argument('date_until',
        type=str,
        required=False,
        help="This field cannot be blank."
    )

    parser.add_argument('time_from',
        type=str,
        required=False,
        help="This field cannot be blank."
    )

    parser.add_argument('time_until',
        type=str,
        required=False,
        help="This field cannot be blank."
    )

    parser.add_argument('status',
        type=str,
        required=False,
        help="This field cannot be blank."
    )

    def get(self, employee_id, status):
        try: 
            if 1:
                final = []
                results = RequestModel.get_employee_vacation(employee_id, status)
                #add all request to return object
                for result in results:
                    temp = {
                        'employee_id': result.employee_id,
                        'date_from': str(result.date_from), 
                        'date_until': str(result.date_until), 
                        'time_from': str(result.time_from), 
                        'time_until': str(result.time_until), 
                        'status': result.status
                    }
                    final.append(temp)
                return {"data": final}, 200
            else:
                return {"message": "Employee with given id does not exist."}, 401
        except Exception as error:
            return {"message": "error"}, 500

    def post(self):
        try:
            data = Vacation.parser.parse_args()
            if (not data['employee_id'] or 
                not data['date_from'] or
                not data['date_until'] or
                not data['time_from'] or
                not data['time_until']):
                return {"message": "Missing required information"}, 401
            else:
                request = RequestModel( data['employee_id'], 
                                        data['date_from'], 
                                        data['date_until'], 
                                        data['time_from'], 
                                        data['time_until'], 
                                        'pending')
                request.insert()
                return {"message": "Successfully created request"}, 200
        except Exception as error:
            return {"message": error.message}, 500

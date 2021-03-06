from flask_restful import Resource, reqparse
from models.request import RequestModel
from models.employee import EmployeeModel
from models.department import DepartmentModel

class Request(Resource): 

    parser = reqparse.RequestParser()
    parser.add_argument('request_id',
        type=str,
        required=False,
        help="This field cannot be blank."
    )
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

    parser.add_argument('comments', 
        type=str, 
        required=False, 
    )

    parser.add_argument('status',
        type=str,
        required=False,
        help="This field cannot be blank."
    )

    parser.add_argument('deny_comments',
        type=str,
        required=False,
        help="This field cannot be blank."
    )


    def get(self, employee_id=None, status=None):
        try: 
            if EmployeeModel.find_by_id(employee_id):
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
                        'comments': result.comments,  
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
            data = Request.parser.parse_args()
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
                                        data['comments'], 
                                        'pending')
                request.insert()
                return {"message": "Successfully created request"}, 200
        except Exception as error:
            return {"message": str(error)}, 500


class AllRequests(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('request_id',
        type=str,
        required=False,
        help="This field cannot be blank."
    )

    def get(self):
        try:
            result = RequestModel.get_vacation('all')
            return result, 200
        except Exception as error:
            return {"message": str(error) }, 500

class ApprovedRequests(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('request_id',
        type=str,
        required=False,
        help="This field cannot be blank."
    )

    def get(self):
        try:
            result = RequestModel.get_vacation('approved')
            return { "data" : result}, 200
        except Exception as error:
            return {"message": str(error) }, 500


class PendingRequests(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('request_id',
        type=str,
        required=False,
        help="This field cannot be blank."
    )

    def get(self):
        try:
            result = RequestModel.get_vacation('pending')
            return { "data" : result}, 200
        except Exception as error:
            return {"message": str(error) }, 500


class DeniedRequests(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('request_id',
        type=str,
        required=False,
        help="This field cannot be blank."
    )

    def get(self):
        try:
            result = RequestModel.get_vacation('denied')
            return { "data" : result}, 200
        except Exception as error:
            return {"message": str(error) }, 500


class ApproveRequest(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('request_id',
        type=str,
        required=False,
        help="This field cannot be blank."
    )

    def get(self, request_id):
        try:
            result = RequestModel.approve_request(request_id)
            return {"message": str(result)}, 200
        except Exception as error:
            return {"message": str(error) }, 500

class DenyRequest(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('request_id',
        type=str,
        required=False,
        help="This field cannot be blank."
    )
    parser.add_argument('deny_comments',
        type=str,
        required=False,
        help="This field cannot be blank."
    )

    def get(self, request_id):
        try:
            result = RequestModel.deny_request(request_id)
            return {"message": str(result)}, 200
        except Exception as error:
            return {"message": str(error) }, 500

    def post(self): 
        try: 
            data = Request.parser.parse_args(); 
            result = RequestModel.deny_request(data); 
            return {"message": str(result)}, 200 
        except Exception as error: 
            return {"message": str(error) }, 500


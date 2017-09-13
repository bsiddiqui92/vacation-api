from flask import Flask
from flask_restful import Api
from flask_cors import CORS, cross_origin

from resources.employee import Employee, GetAllEmployees
from resources.request import Request, ApprovedRequests, PendingRequests, DeniedRequests, AllRequests, ApproveRequest, DenyRequest
from resources.department import getAllDepartments


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
'mysql+pymysql://root:password@vacation.caqe8gzbr7wa.us-east-1.rds.amazonaws.com/vacation'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
CORS(app)

#Employee Related Endpoint
api.add_resource(Employee, '/employee')
api.add_resource(GetAllEmployees, '/employee/all')


#Request Related Endpoint
api.add_resource(Request, '/request/<string:employee_id>/<string:status>', '/request')

api.add_resource(AllRequests, '/requestbystatus/all')
api.add_resource(ApprovedRequests, '/requestbystatus/approved')
api.add_resource(PendingRequests, '/requestbystatus/pending')
api.add_resource(DeniedRequests, '/requestbystatus/denied')

api.add_resource(ApproveRequest, '/approverequest/<string:request_id>')
api.add_resource(DenyRequest, '/denyrequest/<string:request_id>', '/denyrequest/')


# Department Endpoints
api.add_resource(getAllDepartments, '/departments/all') 


if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000, debug=True)  # important to mention debug=True

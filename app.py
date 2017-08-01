from flask import Flask
from flask_restful import Api

from resources.employee import Employee
from resources.vacation import Vacation

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@1538@vacation.caqe8gzbr7wa.us-east-1.rds.amazonaws.com/vacation'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

api.add_resource(Employee, '/employee', '/employee/<string:field>/<string:value>')
api.add_resource(Vacation, '/request/<string:employee_id>/<string:status>', '/request')


if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000, debug=True)  # important to mention debug=True

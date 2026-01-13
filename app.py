from flask import Flask
from database import init_db
from flask_cors import CORS
from config import Config

#Login(class) controller
from controller.login.login import login_bp

#Company(class) controllers
from controller.company.create import company_create_bp
from controller.company.delete import company_delete_bp
from controller.company.get import company_get_bp
from controller.company.update import company_update_bp

#Employee(class) controllers
from controller.employee.create import employee_create_bp
from controller.employee.delete import employee_delete_bp
from controller.employee.get import employee_get_bp
from controller.employee.update import employee_update_bp

#Payroll(class) controllers
from controller.payroll.create import payroll_create_bp
from controller.payroll.delete import payroll_delete_bp
from controller.payroll.get import payroll_get_bp
from controller.payroll.update import payroll_update_bp

def create_app():
    app = Flask(__name__)

    #Loading configuration
    app.config.from_object(Config)

    #CORS
    CORS(app)

    #Logging
    app.logger.setLevel(app.config["LOG_LEVEL"])

    #Initialize database
    init_db(app)

    #Blueprints

    #Login(class)
    app.register_blueprint(login_bp)

    #Company(class)
    app.register_blueprint(company_create_bp)
    app.register_blueprint(company_delete_bp)
    app.register_blueprint(company_get_bp)
    app.register_blueprint(company_update_bp)

    #Employee(class)
    app.register_blueprint(employee_create_bp)
    app.register_blueprint(employee_delete_bp)
    app.register_blueprint(employee_update_bp)
    app.register_blueprint(employee_get_bp)

    #Payroll(class)
    app.register_blueprint(payroll_create_bp)
    app.register_blueprint(payroll_delete_bp)
    app.register_blueprint(payroll_get_bp)
    app.register_blueprint(payroll_update_bp)

    @app.route("/")
    def home():
        return "Welcome to Flask"

    return app

#Runing Flask 
app = create_app()

if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
from flask import current_app
from database import db
from utils.utils import get_employee
from models import Employee
from sqlalchemy.exc import IntegrityError

#Get employee
def get_employee_crud(id):
    try:
        employee = get_employee(id)
        return employee
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

#Get all employees
def get_employees_crud():
    try:
        employees = Employee.query.all()
        db.session.commit()
        return employees

    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

#Get short details (employee)
def get_employees_short_crud():
    try:
        employees = Employee.query.with_entities(Employee.id, Employee.employee_name, Employee.employee_status.value, Employee.employee_department.value).all()
        db.session.commit()
        return employees
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e
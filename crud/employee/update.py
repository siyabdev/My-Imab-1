from flask import current_app
from database import db
from utils.utils import get_employee
from sqlalchemy.exc import IntegrityError
from utils.utils import check_enum_format

#Update employee
def update_employee_crud(id, employee_name, employee_status, employee_department, employee_email, employee_phone_number_main, employee_phone_number_secondary, employee_dob, employee_cnic, employee_gender, employee_address_permanent, employee_address_current):
    employee = get_employee(id)

    if not employee:
        return employee == False
    try:
        #Update any fields provided
        if employee_name:
            employee.employee_name = employee_name
        
        if employee_status:
            employee.employee_status = check_enum_format(employee_status)
        
        if employee_department:
            employee.employee_department = check_enum_format(employee_department)
        
        if employee_email:
            employee.employee_email = employee_email
        
        if employee_phone_number_main:
            employee.employee_phone_number_main = employee_phone_number_main
        
        if employee_phone_number_secondary:
            employee.employee_phone_number_secondary = employee_phone_number_secondary
        
        if employee_dob:
            employee.employee_dob = employee_dob
        
        if employee_cnic:
            employee.employee_cnic = employee_cnic
        
        if employee_gender:
            employee.employee_gender = check_enum_format(employee_gender)
        
        if employee_address_permanent:
            employee.employee_address_permanent = employee_address_permanent
        
        if employee_address_current:
            employee.employee_address_current = employee_address_current

        db.session.commit()

        return employee
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e


from flask import current_app
from database import db
from models import Employee
from sqlalchemy.exc import IntegrityError
from utils.utils import check_enum_format

#Create employee
def create_employee_crud(employee_company_id, employee_name, employee_status, employee_department, employee_email, employee_phone_number_main, employee_phone_number_secondary, employee_dob, employee_cnic, employee_gender, employee_address_permanent, employee_address_current):

    try:
        create_query = Employee(
            employee_company_id = employee_company_id,
            employee_name = employee_name,
            employee_status = check_enum_format(employee_status),
            employee_department = check_enum_format(employee_department),
            employee_email = employee_email,
            employee_phone_number_main = employee_phone_number_main,
            employee_phone_number_secondary = employee_phone_number_secondary,
            employee_dob = employee_dob,
            employee_cnic = employee_cnic,
            employee_gender = check_enum_format(employee_gender),
            employee_address_permanent = employee_address_permanent,
            employee_address_current = employee_address_current
        )

        db.session.add(create_query)
        db.session.commit()

        return create_query

    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

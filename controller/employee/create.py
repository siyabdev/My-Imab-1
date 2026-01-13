from flask import Blueprint, request, jsonify, current_app
from crud.employee.create import create_employee_crud
from utils.utils import verify_employee
from sqlalchemy.exc import IntegrityError
from schemas.employee import CreateEmployeeRequest, EmployeeResponse
from auth import require_auth

employee_create_bp = Blueprint("employee_create_bp", __name__, url_prefix="/employee")

#Create employee
@employee_create_bp.route("/create", methods=["POST"])
@require_auth
def create_employee():
    data = CreateEmployeeRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error. {message}."),400
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400
    
    employee = verify_employee(data.employee_name, data.employee_email, data.employee_cnic)

    if employee:
        current_app.logger.info(f"Employee already exists. '{employee}'")
        return jsonify({
            "code": "EMPLOYEE_ALREADY_EXISTS",
            "message": f"This employee '{employee}' already exists, try a new one."
        }), 403
    
    try:
        new_employee = create_employee_crud(
            employee_company_id = data.employee_company_id,
            employee_name = data.employee_name,
            employee_status = data.employee_status,
            employee_department = data.employee_department,
            employee_email = data.employee_email,
            employee_phone_number_main = data.employee_phone_number_main,
            employee_phone_number_secondary = data.employee_phone_number_secondary,
            employee_dob = data.employee_dob,
            employee_cnic = data.employee_cnic,
            employee_gender = data.employee_gender,
            employee_address_permanent = data.employee_address_permanent,
            employee_address_current = data.employee_address_current
        )

        current_app.logger.info(f"employee {new_employee} created.")
        return jsonify({
            "code": "EMPLOYEE_CREATED",
            "data": EmployeeResponse(new_employee).to_dict()
        }), 201

    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        return jsonify({
            "code": "INTEGRITY_ERROR",
            "message": f"Integrity error occured {error}."
        }), 409

    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        return jsonify({
            "code": "EXCEPTIONAL_ERROR",
            "message": f"Exceptional error occured {e}."
        }), 500


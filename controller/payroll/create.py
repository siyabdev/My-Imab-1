from flask import Blueprint, request, jsonify, current_app
from crud.payroll.create import create_payroll_crud
from utils.utils import get_payroll
from sqlalchemy.exc import IntegrityError
from schemas.payroll import CreatePayrollRequest, PayrollResponse
from auth import require_auth

payroll_create_bp = Blueprint("payroll_create_bp", __name__, url_prefix="/payroll")

#Create payroll
@payroll_create_bp.route("/create", methods=["POST"])
@require_auth
def create_payroll():
    data = CreatePayrollRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error {message}."), 400
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400
    
    payroll = get_payroll(data.employee_id, data.batch_name)

    if payroll: 
        current_app.logger.info(f"Payroll {payroll} already exists.")
        return jsonify({
            "code": "PAYROLL_ALREADY_EXISTS",
            "message": f"This payroll {data.employee_id}, '{data.batch_name}' already exists, try a new one."
        }), 403
    
    try:
        new_payroll = create_payroll_crud(
            employee_id = data.employee_id,
            employee_company_id = data.employee_company_id,
            batch_name = data.batch_name,
            batch_status = data.batch_status,
            employee_basic_salary = data.employee_basic_salary,
            employee_hourly_rate = data.employee_hourly_rate,
            employee_contract_hours = data.employee_contract_hours,
            employee_rota_hours = data.employee_rota_hours,
            employee_worked_hours = data.employee_worked_hours,
            employee_net_hours = data.employee_net_hours,
            employee_over_below = data.employee_over_below,
            employee_lates = data.employee_lates,
            employee_early = data.employee_early,
            employee_leaves = data.employee_leaves,
            employee_score = data.employee_score,
            total_addition = data.total_addition,
            total_deduction = data.total_deduction,
            total_gross = data.total_gross,
            total_tax = data.total_tax,
            employee_total_net = data.employee_total_net,
            total_net_orion = data.total_net_orion
        )

        current_app.logger.info(f"Payroll {new_payroll} created.")
        return jsonify({
            "code": "PAYROLL_CREATED",
            "data": PayrollResponse(new_payroll).to_dict()
        }), 201
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        return jsonify({
            "code": "INTEGRITY_ERROR_OCCURED",
            "message": f"Integrity error occured {error}."
        }), 409
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        return jsonify({
            "code":"EXCEPTIONAL_ERROR_OCCURED",
            "message":f"Exceptional error {e} occured. Please try again."
        })

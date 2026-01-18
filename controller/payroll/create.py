from flask import Blueprint, request, jsonify, current_app
from crud.payroll.create import create_payroll_crud
from sqlalchemy.exc import IntegrityError
from schemas.payroll import CreatePayrollRequest, PayrollResponse
from auth import require_auth
from utils.utils import (
    get_employee,
    get_company,
    get_payroll,
    get_hourly_rate,
    get_over_below,
    get_score,
    get_addition,
    get_deduction,
    get_gross,
    get_tax,
    get_total_net,
    get_net_orion
)

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
    
    # Get employee from database
    employee = get_employee(data.employee_id)
    if not employee:
        current_app.logger.error(f"Employee {data.employee_id} not found.")
        return jsonify({
            "code": "EMPLOYEE_NOT_FOUND",
            "message": f"Employee {data.employee_id} not found."
        }), 404
        
    # Get company from database
    company = get_company(data.company_id)
    if not company:
        current_app.logger.error(f"Company {data.company_id} not found.")
        return jsonify({
            "code": "COMPANY_NOT_FOUND",
            "message": f"Company {data.company_id} not found."
        }), 404
    
    # Get payroll from database
    payroll = get_payroll(data.employee_id, data.batch_name)
    if payroll: 
        current_app.logger.info(f"Payroll {payroll} already exists.")
        return jsonify({
            "code": "PAYROLL_ALREADY_EXISTS",
            "message": f"This payroll {data.employee_id}, '{data.batch_name}' already exists, try a new one."
        }), 403
        
    # Calculations
    employee_hourly_rate = get_hourly_rate(employee.employee_basic_salary, data.employee_contract_hours)
    employee_over_below = get_over_below(data.employee_worked_hours, data.employee_contract_hours)
    employee_score = get_score(data.employee_lates, data.employee_early, data.employee_leaves)
    total_addition = get_addition(employee_over_below, employee_hourly_rate)
    total_deduction = get_deduction(employee_over_below, employee_hourly_rate)
    total_gross = get_gross(employee.employee_basic_salary, total_addition, total_deduction)
    total_tax = get_tax(total_gross)
    employee_total_net = get_total_net(total_gross, total_tax)
    total_net_orion = get_net_orion(total_gross)
    
    try:
        new_payroll = create_payroll_crud(
            employee_id = data.employee_id,
            company_id = data.company_id,
            batch_name = data.batch_name,
            batch_status = data.batch_status,
            employee_basic_salary = employee.employee_basic_salary,
            employee_hourly_rate = employee_hourly_rate,
            employee_contract_hours = data.employee_contract_hours,
            employee_rota_hours = data.employee_rota_hours,
            employee_worked_hours = data.employee_worked_hours,
            employee_net_hours = 0,
            employee_over_below = employee_over_below,
            employee_lates = data.employee_lates,
            employee_early = data.employee_early,
            employee_leaves = data.employee_leaves,
            employee_score = employee_score,
            total_addition = total_addition,
            total_deduction = total_deduction,
            total_gross = total_gross,
            total_tax = total_tax,
            employee_total_net = employee_total_net,
            total_net_orion = total_net_orion
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

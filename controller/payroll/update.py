from flask import Blueprint, request, jsonify, current_app
from crud.payroll.update import update_payroll_crud
from utils.utils import get_payroll
from sqlalchemy.exc import IntegrityError
from schemas.payroll import UpdatePayrollRequest, PayrollResponse
from auth import require_auth

payroll_update_bp = Blueprint("payroll_update_bp", __name__, url_prefix="/payroll")

#Update payroll
@payroll_update_bp.route("/update", methods=["PUT"])
@require_auth
def update_payroll():
    data = UpdatePayrollRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error({"error": f"Schema error {message}."}), 400
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400

    if not data.has_any_updates():
        current_app.logger.error(f"Data {data} missing.")
        return jsonify({
            "code": "DATA_MISSING", 
            "message": f"Required fields for data {data} update are not provided"
        }), 400
    
    payroll = get_payroll(data.employee_id, data.batch_name)
    if not payroll:
        current_app.logger.error(f"Payroll {payroll} not found.")
        return jsonify({
            "code": "PAYROLL_NOT_FOUND", 
            "message": f"Payroll {payroll} not found."
            }), 404

    try:
        updated_payroll = update_payroll_crud(employee_id = data.employee_id, batch_name = data.batch_name, batch_status = data.batch_status, employee_basic_salary = data.employee_basic_salary, employee_hourly_rate = data.employee_hourly_rate, employee_contract_hours = data.employee_contract_hours, employee_rota_hours = data.employee_rota_hours, employee_worked_hours = data.employee_worked_hours, employee_net_hours = data.employee_net_hours,  employee_lates = data.employee_lates, employee_early = data.employee_early, employee_leaves = data.employee_leaves, employee_score = data.employee_score, total_addition = data.total_addition, total_deduction = data.total_deduction, total_gross = data.total_gross, total_tax = data.total_tax, employee_total_net = data.employee_total_net, total_net_orion = data.total_net_orion)
        current_app.logger.info(f"Payroll updated {updated_payroll}.")
        return jsonify({
            "code": "PAYROLL_UPDATED",
            "message": PayrollResponse(updated_payroll).to_dict()
        }), 200
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        return jsonify({
            "code": "INTEGRITY_ERROR",
            "message": f"Integrity error occured {error}."
        }), 409
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        return jsonify({
            "code":"EXCEPTIONAL_ERROR_OCCURED",
            "message":f"Exceptional error {e} occured. Please try again."
        })
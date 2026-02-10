from flask import Blueprint, request, jsonify, current_app
from crud.payroll.update import update_payroll_crud
from sqlalchemy.exc import IntegrityError
from schemas.payroll import UpdatePayrollRequest, PayrollResponse
from auth import require_auth
from utils.utils import (
    verify_payroll,
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
    
    payroll = verify_payroll(data.id)
    if not payroll:
        current_app.logger.error(f"Payroll {payroll} not found.")
        return jsonify({
            "code": "PAYROLL_NOT_FOUND", 
            "message": f"Payroll {payroll} not found."
            }), 404

    #Calculations
    contract_hours = payroll.employee_contract_hours
    rota_hours = payroll.employee_rota_hours
    worked_hours = payroll.employee_worked_hours
    lates = payroll.employee_lates
    early = payroll.employee_early
    leaves = payroll.employee_leaves

    employee_hourly_rate = get_hourly_rate(payroll.employee_basic_salary, contract_hours)
    employee_over_below = get_over_below(worked_hours, contract_hours)
    employee_score = get_score(lates, early, leaves)
    total_addition = get_addition(employee_over_below, employee_hourly_rate)
    total_deduction = get_deduction(employee_over_below, employee_hourly_rate)
    total_gross = get_gross(payroll.employee_basic_salary, total_addition, total_deduction)
    total_tax = get_tax(total_gross)
    employee_total_net = get_total_net(total_gross, total_tax)
    total_net_orion = get_net_orion(total_gross)

    try:
        updated_payroll = update_payroll_crud(
        id=data.id,
        employee_contract_hours=contract_hours,
        employee_rota_hours=rota_hours,
        employee_worked_hours=worked_hours,
        employee_lates=lates,
        employee_early=early,
        employee_leaves=leaves,
        employee_hourly_rate=employee_hourly_rate,
        employee_over_below=employee_over_below,
        employee_score=employee_score,
        total_addition=total_addition,
        total_deduction=total_deduction,
        total_gross=total_gross,
        total_tax=total_tax,
        employee_total_net=employee_total_net,
        total_net_orion=total_net_orion
    )

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
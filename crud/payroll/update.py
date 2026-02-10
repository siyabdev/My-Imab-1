from flask import current_app
from database import db
from sqlalchemy.exc import IntegrityError
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

#Update payroll
def update_payroll_crud(id, employee_contract_hours, employee_rota_hours, employee_worked_hours, employee_lates, employee_early, employee_leaves):
    payroll = verify_payroll(id)

    if not payroll:
        return payroll == False
    try:       
        if employee_contract_hours:
            payroll.employee_contract_hours = employee_contract_hours
        
        if employee_rota_hours:
            payroll.employee_rota_hours = employee_rota_hours
        
        if employee_worked_hours:
            payroll.employee_worked_hours = employee_worked_hours
        
        if employee_lates:
            payroll.employee_lates = employee_lates

        if employee_early:
            payroll.employee_early = employee_early

        if employee_leaves:
            payroll.employee_leaves = employee_leaves

        #Calculations

        payroll.employee_hourly_rate = get_hourly_rate(
            payroll.employee_basic_salary,
            payroll.employee_contract_hours)

        payroll.employee_over_below = get_over_below(
            payroll.employee_worked_hours,
            payroll.employee_contract_hours)

        payroll.employee_score = get_score(
            payroll.employee_lates,
            payroll.employee_early,
            payroll.employee_leaves)

        payroll.total_addition = get_addition(
            payroll.employee_over_below,
            payroll.employee_hourly_rate)

        payroll.total_deduction = get_deduction(
            payroll.employee_over_below,
            payroll.employee_hourly_rate)

        payroll.total_gross = get_gross(
            payroll.employee_basic_salary,
            payroll.total_addition,
            payroll.total_deduction)

        payroll.total_tax = get_tax(payroll.total_gross)

        payroll.employee_total_net = get_total_net(
            payroll.total_gross,
            payroll.total_tax)

        payroll.total_net_orion = get_net_orion(payroll.total_gross)

        db.session.commit()

        return payroll

    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error

    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

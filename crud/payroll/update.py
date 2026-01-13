from flask import current_app
from database import db
from utils.utils import get_payroll
from sqlalchemy.exc import IntegrityError

#Update payroll
def update_payroll_crud(employee_id, batch_name, batch_status, employee_basic_salary, employee_hourly_rate, employee_contract_hours, employee_rota_hours, employee_worked_hours, employee_net_hours, employee_over_below, employee_lates, employee_early, employee_leaves, employee_score, total_addition, total_deduction, total_gross, total_tax, employee_total_net, total_net_orion):
    payroll = get_payroll(employee_id, batch_name)

    if not payroll:
        return payroll == False
    try:
                
        if batch_status:
            payroll.batch_status = batch_status
        
        if employee_basic_salary:
            payroll.employee_basic_salary = employee_basic_salary
        
        if employee_hourly_rate:
            payroll.employee_hourly_rate = employee_hourly_rate
        
        if employee_contract_hours:
            payroll.employee_contract_hours = employee_contract_hours
        
        if employee_rota_hours:
            payroll.employee_rota_hours = employee_rota_hours
        
        if employee_worked_hours:
            payroll.employee_worked_hours = employee_worked_hours

        if employee_net_hours:
            payroll.employee_net_hours = employee_net_hours

        if employee_over_below:
            payroll.employee_over_below = employee_over_below
        
        if employee_lates:
            payroll.employee_lates = employee_lates

        if employee_early:
            payroll.employee_early = employee_early

        if employee_leaves:
            payroll.employee_leaves = employee_leaves

        if employee_score:
            payroll.employee_score = employee_score
        
        if total_addition:
            payroll.total_addition = total_addition

        if total_deduction:
            payroll.total_deduction = total_deduction

        if total_gross:
            payroll.total_gross = total_gross
        
        if total_tax:
            payroll.total_tax = total_tax
        
        if employee_total_net:
            payroll.employee_total_net = employee_total_net

        if total_net_orion:
            payroll.total_net_orion = total_net_orion

        db.session.commit()

        return payroll

    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error

    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

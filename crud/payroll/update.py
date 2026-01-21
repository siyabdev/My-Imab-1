from flask import current_app
from database import db
from utils.utils import verify_payroll
from sqlalchemy.exc import IntegrityError

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

        db.session.commit()

        return payroll

    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error

    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

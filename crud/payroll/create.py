from flask import current_app
from database import db
from models import Payroll
from sqlalchemy.exc import IntegrityError
from utils.utils import check_enum_format

#Create payroll
def create_payroll_crud(employee_id, employee_company_id, batch_name, batch_status, employee_basic_salary, employee_hourly_rate, employee_contract_hours, employee_rota_hours, employee_worked_hours, employee_net_hours, employee_over_below, employee_lates, employee_early, employee_leaves, employee_score, total_addition, total_deduction, total_gross, total_tax, employee_total_net, total_net_orion):

    try:
        create_query = Payroll(
            employee_id = employee_id,
            employee_company_id = employee_company_id,
            batch_name = check_enum_format(batch_name),
            batch_status = batch_status,
            employee_basic_salary = employee_basic_salary,
            employee_hourly_rate = employee_hourly_rate,
            employee_contract_hours = employee_contract_hours,
            employee_rota_hours = employee_rota_hours,
            employee_worked_hours = employee_worked_hours,
            employee_net_hours = employee_net_hours,
            employee_over_below = employee_over_below,
            employee_lates = employee_lates,
            employee_early = employee_early,
            employee_leaves = employee_leaves,
            employee_score = employee_score,
            total_addition = total_addition,
            total_deduction = total_deduction,
            total_gross = total_gross,
            total_tax = total_tax,
            employee_total_net = employee_total_net,
            total_net_orion = total_net_orion
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
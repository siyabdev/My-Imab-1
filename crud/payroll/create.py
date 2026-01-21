from flask import current_app
from database import db
from models import Payroll
from sqlalchemy.exc import IntegrityError
from utils.utils import check_enum_format

#Create payroll
def create_payroll_crud(employee_id, company_id, batch_name, batch_status, employee_contract_hours, employee_rota_hours, employee_worked_hours, employee_lates, employee_early, employee_leaves):

    try:
        create_query = Payroll(
            employee_id = employee_id,
            company_id = company_id,
            batch_name = check_enum_format(batch_name),
            batch_status = batch_status,
            employee_contract_hours = employee_contract_hours,
            employee_rota_hours = employee_rota_hours,
            employee_worked_hours = employee_worked_hours,
            employee_lates = employee_lates,
            employee_early = employee_early,
            employee_leaves = employee_leaves,
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
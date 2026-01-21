from flask import current_app
from database import db
from utils.utils import verify_payroll
from models import Payroll
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

#Get payroll
def get_payroll_crud(id):
    try:
        payroll = verify_payroll(id)
        return payroll
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error

    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

#Get all payrolls
def get_payrolls_crud():
    try:
        #Joinedload for loading Employee and Company data with payrolls
        payrolls = Payroll.query.options(
            joinedload(Payroll.employee),
            joinedload(Payroll.company)
        ).all()
        db.session.commit()
        return payrolls
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error

    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

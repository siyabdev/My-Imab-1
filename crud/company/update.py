from flask import current_app
from database import db
from utils.utils import get_company
from sqlalchemy.exc import IntegrityError

#Update company
def update_company_crud(id, company_name, company_email, company_joined, company_address):
    company = get_company(id)

    if not company:
        return company == False
    try:
        #Update any fields provided
        if company_name:
            company.company_name = company_name
        
        if company_email:
            company.company_email = company_email
        
        if company_joined:
            company.company_joined = company_joined
        
        if company_address:
            company.company_address = company_address

        db.session.commit()

        return company
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e


from flask import current_app
from database import db
from utils.utils import get_company
from models import Company
from sqlalchemy.exc import IntegrityError

#Get company
def get_company_crud(id):
    try:
        company = get_company(id)
        return company
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

#Get all companies
def get_companies_crud():
    try:
        companies = Company.query.all()
        db.session.commit()
        return companies

    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

#Get short details (companies)
def get_companies_short_crud():
    try:
        companies = Company.query.with_entities(Company.id, Company.company_name).all()
        db.session.commit()
        return companies
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e
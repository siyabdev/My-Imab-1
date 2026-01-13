from flask import current_app
from database import db
from models import Company
from sqlalchemy.exc import IntegrityError

#Create company
def create_company_crud(company_name, company_email, company_joined, company_address):

    try:
        create_query = Company(
            company_name = company_name,
            company_email = company_email,
            company_joined = company_joined,
            company_address = company_address
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

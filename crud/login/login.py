from flask import current_app
from models import Login
from sqlalchemy.exc import IntegrityError

#Verifying login
def verify_login(username, password):
    login = Login.query.filter_by(username=username).first()
    
    if not login:
        current_app.logger.info(f"No employee {login }.")
        return None
    
    try:
        if login.password == password:
            current_app.logger.info(f"Employee {login} returned.")
            return login
        
        return None
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e


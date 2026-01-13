from flask import current_app
from models import Company, Employee, Payroll
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

#Get company(class)
def get_company(id):
    company = Company.query.filter_by(id=id).first()
    return company

#Verify company(class)
def verify_company(company_name, company_email):
    company = Company.query.filter_by(company_name=company_name, company_email=company_email).first()
    return company

#Get employee(class)
def get_employee(id):
    employee = Employee.query.filter_by(id=id).first()
    return employee

#Verify employee(class)
def verify_employee(employee_name, employee_email, employee_cnic):
    employee = Employee.query.filter_by(employee_name=employee_name, employee_email=employee_email, employee_cnic=employee_cnic).first()
    return employee

#Verify payroll(class)
def verify_payroll(id):
    payroll = Payroll.query.filter_by(id=id).first()
    return payroll

#Get payroll(class)
def get_payroll(employee_id, batch_name):
    try:
        #Joinedload for loading Employee and Company data with payroll
        payroll = (
            Payroll.query.options(
            joinedload(Payroll.employee),
            joinedload(Payroll.company)).filter_by(employee_id=employee_id, batch_name=batch_name).first()
        )
        return payroll
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error

    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e
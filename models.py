from database import db
from sqlalchemy import UniqueConstraint,CheckConstraint, Enum
from sqlalchemy.orm import relationship
from base import BaseModel
import enum
from datetime import date

#Employee department(enum)
class EmployeeDepartmentEnum(enum.Enum):
    management = "management"
    maintenance = "maintenance"
    covering = "covering"

#Employee gender(enum)
class EmployeeGenderEnum(enum.Enum):
    male = "male"
    female = "female"

#Employee batch name(enum)
class EmployeeBatchNameEnum(enum.Enum):
    contract = "contract"
    intern = "intern"
    regular = "regular"

#Employee status(enum)
class EmployeeStatusEnum(enum.Enum):
    permanent = "permanent"
    probation = "probation"
    trainee = "trainee"

#Login class
class Login(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=True)

    __table_args__ = (
    UniqueConstraint("username", name="unique_employee_username"),
    CheckConstraint("length(username) > 6", name="check_username_min_length"),
    CheckConstraint("length(password) > 8", name="check_password_min_length"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "username": self.username,
            "password": self.password
    }

    @classmethod
    def to_dict_list(cls, logins):
        return [log.to_dict() for log in logins]

#Company class
class Company(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120), nullable=False)
    company_email = db.Column(db.String(120), nullable=False)
    company_joined = db.Column(db.Date, nullable=False)
    company_address = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "company_name": self.company_name,
            "company_email": self.company_email,
            "company_joined": self.company_joined.isoformat(),
            "company_address": self.company_address
    }

    @classmethod
    def to_dict_list(cls, companies):
        return [comp.to_dict() for comp in companies]

#Employee class
class Employee(BaseModel):
    id = db.Column(db.Integer, primary_key = True)
    employee_company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employee_name = db.Column(db.String(120), nullable=False)
    employee_status = db.Column(db.Enum(EmployeeStatusEnum, name="employee_status_enum"), nullable=False)
    employee_department = db.Column(db.Enum(EmployeeDepartmentEnum, name="employee_department_enum"), nullable=False)
    employee_email = db.Column(db.String(120), nullable=False)
    employee_phone_number_main = db.Column(db.String(120), nullable=False)
    employee_phone_number_secondary = db.Column(db.String(120), nullable=True)
    employee_dob = db.Column(db.Date, nullable=False)
    employee_cnic = db.Column(db.String(120), nullable=False)
    employee_gender = db.Column(db.Enum(EmployeeGenderEnum, name="employee_gender_enum"), nullable=False)
    employee_address_permanent = db.Column(db.String(120), nullable=False)
    employee_address_current = db.Column(db.String(120), nullable=False)

    __table_args__ = (
    UniqueConstraint("employee_email", name="unique_employee_email"),
    UniqueConstraint("employee_phone_number_main", name="unique_employee_phone_number_main"),
    UniqueConstraint("employee_cnic", name="unique_employee_cnic")
    )

    def to_dict(self):
        return {
            "id": self.id,
            "employee_company_id": self.employee_company_id,
            "employee_name": self.employee_name,
            "employee_status": self.employee_status.value,
            "employee_department": self.employee_department.value,
            "employee_email": self.employee_email,
            "employee_phone_number_main": self.employee_phone_number_main,
            "employee_phone_number_secondary": self.employee_phone_number_secondary,
            "employee_dob": self.employee_dob.isoformat(),
            "employee_cnic": self.employee_cnic,
            "employee_gender": self.employee_gender.value,
            "employee_address_permanent": self.employee_address_permanent,
            "employee_address_current": self.employee_address_current
    }

    @classmethod
    def to_dict_list(cls, employees):
        return [emp.to_dict() for emp in employees]

#Payroll class
class Payroll(BaseModel):
    id = db.Column(db.Integer, primary_key = True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    batch_name = db.Column(db.Enum(EmployeeBatchNameEnum, name="employee_batch_name_enum"), nullable=False)
    batch_status = db.Column(db.String(120), nullable=False)
    employee_basic_salary = db.Column(db.Integer, nullable=False)
    employee_hourly_rate = db.Column(db.Integer, nullable=False)
    employee_contract_hours = db.Column(db.Float, nullable=False)
    employee_rota_hours = db.Column(db.Float, nullable=False)
    employee_worked_hours = db.Column(db.Float, nullable=False)
    employee_net_hours = db.Column(db.Float, nullable=False)
    employee_over_below = db.Column(db.Float, nullable=False)
    employee_lates = db.Column(db.Integer, nullable=False)
    employee_early = db.Column(db.Integer, nullable=False)
    employee_leaves = db.Column(db.Integer, nullable=False)
    employee_score = db.Column(db.Integer, nullable=False)
    total_addition = db.Column(db.Integer, nullable=False)
    total_deduction = db.Column(db.Integer, nullable=False)
    total_gross = db.Column(db.Integer, nullable=False)
    total_tax = db.Column(db.Integer, nullable=False)
    employee_total_net = db.Column(db.Integer, nullable=False) 
    total_net_orion = db.Column(db.Integer, nullable=False)

    #Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    company = relationship("Company", foreign_keys=[company_id])

    __table_args__ = (
    UniqueConstraint("employee_id", name="unique_employee_id"),
    UniqueConstraint("batch_name", name="unique_batch_name"),
    CheckConstraint("employee_basic_salary >= 0", name="min_employee_basic_salary_check"),
    CheckConstraint("employee_hourly_rate >= 0", name="min_employee_hourly_rate_check"),
    CheckConstraint("employee_contract_hours >= 0", name="min_employee_contract_hours_check"),
    CheckConstraint("employee_rota_hours >= 0", name="min_employee_rota_hours_check"),
    CheckConstraint("employee_worked_hours >= 0", name="min_employee_worked_hours_check"),
    CheckConstraint("employee_net_hours >= 0", name="min_employee_net_hours_check"),
    CheckConstraint("employee_lates >= 0", name="min_employee_lates_check"),
    CheckConstraint("employee_early >= 0", name="min_employee_early_check"),
    CheckConstraint("employee_leaves >= 0", name="min_employee_leaves_check"),
    CheckConstraint("employee_score >= 0", name="min_employee_score_check"),
    CheckConstraint("total_addition >= 0", name="min_total_addition_check"),
    CheckConstraint("total_deduction >= 0", name="min_total_deduction_check"),
    CheckConstraint("total_gross >= 0", name="min_total_gross_check"),
    CheckConstraint("total_tax >= 0", name="min_total_tax_check"),
    CheckConstraint("employee_total_net >= 0", name="min_employee_total_net_check"),
    CheckConstraint("total_net_orion >= 0", name="min_total_net_orion_check"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "company_id": self.company_id,
            "batch_name": self.batch_name.value,
            "batch_status": self.batch_status,
            "employee_basic_salary": self.employee_basic_salary,
            "employee_hourly_rate": self.employee_hourly_rate,
            "employee_contract_hours": float(self.employee_contract_hours),
            "employee_rota_hours": float(self.employee_rota_hours),
            "employee_worked_hours": float(self.employee_worked_hours),
            "employee_net_hours": float(self.employee_net_hours),
            "employee_over_below": float(self.employee_over_below),
            "employee_lates": self.employee_lates,
            "employee_early": self.employee_early,
            "employee_leaves": self.employee_leaves,
            "employee_score": self.employee_score,
            "total_addition": self.total_addition,
            "total_deduction": self.total_deduction,
            "total_gross": self.total_gross,
            "total_tax": self.total_tax,
            "employee_total_net": self.employee_total_net,
            "total_net_orion": self.total_net_orion
    }
    
    @classmethod
    def to_dict_list(cls, payrolls):
        return [pay.to_dict() for pay in payrolls]
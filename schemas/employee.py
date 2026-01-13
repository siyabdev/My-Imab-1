from flask import current_app
import enum

#Employee department(enum)
class EmployeeDepartmentEnum(enum.Enum):
    MANAGEMENT = "management"
    MAINTENANCE = "maintenance"
    COVERING = "covering"

#Employee gender(enum)
class EmployeeGenderEnum(enum.Enum):
    MALE = "male"
    FEMALE = "female"

#Create employee(class) request
class CreateEmployeeRequest:
    def __init__(self, data):
        self.employee_company_id = data.get("employee_company_id"),
        self.employee_name = data.get("employee_name"),
        self.employee_status = data.get("employee_status"),
        self.employee_department = data.get("employee_department"),
        self.employee_email = data.get("employee_email"),
        self.employee_phone_number_main = data.get("employee_phone_number_main"),
        self.employee_phone_number_secondary = data.get("employee_phone_number_secondary"),
        self.employee_dob = data.get("employee_dob"),
        self.employee_cnic = data.get("employee_cnic"),
        self.employee_gender = data.get("employee_gender"),
        self.employee_address_permanent = data.get("employee_address_permanent"),
        self.employee_address_current = data.get("employee_address_current")

    def is_valid(self):
        #Required fields
        if not all([self.employee_company_id, self.employee_name, self.employee_status, self.employee_department, self.employee_email, self.employee_phone_number_main, self.employee_phone_number_secondary, self.employee_dob, self.employee_cnic, self.employee_gender, self.employee_address_permanent, self.employee_address_current]):
            current_app.logger.error("Missing required fields.")
            return False, "Missing required fields."

        #Validate employee department against enum
        if self.employee_department not in [employee_department.value for employee_department in EmployeeDepartmentEnum]:
            current_app.logger.error("Invalid employee department provided.")
            return False, "Invalid employee department provided."
        
        #Validate employee gender against enum
        if self.employee_gender not in [employee_gender.value for employee_gender in EmployeeGenderEnum]:
            current_app.logger.error("Invalid employee gender provided.")
            return False, "Invalid employee gender provided."

        return True, None

#Update employee(class) request
class UpdateEmployeeRequest:
    def __init__(self, data):
        self.id = data.get("id"),
        self.employee_name = data.get("employee_name"),
        self.employee_status = data.get("employee_status"),
        self.employee_department = data.get("employee_department"),
        self.employee_email = data.get("employee_email"),
        self.employee_phone_number_main = data.get("employee_phone_number_main"),
        self.employee_phone_number_secondary = data.get("employee_phone_number_secondary"),
        self.employee_dob = data.get("employee_dob"),
        self.employee_cnic = data.get("employee_cnic"),
        self.employee_gender = data.get("employee_gender"),
        self.employee_address_permanent = data.get("employee_address_permanent"),
        self.employee_address_current = data.get("employee_address_current")

    def is_valid(self):

        if not self.id:
            current_app.logger.error("Employee id missing. Please provide employee id.")
            return False, "Employee id missing. Please provide employee id."

        #Validate employee department against enum
        if self.employee_department not in [employee_department.value for employee_department in EmployeeDepartmentEnum]:
            current_app.logger.error("Invalid employee department provided.")
            return False, "Invalid employee department provided."
        
        #Validate employee gender against enum
        if self.employee_gender not in [employee_gender.value for employee_gender in EmployeeGenderEnum]:
            current_app.logger.error("Invalid employee gender provided.")
            return False, "Invalid employee gender provided."
        
        return True, None

    def has_any_updates(self):
        return any([self.employee_name, self.employee_status, self.employee_department, self.employee_email, self.employee_phone_number_main, self.employee_phone_number_secondary, self.employee_dob, self.employee_cnic, self.employee_gender, self.employee_address_permanent, self.employee_address_current])

#Delete employee(class) request
class DeleteEmployeeRequest:
    def __init__(self, data):
        self.id = data.get("id")

    def is_valid(self):
        if not (self.id):
            current_app.logger.error("Employee ID doesnt exist.")
            return False, "Employee ID doesnt exist."
        
        return True, None

#Employee(class) response
class EmployeeResponse:
    def __init__(self, data):
        self.id = data.id,
        self.employee_company_id = data.employee_company_id,
        self.employee_name = data.employee_name,
        self.employee_status = data.employee_status,
        self.employee_department = data.employee_department,
        self.employee_email = data.employee_email,
        self.employee_phone_number_main = data.employee_phone_number_main,
        self.employee_phone_number_secondary = data.employee_phone_number_secondary,
        self.employee_dob = data.employee_dob,
        self.employee_cnic = data.employee_cnic,
        self.employee_gender = data.employee_gender,
        self.employee_address_permanent = data.employee_address_permanent,
        self.employee_address_current = data.employee_address_current
    
    def is_valid(self):

        if not self.id:
            current_app.logger.error("Employee id missing. Please provide employee id.")
            return False, "Employee id missing. Please provide employee id."

    def to_dict(self):
        return {
        "id": self.id,
        "employee_company_id": self.employee_company_id,
        "employee_name": self.employee_name,
        "employee_status": self.employee_status,
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

#Employee(class) short response
class EmployeeShortResponse:
    def __init__(self, data):
        self.id = data.id,
        self.employee_name = data.employee_name,
        self.employee_status = data.employee_status
        self.employee_department = data.employee_department
    
    def to_dict(self):
        return{
            "id": self.id,
            "employee_name": self.employee_name,
            "employee_status": self.employee_status,
            "employee_department": self.employee_department.value
        }
    @staticmethod
    def from_list(employees):
        return [EmployeeShortResponse(emp).to_dict() for emp in employees]

#Employee(class) list response        
class EmployeeListResponse:
    @staticmethod
    def from_list(employees):
        return [EmployeeResponse(emp).to_dict() for emp in employees]
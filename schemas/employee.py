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
        # Required fields
        if not all([self.employee_company_id, self.employee_name, self.employee_status, self.employee_department, self.employee_email, self.employee_phone_number_main, self.employee_phone_number_secondary, self.employee_dob, self.employee_cnic, self.employee_gender, self.employee_address_permanent, self.employee_address_current]):
            current_app.logger.error("Missing required fields.")
            return False, "Missing required fields."

        # Validate employee department against enum
        if self.employee_department not in [employee_department.value for employee_department in EmployeeDepartmentEnum]:
            current_app.logger.error("Invalid employee department provided.")
            return False, "Invalid employee department provided."

        return True, None

#Update employee(class) request
class UpdateEmployeeRequest:
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

        if not self.username:
            return False, "Username not provided."

        # Validate username length
        if len(self.username) < 6:
            return False, "Username must be at least 6 characters long."

        # Validate password length
        if len(self.password) < 6:
            return False, "Password must be at least 6 characters long."

        # Validate role against enum
        if self.role and self.role not in [role.value for role in RoleType]:
            return False, "Invalid role provided."
        
        return True, None

    def has_any_updates(self):
        return any([self.name, self.email, self.password, self.role])

class DeleteEmployeeRequest:
    def __init__(self, data):
        self.username = data.get("username")

    def is_valid(self):
        if not ([self.username]):
            return False, "No username."
        
        return True, None
    
class EmployeeResponse:
    def __init__(self, employee):
        self.id = employee.id
        self.name = employee.name
        self.email = employee.email
        self.username = employee.username
        self.password = employee.password
        self.role = employee.role.value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "role": self.role
        }

class EmployeeShortResponse:
    def __init__(self, employee):
        self.id= employee.id
        self.name = employee.name
    
    def to_dict(self):
        return{
            "id" : self.id,
            "name" : self.name
        }
    @staticmethod
    def from_list(employees):
        return [EmployeeShortResponse(emp).to_dict() for emp in employees]
        
class EmployeeListResponse:
    @staticmethod
    def from_list(employees):
        return [EmployeeResponse(emp).to_dict() for emp in employees]
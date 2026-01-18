#Create payroll(class) request
class CreatePayrollRequest:
    def __init__(self, data):
        self.employee_id = data.get("employee_id") 
        self.company_id = data.get("company_id")
        self.batch_name = data.get("batch_name")
        self.batch_status = data.get("batch_status", "open")
        self.employee_contract_hours = data.get("employee_contract_hours")
        self.employee_rota_hours = data.get("employee_rota_hours")
        self.employee_worked_hours = data.get("employee_worked_hours")
        self.employee_lates = data.get("employee_lates", 0)
        self.employee_early = data.get("employee_early", 0)
        self.employee_leaves = data.get("employee_leaves", 0)

    def is_valid(self):
        #Required fields
        if not all([self.employee_id, self.company_id, self.batch_name, self.employee_contract_hours, self.employee_rota_hours, self.employee_worked_hours]):
            return False, "Missing required fields."
        
        #Validate fields values
        if self.employee_contract_hours < 0:
            return False, "Employee contract hours should be greater than or equal to 0."        
        if self.employee_rota_hours < 0:
            return False, "Employee rota hours should be greater than or equal to 0."
        if self.employee_worked_hours < 0:
            return False, "Employee worked hours should be greater than or equal to 0."
        if self.employee_lates < 0:
            return False, "Employee lates should be greater than or equal to 0."
        if self.employee_early < 0:
            return False, "Employee early should be greater than or equal to 0."
        if self.employee_leaves < 0:
            return False, "Employee leaves should be greater than or equal to 0."

        return True, None
    
#Update payroll(class) request
class UpdatePayrollRequest:
    def __init__(self, data):
        self.payroll_id = data.get("payroll_id") 
        self.employee_contract_hours = data.get("employee_contract_hours")
        self.employee_rota_hours = data.get("employee_rota_hours")
        self.employee_worked_hours = data.get("employee_worked_hours")
        self.employee_lates = data.get("employee_lates")
        self.employee_early = data.get("employee_early")
        self.employee_leaves = data.get("employee_leaves")

    def is_valid(self):

        if not self.payroll_id:
            return False, "Payroll id missing. Please provide payroll id."
               
        #Validate fields values
        if self.employee_contract_hours and self.employee_contract_hours < 0:
            return False, "Employee contract hours should be greater than or equal to 0."        
        if self.employee_rota_hours  and self.employee_rota_hours < 0:
            return False, "Employee rota hours should be greater than or equal to 0."
        if self.employee_worked_hours and self.employee_worked_hours < 0:
            return False, "Employee worked hours should be greater than or equal to 0."
        if self.employee_lates and self.employee_lates < 0:
            return False, "Employee lates should be greater than or equal to 0."
        if self.employee_early and self.employee_early < 0:
            return False, "Employee early should be greater than or equal to 0."
        if self.employee_leaves and self.employee_leaves < 0:
            return False, "Employee leaves should be greater than or equal to 0."
                
        return True, None
    
    def has_any_updates(self):
        return any([self.employee_contract_hours, self.employee_rota_hours, self.employee_worked_hours, self.employee_lates, self.employee_early, self.employee_leaves])

#Delete payroll(class) request
class DeletePayrollRequest:
    def __init__(self, data):
        self.id = data.get("id")
    
    def is_valid(self):
        if not (self.id):
            return False, "Payroll ID doesnt exist."
        
        return True, None

#Payroll(class) response
class PayrollResponse:
    def __init__(self, data):
        self.id = data.id
        self.employee_id = data.employee_id 
        self.company_id = data.company_id
        self.batch_name = data.batch_name
        self.batch_status = data.batch_status
        self.employee_basic_salary = data.employee_basic_salary
        self.employee_hourly_rate = data.employee_hourly_rate
        self.employee_contract_hours = data.employee_contract_hours
        self.employee_rota_hours = data.employee_rota_hours
        self.employee_worked_hours = data.employee_worked_hours
        self.employee_net_hours = data.employee_net_hours
        self.employee_over_below = data.employee_over_below
        self.employee_lates = data.employee_lates
        self.employee_early = data.employee_early
        self.employee_leaves = data.employee_leaves
        self.employee_score = data.employee_score
        self.total_addition = data.total_addition
        self.total_deduction = data.total_deduction
        self.total_gross = data.total_gross
        self.total_tax = data.total_tax
        self.employee_total_net = data.employee_total_net
        self.total_net_orion = data.total_net_orion

        #Check if employee relationship is loaded
        if getattr(data, 'employee') and data.employee:
            self.employee_name = data.employee.employee_name
            self.employee_status = data.employee.employee_status if data.employee.employee_status else None
            self.employee_department = data.employee.employee_department if data.employee.employee_department else None
        else:
            self.employee_name = None
            self.employee_status = None
            self.employee_department = None
        
        #Check if company relationship is loaded
        if getattr(data, 'company') and data.company:
            self.company_name = data.company.company_name
        else:
            self.company_name = None
    
    def is_valid(self):

        if not self.employee_id:
            return False, "Employee id missing. Please provide employee id."

        if not self.batch_name:
            return False, "Employee batch name missing. Please provide employee batch name."


    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "company_id": self.company_id,
            "batch_name": self.batch_name,
            "batch_status": self.batch_status,
            "employee_name": self.employee_name,
            "employee_status": self.employee_status.value,
            "employee_department": self.employee_department.value,
            "company_name": self.company_name,
            "employee_basic_salary": self.employee_basic_salary,
            "employee_hourly_rate": self.employee_hourly_rate,
            "employee_contract_hours": self.employee_contract_hours,
            "employee_rota_hours": self.employee_rota_hours,
            "employee_worked_hours": self.employee_worked_hours,
            "employee_net_hours": self.employee_net_hours,
            "employee_over_below": self.employee_over_below,
            "employee_lates": self.employee_lates,
            "employee_early": self.employee_early,
            "employee_leaves": self.employee_leaves,
            "employee_score": self.employee_score,
            "total_addition": self.total_addition,
            "total_deduction": self.total_deduction,
            "total_gross": self.total_gross,
            "total_tax": self.total_tax,
            "employee_total_net": self.employee_total_net,
            "total_net_orion": self.total_net_orion,
        }

#Payroll(class) list response
class PayrollListResponse:
    @staticmethod
    def from_list(payrolls):
        return [PayrollResponse(pay).to_dict() for pay in payrolls]
class CreatePayrollRequest:
    def __init__(self, data):
        self.employee_id = data.get("employee_id")
        self.batch = data.get("batch")
        self.basic_salary = data.get("basic_salary")
        self.hourly_rate = data.get("hourly_rate")
        self.monthly_hours = data.get("monthly_hours")
        self.worked_hours = data.get("worked_hours")
        self.early = data.get("early")
        self.late = data.get("late")
        self.leaves = data.get("leaves")
        self.bonus1 = data.get("bonus1")
        self.bonus2 = data.get("bonus2")

    def is_valid(self):
        if not all([self.employee_id, self.batch, self.basic_salary, self.hourly_rate, self.monthly_hours, self.worked_hours, self.early, self.late, self.leaves, self.bonus1, self.bonus2]):
            return False, "Missing required fields."
        
        if len(self.basic_salary) < 0:
            return False, "Basic salary should be greater than 0."
        if len(self.hourly_rate) < 0:
            return False, "Hourly rate should be greater than 0."
        if len(self.monthly_hours) < 0:
            return False, "Monthly hours should be greater than 0."
        if len(self.worked_hours) < 0:
            return False, "Worked hours should be greater than 0."
        
        return True, None

class UpdatePayrollRequest:
    def __init__(self, data):
        self.employee_id = data.get("employee_id")
        self.batch = data.get("batch")
        self.basic_salary = data.get("basic_salary")
        self.hourly_rate = data.get("hourly_rate")
        self.monthly_hours = data.get("monthly_hours")
        self.worked_hours = data.get("worked_hours")
        self.early = data.get("early")
        self.late = data.get("late")
        self.leaves = data.get("leaves")
        self.bonus1 = data.get("bonus1")
        self.bonus2 = data.get("bonus2")

    def is_valid(self):

        if not self.employee_id:
            return False, "Employee ID not provided."
        if not self.batch:
            return False, "Batch not provided."
             
        if len(self.basic_salary or self.hourly_rate or self.monthly_hours or self.worked_hours) < 0:
            return False, "Basic salary, hourly rate, monthly hours or worked hours should be greater than 0."
                
        return True, None
    
    def has_any_updates(self):
        return any([self.basic_salary, self.hourly_rate, self.monthly_hours, self.worked_hours, self.early, self.late, self.leaves, self.bonus1, self.bonus2])

class DeletePayrollRequest:
    def __init__(self, data):
        self.employee_id = data.get("employee_id")
        self.batch = data.get("batch")
    
    def is_valid(self):
        if not ([self.employee_id, self.batch]):
            return False, "No Employee ID and Batch provided."
        
        return True, None

class PayrollResponse:
    def __init__(self, payroll):
        self.id = payroll.id
        self.employee_id = payroll.employee_id
        self.batch = payroll.batch
        self.basic_salary = payroll.basic_salary
        self.hourly_rate = payroll.hourly_rate
        self.monthly_hours = payroll.monthly_hours
        self.worked_hours = payroll.worked_hours
        self.early = payroll.early
        self.late = payroll.late
        self.leaves = payroll.leaves
        self.bonus1 = payroll.bonus1
        self.bonus2 = payroll.bonus2
        # Check if employee relationship is loaded
        if hasattr(payroll, 'employee') and payroll.employee:
            self.employee_name = payroll.employee.employee_name
            self.employee_status = payroll.employee.employee_status
            self.employee_department = payroll.employee.employee_department.value if payroll.employee.employee_department else None
        else:
            self.employee_name = None
            self.employee_status = None
            self.employee_department = None
        
        # Check if company relationship is loaded
        if hasattr(payroll, 'company') and payroll.company:
            self.company_name = payroll.company.company_name
        else:
            self.company_name = None

    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "batch": self.batch,
            "basic_salary": self.basic_salary,
            "hourly_rate": self.hourly_rate,
            "monthly_hours": self.monthly_hours,
            "worked_hours": self.worked_hours,
            "early": self.early,
            "late": self.late,
            "leaves": self.leaves,
            "bonus1": self.bonus1,
            "bonus2": self.bonus2,
            "employee_name": self.employee_name,
            "employee_status": self.employee_status,
            "employee_department": self.employee_department,
            "company_name": self.company_name
        }

class PayrollListResponse:
    @staticmethod
    def from_list(payrolls):
        return [PayrollResponse(pay).to_dict() for pay in payrolls]

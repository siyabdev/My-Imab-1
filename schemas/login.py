#Login(class) request
class LoginRequest:
    def __init__(self, data):
        self.username = data.get("username")
        self.password = data.get("password")
    
    def is_valid(self):
        #Required fields
        if not self.username:
            return False, "Username required for login."
        
        if not self.password:
            return False, "Password required for login."
        
        #Validate fields
        if len(self.username) < 6:
            return False, "Username must be at least 6 characters long."

        if len(self.password) < 6:
            return False, "Password must be at least 6 characters long."
        
        return True, None

#Login(class) response
class LoginResponse:
    def __init__(self, token, employee_id, username):
        self.token = token
        self.employee_id = employee_id
        self.username = username
    
    def to_dict(self):
        return {
            "token": self.token,
            "employee_id": self.employee_id,
            "username": self.username
        }
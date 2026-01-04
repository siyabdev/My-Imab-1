from flask import current_app
import enum

#Create company(class) request 
class CreateCompanyRequest:
    def __init__(self, data):
        self.company_name = data.get("company_name")
        self.company_email = data.get("company_email")
        self.company_joined = data.get("company_joined")
        self.company_address = data.get("company_address")

    def is_valid(self):
        # Required fields
        if not all([self.company_name, self.company_email, self.company_joined, self.company_address]):
            current_app.logger.error("Missing required fields.")
            return False, "Missing required fields."
        
        return True, None

#Update company(class) request
class UpdateCompanyRequest:
    def __init__(self, data):
        self.id = data.get("id")
        self.company_name = data.get("company_name")
        self.company_email = data.get("company_email")
        self.company_joined = data.get("company_joined")
        self.company_address = data.get("company_address")

    def is_valid(self):

        if not self.id:
            current_app.logger.error("Missing required fields.")
            return False, "Company id missing. Please provide company id."
        
        return True, None
    
    def has_any_updates(self):
        return any([self.company_name, self.company_email, self.company_joined, self.company_address])

#Delete company(class) request
class DeleteCompanyRequest:
    def __init__(self, data):
        self = data.get("")

    def is_valid(self):
        if not ([self]):
            return False, ""
        
        return True, None

#Company(class) response
class CompanyResponse:
    def __init__(self, data):
        self.id = data.get("id")
        self.company_name = data.get("company_name")
        self.company_email = data.get("company_email")
        self.company_joined = data.get("company_joined")
        self.company_address = data.get("company_address")

    def to_dict(self):
        return {
            "id": self.id,
            "company_name": self.company_name,
            "company_email": self.company_email,
            "company_joined": self.company_joined.isoformat(),
            "company_address": self.company_address
        }

#Company(class) short response
class CompanyShortResponse:
    def __init__(self, data):
        self.id= data.get("id")
        self.company_name = data.get("company_name")
    
    def to_dict(self):
        return{
            "id": self.id,
            "company_name": self.company_name
        }
    @staticmethod
    def from_list(companies):
        return [CompanyShortResponse(comp).to_dict() for comp in companies]

#Company(class) list response
class CompanyListResponse:
    @staticmethod
    def from_list(companies):
        return [CompanyListResponse(comp).to_dict() for comp in companies]
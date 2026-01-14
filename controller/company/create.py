from flask import Blueprint, request, jsonify, current_app
from crud.company.create import create_company_crud
from utils.utils import verify_company
from sqlalchemy.exc import IntegrityError
from schemas.company import CreateCompanyRequest, CompanyResponse
from auth import require_auth

company_create_bp = Blueprint("company_create_bp", __name__, url_prefix="/company")

#Create company
@company_create_bp.route("/create", methods=["POST"])
@require_auth
def create_company():
    data = CreateCompanyRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error. {message}."),400
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400
    
    company = verify_company(data.company_name, data.company_email)

    if company:
        current_app.logger.info(f"Company already exists. '{company}'")
        return jsonify({
            "code": "COMPANY_ALREADY_EXISTS",
            "message": f"This company '{company}' already exists, try a new one."
        }), 403
    
    try:
        new_company = create_company_crud(
            company_name = data.company_name,
            company_email = data.company_email,
            company_joined = data.company_joined,
            company_address = data.company_address
        )

        current_app.logger.info(f"Company {new_company} created.")
        return jsonify({
            "code": "COMPANY_CREATED",
            "data": CompanyResponse(new_company).to_dict()
        }), 201

    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        return jsonify({
            "code": "INTEGRITY_ERROR",
            "message": f"Integrity error occured {error}."
        }), 409

    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        return jsonify({
            "code": "EXCEPTIONAL_ERROR",
            "message": f"Exceptional error occured {e}."
        }), 500
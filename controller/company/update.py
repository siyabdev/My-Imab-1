from flask import Blueprint, request, jsonify, current_app
from crud.company.update import update_company_crud
from utils.utils import get_company
from sqlalchemy.exc import IntegrityError
from schemas.company import UpdateCompanyRequest, CompanyResponse
from auth import require_auth

company_update_bp = Blueprint("company_update_bp", __name__, url_prefix="/company")

#Update company
@company_update_bp.route("/update", methods=["PUT"])
@require_auth
def update_company():
    data = UpdateCompanyRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error. {message}")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400

    if not data.has_any_updates():
        current_app.logger.error("Data missing.")
        return jsonify({
            "code": "DATA_MISSING", 
            "message": "Required fields for data update are not provided."
        }), 400
    
    company = get_company(data.id)
    if not company:
        current_app.logger.error(f"Company {company} not found.")
        return jsonify({
            "code": "COMPANY_NOT_FOUND", 
            "message": f"Company {company} not found."
        }), 404

    try:        
        updated_company = update_company_crud(id=data.id, company_name = data.company_name, company_email = data.company_email, company_joined = data.company_joined, company_address = data.company_address)
        current_app.logger.info(f"Company updated {updated_company}.")
        return jsonify({
            "code": "COMPANY_UPDATED",
            "data": CompanyResponse(updated_company).to_dict()
        }), 200

    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        return jsonify({
            "code": "INTEGRITY_ERROR",
            "message": f"Integrity error {error} occured."
        }), 409
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        return jsonify({
            "code": "EXCEPTIONAL_ERROR",
            "message": f"Exceptional error {e} occured."
        }), 500
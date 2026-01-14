from flask import Blueprint, request, jsonify, current_app
from crud.company.delete import delete_company_crud
from utils.utils import get_company
from sqlalchemy.exc import IntegrityError
from schemas.company import DeleteCompanyRequest
from auth import require_auth

company_delete_bp = Blueprint("company_delete_bp", __name__, url_prefix="/company")

#Delete company
@company_delete_bp.route("/delete", methods=["DELETE"])
@require_auth
def delete_company():
    data = DeleteCompanyRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error {message}.")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400

    company = get_company(data.id)

    if not company:
        current_app.logger.info(f"Company {company} doesnt exist.")
        return jsonify({
            "code": "COMPANY_DOESNT_EXIST",
            "message": f"Company '{company}' doesnt exist, please enter a valid company ID."
        })

    try:
        delete_query = delete_company_crud(id=data.id)
        if delete_query:
            current_app.logger.info(f"Company '{data.id}' deleted.")
            return jsonify({
                "code": "COMPANY_DELETED",
                "message": f"Company '{data.id}' is deleted."
            }), 200
        
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
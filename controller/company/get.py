from flask import Blueprint, request, jsonify, current_app
from crud.company.get import get_company_crud, get_companies_crud, get_companies_short_crud
from schemas.company import CompanyResponse, CompanyListResponse, CompanyShortResponse
from sqlalchemy.exc import IntegrityError
from auth import require_auth

company_get_bp = Blueprint("company_get_bp", __name__, url_prefix="/company")

#Get company
@company_get_bp.route("/get", methods=["GET"])
@require_auth
def get_company():
    data = request.json
    id = data.get("id")

    if not id:
        current_app.logger.error(f"Wrong company ID '{id}' provided.")
        return jsonify({
            "code": "WRONG_COMPANY_ID_PROVIDED",
            "message": f"Please enter correct company ID '{id}'."
        }), 403
    
    company = get_company_crud(id=id)

    try:
        if company:
            current_app.logger.info(f"Company {company} response returned.")
            return CompanyResponse(company).to_dict()
        
        else:
            current_app.logger.error(f"Company ID '{id}' is not registered.")
            return jsonify({
                "code":"COMPANY_ID_DOESNT_EXIST",
                "message": f"Company ID '{id}' is not registered, please try another."
            }), 403
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        return jsonify({
            "code": "INTEGRITY_ERROR",
            "message": f"Integrity error occured {error}."
        }), 409

    except Exception as e:
            current_app.logger.error(f"Exceptional error {e}.")
            return jsonify({
                "code":"EXCEPTIONAL_ERROR_OCCURED",
                "message":f"Exceptional error {e} occured. please try again."
            })
    

#Get all companies
@company_get_bp.route("/all", methods=["GET"])
@require_auth
def get_all_companies():
     
    try:
         get_companies = get_companies_crud()

         if get_companies:
              current_app.logger.info(f"Companies {get_companies} response returned.")
              return CompanyListResponse.from_list(get_companies)
         else:
            current_app.logger.error("No companies found.")
            return jsonify({
                "code":"NO_COMPANIES_FOUND",
                "message":"No companies found, please add company first."
            })
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        return jsonify({
            "code": "INTEGRITY_ERROR",
            "message": f"Integrity error occured {error}."
        }), 409
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        return jsonify({
            "code":"EXCEPTIONAL_ERROR_OCCURED",
            "message":f"Exceptional error {e} occured. Please try again."
        })

#Get short details (companies)
@company_get_bp.route("/short", methods = ["GET"])
@require_auth
def get_companies_short():

    try:
        companies = get_companies_short_crud()

        if companies:
            current_app.logger.info(f"Companies {companies} response returned.")
            return CompanyShortResponse.from_list(companies)

        else:
            current_app.logger.error("No companies found")
            return jsonify({
                "code":"NO_COMPANIES_FOUND",
                "message":"No companies found, please add company first."
            })
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        return jsonify({
            "code": "INTEGRITY_ERROR",
            "message": f"Integrity error occured {error}."
        }), 409
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        return jsonify({
            "code":"EXCEPTIONAL_ERROR_OCCURED",
            "message":f"Exceptional error {e} occured. Please try again."
        })
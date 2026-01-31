from flask_jwt_extended import get_jwt,verify_jwt_in_request

def auth_user():
    verify_jwt_in_request()  
    claim = get_jwt() or {}

    return claim.get('user')
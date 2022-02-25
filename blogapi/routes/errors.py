from flask import Blueprint
from flask import request, jsonify

error = Blueprint('error', __name__)

@error.errorhandler(404)
def not_found(error):
    return jsonify({"message":"Resource not found"}),404

@error.errorhandler(500)
def internal_server(error):
    return jsonify({"message":"There is a problem"}),500
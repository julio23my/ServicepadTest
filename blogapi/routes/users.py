import os
import uuid
import jwt
import datetime

from flask import request, Blueprint,jsonify
from flask_restful import reqparse
from werkzeug.security import generate_password_hash, check_password_hash

from blogapi.extensions import db
from blogapi.utils.database import get_all, get_one, add_instance, delete_instance, edit_instance, update_instance
from blogapi.models.user import User
from blogapi.utils.serializer import TokenSchema, UserSchema

from blogapi.utils.decorators import token_required


user = Blueprint('user', __name__)




@user.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    
    if not current_user.admin:
        return jsonify({'message' : 'You dont have the privileges of admin'}), 401

    users = get_all(User)
    serializer = UserSchema(many=True)

    output = serializer.dump(users)

    return jsonify( output ), 200


@user.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):
    
    if not current_user.admin:
        return jsonify({'message' : 'You dont have the privileges of admin'}), 401

    user = get_one(model=User, public_id=public_id)
    if not user:
        return jsonify({'message' : 'User not found'}), 404
    serializer = UserSchema(many=True)

    output = serializer.dump(user)

    return jsonify( output ), 200

@user.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'message' : 'You dont have the privileges of admin'}), 401

    data = request.get_json()

    hash_password = generate_password_hash(str(data['password']).encode("utf-8"), method='sha256')
    
    add_new = add_instance(model=User, public_id=str(uuid.uuid4()), name=data['name'], password=hash_password, admin=False)
    if add_new:
        return jsonify({'message' : 'User has been created'}), 201
    else:
        return jsonify({'message' : 'Error during adding the user'}), 400

@user.route('/admin', methods=['POST'])
def create_admin_user():
    
    hash_password = generate_password_hash(str('admin').encode("utf-8"), method='sha256')
    add_new = add_instance(User, public_id=str(uuid.uuid4()), name='name', password=hash_password, admin=True)
    if add_new:
        return jsonify({'message' : 'Admin has been created'}), 201
    else:
        return jsonify({'message' : 'Error during adding the admin'}), 400


@user.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message' : 'You dont have the privileges of admin'}), 401

    edit = update_instance(User, id=public_id ,public_id=public_id, admin=True)

    if edit:
        return jsonify({'message' : 'User has been promoted'}), 200
    else:
        return jsonify({'message' : 'Error during upgrading privileges of admin'}), 400

@user.route('/user/<public_id>', methods=['PATCH'])
@token_required
def edit_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message' : 'You dont have the privileges of admin'}), 401

    data = request.get_json()
    
    edit = edit_instance(User, id=public_id, public_id=public_id, **data)
    if edit:
        return jsonify({'message' : 'User has updated'}), 200
    else:
        return jsonify({'message' : 'Error during updating user'}), 400

@user.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({'message' : 'You dont have the privileges of admin'}), 401

    user = delete_instance(User, public_id=public_id)

    if user:
        return jsonify({'message' : 'User has delete promoted'}), 200
    else:
        return jsonify({'message' : 'Error during delete user'}), 400

@user.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message' : 'Could not verify'}), 401

    user = get_one(User, name=auth.username)

    if not user:
        return jsonify({'message' : 'Could not verify'}), 401

    if check_password_hash(user.password, auth.password):
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = jwt.encode({'public_id' : user.public_id, 'exp' :exp },os.environ.get("SECRET_KEY") , algorithm=os.environ.get("ALGORITHM"))
        answer = {'token':token, 'expire': exp, 'user':user}
        serializer = TokenSchema()
        token_data = serializer.dump(answer)
        return jsonify(token_data), 200

    return jsonify({'message' : 'Could not verify'}), 401



from flask import Blueprint
import uuid
import jwt
import datetime
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from blogapi.models.user import User
from blogapi.extensions import db
import os
from blogapi.utils.decorators import token_required

user = Blueprint('user', __name__)




@user.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    users = User.query.all()

    output = []

    for user in users:
        dic_user = dict()
        dic_user['public_id'] = user.public_id
        dic_user['name'] = user.name
        dic_user['password'] = user.password
        dic_user['admin'] = user.admin
        output.append(dic_user)
    return jsonify({'users':output})


@user.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user,public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No user found'})
    
    dic_user = dict()
    dic_user['public_id'] = user.public_id
    dic_user['name'] = user.name
    dic_user['password'] = user.password
    dic_user['admin'] = user.admin

    return jsonify({'user':dic_user})

@user.route('/user', methods=['POST'])
# @token_required
def create_user():
    # if not current_user.admin:
    #     return jsonify({'message' : 'Cannot perform that function!'})

    data = request.get_json()

    print(data)
    hash_password = generate_password_hash(str(data['password']).encode("utf-8"), method='sha256')
    user_new = User(public_id=str(uuid.uuid4()), name=data['name'], password=hash_password, admin=False)
    db.session.add(user_new)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})


@user.route('/user/<public_id>', methods=['PUT'])
# @token_required
def promote_user(current_user, public_id):
    # if not current_user.admin:
    #     return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No user found'})

    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'User has been promoted'})

@user.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})



@user.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},os.environ.get("PASSWORD_KEY") , algorithm=os.environ.get("ALGORITHM"))

        return jsonify({'token' : token})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})



from flask import Blueprint
import json
from lib2to3.pgen2 import token
import uuid
import jwt
import datetime
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .models import User, Post
from .extensions import db
import os

main = Blueprint('main', __name__)



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        
        try: 
            data = jwt.decode(token, main.config['SECRET_KEY'], algorithms='HS256')
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@main.route('/user', methods=['GET'])
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
        output.mainend(dic_user)
    return jsonify({'users':output})


@main.route('/user/<public_id>', methods=['GET'])
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

@main.route('/user', methods=['POST'])
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


@main.route('/user/<public_id>', methods=['PUT'])
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

@main.route('/user/<public_id>', methods=['DELETE'])
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



@main.route('/login')
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


@main.route('/post', methods=['GET'])
@token_required
def get_all_posts(current_user):

    posts = Post.query.filter_by(author=current_user.id).all()
    output = []

    for post in posts:
        dic_post = {}
        dic_post['id'] = post.id
        dic_post['description'] = post.description
        dic_post['priority'] = post.priority
        dic_post['status'] = post.status
        dic_post['is_public'] = post.is_public
        dic_post['create_at'] = post.create_at
        dic_post['author'] = post.author
        output.append(dic_post)

    return jsonify({'posts': output})

@main.route('/post/<post_id>', methods=['GET'])
@token_required
def get_one_post(current_user, post_id):
    post = Post.query.filter_by(id=post_id, user_id=current_user.id).first()

    if not post:
        return jsonify({'message': 'Not Found!'})

    dic_post = dict()
    dic_post['id'] = post.id
    dic_post['description'] = post.description
    dic_post['priority'] = post.priority
    dic_post['status'] = post.status
    dic_post['is_public'] = post.is_public
    dic_post['create_at'] = post.create_at
    dic_post['author'] = post.author

    return jsonify(dic_post)

@main.route('/post/<post_id>', methods=['POST'])
def create_post(current_user, post_id):

    data = request.get_json()

    new_post = Post(title=data['title'],
                    description = data['description'],
                    priority = data['priority'],
                    status = data['status'],
                    time_publish = datetime.datetime.utcnow(),
                    author =current_user.id)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message':'Post created'})

@main.route('/post/<post_id>', methods=['PUT'])
def update_post(current_user, post_id):
    post = Post.query.filter_by(id=post_id, user_id=current_user.id).first()

    if not post:
        return jsonify({'message': 'Not Found!'})

    post.is_public = True
    db.session.commit()

    return jsonify({'message':'Post is public now'})

@main.route('/post/<post_id>', methods=['DELETE'])
def delete_post(current_user, post_id):
    post = Post.query.filter_by(id=post_id, user_id=current_user.id).first()

    if not post:
        return jsonify({'message' : 'No Post found!'})
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message' : 'Post item deleted!'})

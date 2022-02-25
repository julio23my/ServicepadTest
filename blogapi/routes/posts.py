import datetime

from flask import Blueprint
from flask import request, jsonify

from blogapi.models.post import Post
from blogapi.models.user import User
from blogapi.utils.decorators import token_required
from blogapi.extensions import db
from blogapi.utils.database import get_all, get_one, add_instance, delete_instance, edit_instance, update_instance

post = Blueprint('post', __name__)

@post.route('/post', methods=['GET'])
def get_all_posts():

    posts = get_all(Post)
    output = []

    for post in posts:
        dic_post = {}
        dic_post['id'] = post.id
        dic_post['description'] = post.description
        dic_post['priority'] = post.priority
        dic_post['status'] = post.status
        dic_post['is_public'] = post.is_public
        dic_post['created_at'] = post.created_at
        dic_post['author'] = post.user.name
        dic_post['author_id'] = post.user.public_id
        output.append(dic_post)

    return {'posts': output}, 200

@post.route('/post/<post_id>', methods=['GET'])
def get_one_post(post_id):
    post = get_one(Post, id=post_id)

    if not post:
        return {'message' : 'Post not found'}, 404

    dic_post = dict()
    dic_post['id'] = post.id
    dic_post['description'] = post.description
    dic_post['priority'] = post.priority
    dic_post['status'] = post.status
    dic_post['is_public'] = post.is_public
    dic_post['created_at'] = post.created_at
    dic_post['author'] = post.user.name
    dic_post['author_id'] = post.user.public_id

    return dic_post, 200

@post.route('/post', methods=['POST'])
@token_required
def create_post(current_user):

    data = request.get_json()
    data['author'] = str(current_user.id)
    new_post = add_instance(Post, **data)
    if new_post:
        return {'message' : 'Post has been created'}, 201
    else:
        return {'message' : 'Error during adding the user'}, 400

@post.route('/post/<post_id>', methods=['PUT'])
@token_required
def public_post(current_user, post_id):
    edit = update_instance(Post, id=post_id, id=post_id , is_public=True)
    if edit:
        return {'message' : 'Post has been set to public'}, 200
    else:
        return {'message' : 'Error during updating post'}, 400

@post.route('/user/<post_id>', methods=['PATCH'])
@token_required
def update_post(current_user, post_id):
    if not current_user.admin:
        return {'message' : 'You dont have the privileges of admin'}, 401

    data = request.get_json()
    
    edit = edit_instance(User, id=post_id, id=post_id, **data)
    if edit:
        return {'message' : 'Post has updated'}, 200
    else:
        return {'message' : 'Error during updating post'}, 400

@post.route('/post/<post_id>', methods=['DELETE'])
@token_required
def delete_post(current_user, post_id):
    if not current_user.admin:
        return {'message' : 'You dont have the privileges of admin'}, 401

    post = delete_instance(Post, id=post_id)
    if post:
        return {'message' : 'Post has delete'}, 200
    else:
        return {'message' : 'Error during deketing post'}, 400
    
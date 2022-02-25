from flask import Blueprint
from lib2to3.pgen2 import token

import datetime
from flask import request, jsonify
from blogapi.models.post import Post
from blogapi.utils.decorators import token_required
from blogapi.extensions import db

post = Blueprint('post', __name__)

@post.route('/post', methods=['GET'])
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

@post.route('/post/<post_id>', methods=['GET'])
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

@post.route('/post/<post_id>', methods=['POST'])
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

@post.route('/post/<post_id>', methods=['PUT'])
def update_post(current_user, post_id):
    post = Post.query.filter_by(id=post_id, user_id=current_user.id).first()

    if not post:
        return jsonify({'message': 'Not Found!'})

    post.is_public = True
    db.session.commit()

    return jsonify({'message':'Post is public now'})

@post.route('/post/<post_id>', methods=['DELETE'])
def delete_post(current_user, post_id):
    post = Post.query.filter_by(id=post_id, user_id=current_user.id).first()

    if not post:
        return jsonify({'message' : 'No Post found!'})
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message' : 'Post item deleted!'})
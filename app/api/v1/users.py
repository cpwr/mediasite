# coding: utf-8

from flask import request
from flask import current_app

from ..decorators import json
from app import db
from app.models import User
from app.api.v1 import api_v1


@api_v1.route('/users/<int:id>/', methods=['GET'])
@json()
def get_user(id):
    user = User.query.get_or_404(id)
    return user.to_json(), 200


@api_v1.route('/users/', methods=['GET'])
@json()
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', current_app.config['ADMIN_USERS_PER_PAGE'],
                                    type=int), current_app.config['ADMIN_USERS_PER_PAGE'])

    users = (
        User.query
        .order_by(User.username.desc())
    )
    p = users.paginate(page, per_page)

    return {
        'paginator': {
            'page': page,
            'pages': p.pages,
        },
        'objects': [x.to_json() for x in p.items],
    }, 200


@api_v1.route('/users/<int:id>/', methods=['DELETE'])
@json()
def delete_user(id):
    user = User.query.get_or_404(id)
    user.status = User.STATUS_DELETED
    db.session.commit()
    return {}, 204


@api_v1.route('/user/activate/<int:id>/', methods=['PUT'])
@json()
def activate_user(id):
    user = User.query.get_or_404(id)
    user.status = User.STATUS_ACTIVE
    db.session.commit()
    return {}, 204

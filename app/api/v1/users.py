# coding: utf-8

from flask import jsonify
from flask import request
from flask import current_app

from app.api.v1 import api_v1
from app.models import User


@api_v1.route('/users/', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', current_app.config['ADMIN_USERS_PER_PAGE'],
                                    type=int), current_app.config['ADMIN_USERS_PER_PAGE'])

    users = (
        User.query
        .order_by(User.username.desc())
    )
    p = users.paginate(page, per_page)

    return jsonify({
        'paginator': {
            'page': page,
            'pages': p.pages,
        },
        'objects': [x.to_json() for x in p.items],
    })

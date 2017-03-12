from datetime import datetime
from enum import IntEnum

import sqlalchemy as sa


metadata = sa.MetaData()


permissions = sa.Table(
    'permissions', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(64), unique=True),
    sa.Column('title', sa.String(64)),
)

roles = sa.Table(
    'roles', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(64), unique=True),
)

follows = sa.Table(
    'roles', metadata,
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('users.id'), primary_key=True),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('users.id'), primary_key=True),
    sa.Column('timestamp', sa.DateTime, default=datetime.utcnow),
)

users = sa.Table(
    'users', metadata,

    id = sa.Column('id', sa.Integer, primary_key=True),
    email = sa.Column('email', sa.String, index=True, unique=True, nullable=False),
    username = sa.Column('username', sa.String(64), unique=True, nullable=False),
    status = sa.Column('status', sa.Integer, default=Status.active, index=True),
    is_admin = sa.Column('is_admin', sa.Boolean, default=False),
    reg_date = sa.Column('reg_date', sa.DateTime, default=datetime.now),
)



role_permission_associate = sa.Table(
    'role_permission', metadata,
    sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id')),
    sa.Column('permission_id', sa.Integer, sa.ForeignKey('permissions.id')),
)
user_permission_associate = sa.Table(
    'user_permission', metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
    sa.Column('permission_id', sa.Integer, sa.ForeignKey('permissions.id')),
)
user_role_associate = sa.Table(
    'user_role', metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
    sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id')),
)

post_tag_associate = sa.Table(
    'posts_tag', metadata,
    sa.Column('post_id', sa.Integer, sa.ForeignKey('posts.id')),
    sa.Column('tag_id', sa.Integer, sa.ForeignKey('tags.id')),
)


class Status(IntEnum):
    active = 0
    deleted = 1


class Permissions(IntEnum):
    post_comment = 0
    write_articles = 1
    manage_comments = 2
    manage_users = 3
    manage_articles = 4


    #
    # def to_json(self):
    #     return {
    #         'id': self.id,
    #         'email': self.email,
    #         'username': self.username,
    #         'status': self.status,
    #         'is_admin': self.is_admin,
    #         'reg_date': self.reg_date,
    #         'permissions': [p.name for p in self.permissions],
    #         'roles': [r.id for r in self.roles],
    #         'followed': [u.id for u in self.followed],
    #         'followers': [u.id for u in self.followers],
    #         'comments': [c.id for c in self.comments],
    #     }
#
#
# class Post(db.Model):
#
#     __tablename__ = 'posts'
#
#     (
#         STATUS_ACTIVE,
#         STATUS_DELETED,
#         ON_MODERATION,
#         STATUS_BLOCKED,
#     ) = range(4)
#
#     STATUSES = [
#         (STATUS_ACTIVE, 'Active'), (STATUS_DELETED, 'Deleted'),
#         (ON_MODERATION, 'On moderation'), (STATUS_BLOCKED, 'Blocked')
#     ]
#
#     id = sa.Column(sa.Integer, primary_key=True)
#     title = sa.Column(sa.String, index=True)
#     text = sa.Column(db.Text)
#     timestamp = sa.Column(db.DateTime, index=True, default=datetime.utcnow)
#     author_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
#     category_id = sa.Column(sa.Integer, sa.ForeignKey('posts_category.id'))
#     comments_count = sa.Column(sa.Integer, default=0)
#     status = sa.Column(sa.Integer, default=STATUS_ACTIVE, index=True)
#
#     comments = sa.Relationship('Comment', backref='post', lazy='dynamic')
#     author = sa.Relationship("User", backref="posts", lazy="joined")
#     category = sa.Relationship(
#         "PostCategory",
#         backref=db.backref('posts', order_by=desc('Post.datetime')),
#         lazy="joined"
#     )
#     tags = sa.Relationship(
#         "Tag",
#         secondary=post_tag_associate,
#         backref=db.backref('posts', order_by=desc('Post.datetime')),
#         lazy="joined"
#     )
#
#     def to_json(self):
#         return {
#             'id': self.id,
#             'title': self.title,
#             'text': self.text,
#             'timestamp': self.timestamp,
#             'author_id': self.author_id,
#             'comments': self.comments,
#             'category_id': self.category_id,
#             'comments_count': self.comments_count,
#             'status': self.status,
#             'author': self.author,
#             'category': self.category,
#             'tags': self.tags,
#         }
#
#
# class Comment(db.Model):
#
#     __tablename__ = 'comments'
#
#     (
#         STATUS_ACTIVE,
#         STATUS_DELETED,
#         STATUS_MODIFIED
#     ) = range(3)
#
#     STATUSES = [(STATUS_ACTIVE, 'Active'), (STATUS_DELETED, 'Deleted'), (STATUS_MODIFIED, 'Modified')]
#
#     id = sa.Column(sa.Integer, primary_key=True)
#     body = sa.Column(db.Text)
#     timestamp = sa.Column(db.DateTime, index=True, default=datetime.utcnow)
#     modify_timestamp = sa.Column(db.DateTime, index=True, default=datetime.now)
#     status = sa.Column(sa.Integer, default=STATUS_ACTIVE, index=True)
#
#     author_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
#     post_id = sa.Column(sa.Integer, sa.ForeignKey('posts.id'))
#
#
# class Tag(db.Model):
#
#     __tablename__ = 'tags'
#
#     id = sa.Column(sa.Integer, primary_key=True)
#     name = sa.Column(sa.String(255), nullable=False)
#
#
# class PostCategory(db.Model):
#
#     __tablename__ = 'posts_category'
#
#     id = sa.Column(sa.Integer, primary_key=True)
#     name = sa.Column(sa.String(255), nullable=False)
#     parent_id = db. Column(sa.Integer, sa.ForeignKey('posts_category.id'), nullable=True)
#
#     parent = sa.Relationship('PostCategory', remote_side=[id],  backref="subcategories", lazy='joined')


# async def sync_permissions():
#     for p in Permissions:
#         permission = Permission.query.filter_by(name=p.name).first()
#         if permission is None:
#             p = Permission()
#             p.name = p.name
#             p.title = p.value
#             db.session.add(p)
#             db.session.commit()
#
#
# async def insert_roles():
#     roles = {
#         'user': ['post_comment'],
#         'moderator': [
#             'post_comment',
#             'write_articles', 'manage_comments',
#             'manage_articles', 'manage_users',
#         ]
#     }
#     permissions_map = {p.name: p for p in Permission.query}
#
#     for role, permissions in roles.items():
#         ur = Role.query.filter_by(name=role).first()
#         if ur is None:
#             r = Role()
#             for p in permissions:
#                 r.permissions.append(permissions_map.get(p))
#             r.name = role
#             db.session.add(r)
#             db.session.commit()

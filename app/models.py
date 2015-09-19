# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import desc

from app import db


role_permission_associate = db.Table(
    'role_permission', db.Model.metadata,
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'))
)
user_permission_associate = db.Table(
    'user_permission', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'))
)
user_role_associate = db.Table(
    'user_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)

post_tag_associate = db.Table(
    'posts_tag', db.Model.metadata,
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)


class Permission(db.Model):

    __tablename__ = 'permissions'

    PERMISSIONS = [
        ('post_comment', 'Писать комментарии'),
        ('write_articles', 'Писать новости'), ('manage_comments', 'Управлять комментариями'),
        ('manage_users', 'Управлять пользователями'), ('manage_articles', 'Управлять новостями'),
    ]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    title = db.Column(db.String(64))


class Role(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    permissions = db.relationship("Permission", secondary=role_permission_associate, backref="roles")


class Follow(db.Model):

    __tablename__ = 'follows'

    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):

    __tablename__ = 'users'

    (
        STATUS_ACTIVE,
        STATUS_DELETED,
    ) = range(2)

    STATUSES = [(STATUS_ACTIVE, 'Active'), (STATUS_DELETED, 'Deleted')]

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, index=True)
    name = db.Column(db.String(64), index=True)
    login = db.Column(db.String(64), unique=True, index=True)
    status = db.Column(db.Integer, default=STATUS_ACTIVE, index=True)
    is_admin = db.Column(db.Boolean, default=False, index=True)
    reg_date = db.Column(db.DateTime, default=datetime.now, index=True)

    permissions = db.relationship("Permission", secondary=user_permission_associate, backref="users", lazy='dynamic')
    roles = db.relationship("Role", secondary=user_role_associate, backref="users", lazy='dynamic')
    followed = db.relationship(
        'Follow',
        foreign_keys=[Follow.follower_id],
        backref=db.backref('follower', lazy='joined'),
        lazy='dynamic', cascade='all, delete-orphan',
    )
    followers = db.relationship(
        'Follow',
        foreign_keys=[Follow.followed_id],
        backref=db.backref('followed', lazy='joined'),
        lazy='dynamic', cascade='all, delete-orphan',
    )
    comments = db.relationship('Comment', backref='author', lazy='dynamic')


class Post(db.Model):

    __tablename__ = 'posts'

    (
        STATUS_ACTIVE,
        STATUS_DELETED,
        ON_MODERATION,
        STATUS_BLOCKED,
    ) = range(4)

    STATUSES = [
        (STATUS_ACTIVE, 'Active'), (STATUS_DELETED, 'Deleted'),
        (ON_MODERATION, 'On moderation'), (STATUS_BLOCKED, 'Blocked')
    ]

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, index=True)
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    category_id = db.Column(db.Integer, db.ForeignKey('posts_category.id'))
    comments_count = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=STATUS_ACTIVE, index=True)

    author = db.relationship("User", backref="posts", lazy="joined")
    category = db.relationship("PostCategory", backref=db.backref('posts', order_by=desc('Post.datetime')), lazy="joined")
    tags = db.relationship("Tag", secondary=post_tag_associate, backref=db.backref('posts', order_by=desc('Post.datetime')), lazy="joined")


class Comment(db.Model):

    __tablename__ = 'comments'

    (
        STATUS_ACTIVE,
        STATUS_DELETED,
        STATUS_MODIFIED
    ) = range(3)

    STATUSES = [(STATUS_ACTIVE, 'Active'), (STATUS_DELETED, 'Deleted'), (STATUS_MODIFIED, 'Modified')]

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modify_timestamp = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Integer, default=STATUS_ACTIVE, index=True)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))


class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class PostCategory(db.Model):

    __tablename__ = 'posts_category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    parent_id = db. Column(db.Integer, db.ForeignKey('posts_category.id'), nullable=True)

    parent = db.relationship('PostCategory', remote_side=[id],  backref="subcategories", lazy='joined')

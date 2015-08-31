# -*- coding: utf-8 -*-

from datetime import datetime
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


class Permission(db.Model):

    __tablename__ = 'permissions'

    PERMISSIONS = [
    ]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    title = db.Column(db.String(64))


class Role(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.relationship("Permission", secondary=role_permission_associate, backref="roles")


class User(db.Model):

    __tablename__ = 'users'

    (
        STATUS_ACTIVE,
        STATUS_DELETED,
    ) = range(2)

    STATUSES = [(STATUS_ACTIVE, 'Active'), (STATUS_DELETED, 'Deleted')]

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    name = db.Column(db.String(64))
    login = db.Column(db.String(64), unique=True)
    status = db.Column(db.Integer, default=STATUS_ACTIVE)
    is_admin = db.Column(db.Boolean, default=False)
    reg_date = db.Column(db.DateTime, default=datetime.now)

    permissions = db.relationship("Permission", secondary=user_permission_associate, backref="users", lazy='dynamic')
    roles = db.relationship("Role", secondary=user_role_associate, backref="users", lazy='dynamic')

def get_permissions(user):
    return set([permission.name for permission in user.permissions]).union(
        set([permission.name for role in user.roles for permission in role.permissions])
    )


def has_role(user, role):
    return role in user.roles

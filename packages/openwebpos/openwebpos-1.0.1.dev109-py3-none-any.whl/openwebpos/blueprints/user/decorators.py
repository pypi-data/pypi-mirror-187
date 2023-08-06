from functools import wraps

from flask import redirect, url_for
from flask_login import current_user


def role_require(*roles):
    """
    Decorator to require a user to have a specific role.

    Args:
        roles (str): Role name.

    Returns:
        function: Decorated function.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role.name not in roles:
                return redirect(url_for('user.login'))
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def permission_require(*permissions):
    """
    Decorator to require a user to have a specific permission.

    Args:
        permissions (str): Permission name.

    Returns:
        function: Decorated function.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Permissions based on role
            role_permissions = [p.permission.name for p in
                                current_user.role.role_permissions]
            # Permissions based on user
            user_permissions = [p.permission.name for p in
                                current_user.permissions]
            # Check if role has permission
            if not set(permissions).issubset(set(role_permissions)):
                # Check if user has permission
                if not set(permissions).issubset(set(user_permissions)):
                    return redirect(url_for('pos.index'))
            return f(*args, **kwargs)

        return decorated_function

    return decorator

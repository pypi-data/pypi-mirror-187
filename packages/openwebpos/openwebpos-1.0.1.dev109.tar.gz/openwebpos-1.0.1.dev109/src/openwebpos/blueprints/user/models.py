from datetime import datetime

from flask_login import UserMixin
from usernames import is_safe_username
from werkzeug.security import generate_password_hash, check_password_hash

from openwebpos.blueprints.admin.models import Branch
from openwebpos.extensions import db
from openwebpos.utils.sql import DateTimeMixin, CRUDMixin


class Role(DateTimeMixin, db.Model, CRUDMixin):
    """
    Role model.
    """
    __tablename__ = 'role'

    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)

    # One-to-many relationship
    users = db.relationship('User', backref='role', lazy='dynamic')
    role_permissions = db.relationship('RolePermission', backref='role',
                                       lazy=True)

    @staticmethod
    def insert_default_roles() -> None:
        """
        Insert default roles into the database.
        """
        roles = [
            {'name': 'Administrator', 'description': 'Administrator'},
            {'name': 'Manager', 'description': 'Manager'},
            {'name': 'Cashier', 'description': 'Cashier'},
            {'name': 'Waiter', 'description': 'Waiter'},
            {'name': 'Cook', 'description': 'Cook'},
            {'name': 'Bartender', 'description': 'Bartender'},
            {'name': 'Customer', 'description': 'Customer'}
        ]
        for role in roles:
            role = Role(**role)
            role.save()

    def __int__(self, **kwargs):
        super(Role, self).__init__(**kwargs)


class Permission(db.Model, CRUDMixin):
    """
    Permission model.
    """
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(255))

    # One-to-many relationship with RolePermission
    role_permissions = db.relationship('RolePermission', backref='permission',
                                       lazy=True)

    @staticmethod
    def insert_default_permissions():
        """
        Insert Default permissions.
        """

        permissions_list = [
            {'name': 'view_admin', 'description': 'View Admin'},
            {'name': 'view_user', 'description': 'View User'},
            {'name': 'view_role', 'description': 'View Role'},
            {'name': 'view_permission', 'description': 'View Permission'},
            {'name': 'view_company', 'description': 'View Company'},
            {'name': 'view_branch', 'description': 'View Branch'}
        ]

        for permission in permissions_list:
            permission = Permission(**permission)
            permission.save()

    def __int__(self, **kwargs):
        super(Permission, self).__init__(**kwargs)


class RolePermission(db.Model, CRUDMixin):
    """
    Role Permission model.
    """
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'),
                              nullable=False)

    @staticmethod
    def insert_default_role_permissions():
        """
        Insert default role permissions.
        """
        role_permissions = [
            {'role_id': 1, 'permission_id': 1},
            {'role_id': 1, 'permission_id': 2},
            {'role_id': 1, 'permission_id': 3},
            {'role_id': 1, 'permission_id': 4},
            {'role_id': 1, 'permission_id': 5},
            {'role_id': 1, 'permission_id': 6}
        ]
        for role_permission in role_permissions:
            role_permission = RolePermission(**role_permission)
            role_permission.save()

    def __int__(self, **kwargs):
        super(RolePermission, self).__init__(**kwargs)


class UserPermission(db.Model, CRUDMixin):
    """
    User Permission model.
    """
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'),
                              nullable=False)

    def __int__(self, **kwargs):
        super(UserPermission, self).__init__(**kwargs)


class User(UserMixin, DateTimeMixin, CRUDMixin, db.Model):
    """
    User model for defining users.
    """
    __tablename__ = "user"

    # Parent relationship
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    branch_id = db.Column(db.Integer,
                          db.ForeignKey('branch.id', ondelete='SET NULL'),
                          nullable=True)

    # Authentication
    username = db.Column(db.String(120), unique=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password = db.Column(db.String(120), nullable=False, server_default='')
    active = db.Column('is_active', db.Boolean(), nullable=False,
                       server_default='1')
    staff = db.Column(db.Boolean, nullable=False, default=False)

    # One-to-One relationships
    profile = db.relationship('UserProfile', backref='user', lazy=True,
                              uselist=False, cascade='all, delete-orphan')
    activity = db.relationship('UserActivity', backref='user', lazy=True,
                               uselist=False, cascade='all, delete-orphan')

    # One-to-Many relationships
    orders = db.relationship('Order', backref='user', lazy=True)
    permissions = db.relationship('UserPermission', backref='user', lazy=True)

    @staticmethod
    def insert_default_user():
        """
        Insert default user in the database.
        """
        admin_id = Role.query.filter_by(name='Administrator').first().id
        user = User(username='admin',
                    email='admin@mail.com',
                    password=generate_password_hash('admin'),
                    staff=True,
                    role_id=admin_id,
                    branch_id=1)
        user.save()

    def is_last_admin(self):
        """
        Check if the user is the last admin.
        """
        if self.role.name == 'Administrator':
            if User.query.filter_by(role_id=self.role_id).count() == 1:
                return True
        return False

    def is_admin(self):
        """
        Return whether user is admin.

        Returns:
            bool: True if user is admin, False otherwise.
        """
        return self.role.name == 'Administrator'

    def is_staff(self):
        """
        Return whether user is staff.

        Returns:
            bool: True if user is staff, False otherwise.
        """
        return self.staff

    def is_last_staff(self):
        """
        Return whether user is the last staff.

        Returns:
            bool: True if user is the last staff, False otherwise.
        """
        return self.staff and User.query.filter_by(staff=True).count() == 1

    def set_as_staff(self):
        """
        Set user as staff.

        Returns:
            None
        """
        self.staff = True
        self.update()

    def remove_as_staff(self):
        """
        Remove user as staff.

        Returns:
            None

        TODO:
            - Check if user is the last staff before removing.
            - Raise exception if user is the last staff.
            - Handle exception in view.
            - Add flash message in view.
        """
        self.staff = False
        self.update()

    def set_password(self, password):
        """
        Set user password.

        Args:
            password (str): Password to set.

        Returns:
            None
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if the password is correct.

        Args:
            password (str): Password to check.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        return check_password_hash(self.password, password)

    def check_if_safe_username(self):
        """
        Check if the username is safe.

        Returns:
            bool: True if the username is safe, False otherwise.
        """
        return is_safe_username(self.username)

    def is_active(self):
        """
        Return whether user account is active.

        Returns:
            bool: True if user account is active, False otherwise.
        """
        return self.active

    def make_inactive(self):
        """
        Make user account inactive.

        Returns:
            None
        """
        self.active = False
        self.update()

    def toggle_active(self):
        """
        Toggle user account active status.

        Returns:
            None
        """
        self.active = not self.active
        self.update()

    def toggle_staff(self):
        """
        Toggle user staff status.

        Returns:
            None
        """
        self.staff = not self.staff
        self.update()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        if self.role_id is None:
            self.role_id = Role.query.filter_by(name='Customer').first().id

        if self.branch_id is None:
            self.branch_id = Branch.query.first().id


class UserProfile(DateTimeMixin, CRUDMixin, db.Model):
    """
    User profile model.
    """
    __tablename__ = "user_profile"

    # Parent relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    picture = db.Column(db.String(255), nullable=True, default='default.png')
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    zip_code = db.Column(db.String(120))
    dob = db.Column(db.String(120))

    def __init__(self, **kwargs):
        super(UserProfile, self).__init__(**kwargs)


class UserActivity(CRUDMixin, db.Model):
    """
    User activity model.
    """
    __tablename__ = "user_activity"

    # Parent relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_at = db.Column(db.DateTime, nullable=True)
    current_sign_in_ip = db.Column(db.String(100), nullable=True)
    last_sign_in_at = db.Column(db.DateTime, nullable=True, default=None)
    last_sign_in_ip = db.Column(db.String(100), nullable=True, default=None)
    user_agent = db.Column(db.String(120))
    referrer = db.Column(db.String(120))

    def __init__(self, **kwargs):
        super(UserActivity, self).__init__(**kwargs)

    def update_activity(self, ip_address: str, user_id: int):
        """
        Update the fields associated with user activity tracking.

        Args:
            ip_address: IP address of the user.
            user_id: ID of the user.

        Returns:
            None
        """
        self.user_id = user_id
        self.last_sign_in_at = self.current_sign_in_at
        self.last_sign_in_ip = self.current_sign_in_ip
        self.current_sign_in_at = datetime.utcnow()
        self.current_sign_in_ip = ip_address
        if self.sign_in_count is None:
            self.sign_in_count = 1
        else:
            self.sign_in_count += 1

        return self.save()

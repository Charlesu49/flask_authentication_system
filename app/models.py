from datetime import datetime as d
import datetime
from app import db
import bcrypt
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer


# the below function rounds off datetime, to be used in the created_at attribute of the User class
def round_seconds(dts):
    dts = dts.strftime('%Y-%m-%d %H:%M:%S')
    date = dts.split()[0]
    h, m, s = [dts.split()[1].split(':')[0],
               dts.split()[1].split(':')[1],
               str(round(float(dts.split()[1].split(':')[-1])))]
    result = date + ' ' + h + ':' + m + ':' + s
    result_dt = d.strptime(result, '%Y-%m-%d %H:%M:%S')

    return result_dt


# the model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    # password_salt = db.Column(db.String(255))
    # password_hash_algorithm = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(), default=round_seconds(d.now()))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    confirmed = db.Column(db.Boolean, default=False)

    # to assign a role to a user on account registeration
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.username in current_app.config['APP_ADMIN']:
                self.role = Role.query.filter_by(name='administrator').first()
            if self.role is None:
                print(self.username)
                self.role = Role.query.filter_by(default=True).first()

    # returns true if the user has a role assigned and the role has the given permission 'perm'
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    # returns true is the user is an administrator
    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def __repr__(self):
        return "<User - '{}'>".format(self.username)

    @property
    def password(self):
        # to ensure password cannot be accessed
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, plain_text_password):
        plain_text_password = bytes(plain_text_password, encoding='utf-8')
        self.password_hash = bcrypt.hashpw(plain_text_password, bcrypt.gensalt(12))

    def verify_password(self, attempted_password):
        attempted_password = bytes(attempted_password, encoding='utf-8')
        return bcrypt.checkpw(attempted_password, self.password_hash)

    #  below is related to user confirmation
    # generates new confirmation token using itsdangerous' URLSafeTimedSerializer
    def generate_confirmation_token(self):
        info = Serializer(current_app.config['SECRET_KEY'])
        return info.dumps({'confirm': self.id})

    def confirm(self, token):
        info = Serializer(current_app.config['SECRET_KEY'])
        expiry = 3600
        try:
            data = info.loads(token, max_age=expiry)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


# this custom AnonymousUser class that implements the can() and is_administrator() method will enable the application
# to freely call current_user.can() and current_user.is_administrator without having to check whether the user is logged
# in first
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


# for Flask-Login to user the application's custom anonymous user, we set it class in the
# login_manager_anonymous_user attribute
login_manager.anonymous_user = AnonymousUser


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    user = db.relationship('User', backref='role', lazy='dynamic')

    # set the value of permissions to 0 if an initial value is not provided
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    # methods to manage permissions as defined in the Permission class
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permission -= perm

    def reset_permissions(self):
        self.permissions = 0

    # the method below relies on bitwise and operator '&' to check if a combined permission value
    # includes the given basic permission 'perm' given as a parameter
    def has_permission(self, perm):
        return self.permissions & perm == perm

    # the below static method automatically add roles to the database
    @staticmethod
    def add_roles():
        roles = {
            'user': [Permission.READ],
            'moderator': [Permission.READ, Permission.MODERATE],
            'administrator': [Permission.READ, Permission.MODERATE, Permission.ADMIN]
        }
        default_role = 'user'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for permission in roles[r]:
                role.add_permission(permission)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return "<Role - '{}'>".format(self.name)


# permission constants- here we use powers of 2 for the permission values, allowing the values
# to be combined and giving each possible combination of permissions a unique value to be stored
# in the role's permissions field.
class Permission:
    READ = 1
    MODERATE = 2
    ADMIN = 4


# The login_manager.user_loader decorator is used to register the function with
# Flask-Login, which will call it when it needs to retrieve information about the loggedin
# user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

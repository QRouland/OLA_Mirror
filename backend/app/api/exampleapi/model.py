from passlib.apps import custom_app_context as pwd_context

from app.core import db

users_roles = db.Table('users_roles',
                       db.Column('user_id',
                                 db.Integer,
                                 db.ForeignKey('user.id')
                                 ),
                       db.Column('role_id',
                                 db.Integer,
                                 db.ForeignKey('role.id')
                                 )
                       )


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    roles = db.relationship('Role', secondary=users_roles)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

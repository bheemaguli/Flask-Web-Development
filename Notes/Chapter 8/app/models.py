from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import UserMixin
from flask import current_app
from . import db

# Deprecated 
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import jwt # pyjwt
import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username
    
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    confirm = db.Column(db.Boolean, default=False)
    
    # def generate_confirmation_token(self, expiration=3600):
    #     s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps({'confirm':self.id}).decode('utf-8')
    
    # def confirm(self, token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token.encode('utf-8'))
    #     except:
    #         return False
    #     if data.get('confirm') != self.id:
    #         return False
    #     self.confirmed = True
    #     db.session.add(self)
    #     return True
    
    def generate_confirmation_token(self, expiration=600):
        reset_token = jwt.encode(
            {
                "confirm": self.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                       + datetime.timedelta(seconds=expiration)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return reset_token

    def confirm(self, token):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms="HS256"
            )
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    
    # def generate_confirmation_token(self, expiration=3600):
    #     """ Generate for mailbox validation JWT (json web token)"""
    #     #  Signature algorithm 
    #     header = {
    #     'alg': 'HS256',}
    #     #  The key used for the signature 
    #     key = current_app.config['SECRET_KEY']
    #     #  Data load to be signed 
    #     data = {'confirm': self.id, 'exp':expiration}
        
    #     return jwt.encode(header=header, payload=data, key=key)
    #     reset_token = jwt.encode(
    #         {
    #             "confirm": self.id,
    #             "exp": datetime.datetime.now(tz=datetime.timezone.utc)
    #                    + datetime.timedelta(seconds=expiration)
    #         },
    #         current_app.config['SECRET_KEY'],
    #         algorithm="HS256"
    #     )

    # def confirm(self, token):
    #     """ Used to verify user registration and change password or mailbox token,  And complete the corresponding confirmation operation """
    #     key = current_app.config['SECRET_KEY']

    #     try:
    #         data = jwt.decode(token, key)
    #         print(data)
    #     except JoseError:
    #         return False
        
    #     if data.get('confirm') != self.id:
    #         return False
    #     self.confirmed = True
    #     db.session.add(self)
    #     return True

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    # This is used to debug the database
    def __repr__(self):
        return '<Role %r>' % self.name
    
@login_manager.user_loader
def  load_user(user_id):
    return User.query.get(int(user_id))
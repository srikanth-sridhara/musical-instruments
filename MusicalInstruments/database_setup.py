""" This is the setup needed for the inventory database """
import random, string
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as password_context
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

class User(Base):
    """ User Table """
    __tablename__ = 'logged_user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    picture = Column(String)
    provider = Column(String(250))
    email = Column(String, index=True)
    password_hash = Column(String(250))

    def hash_password(self, password):
        self.password_hash = password_context.encrypt(password)

    def verify_password(self, password):
        return password_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        ser = Serializer(secret_key, expires_in=expiration)
        return ser.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        ser = Serializer(secret_key)
        try:
            data = ser.loads(token)
        except SignatureExpired:
    		#Valid Token, but expired
            return None
        except BadSignature:
            #Invalid Token
            return None
        user_id = data['id']
        return user_id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


class Categories(Base):
    """ Categories Table """
    __tablename__ = 'categories'
    name = Column(Text, nullable=False)
    description = Column(Text)
    image = Column(String(250))

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('logged_user.id'))
    user = relationship(User)

    category_item = relationship('CategoryItems', cascade='all, delete-orphan')

    @property
    def serialize(self):
        """ This function is used to serialize the table objects """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image,
        }


class CategoryItems(Base):
    """ Category Items Table """
    __tablename__ = 'category_items'
    title = Column(String(250), nullable=False)
    description = Column(Text)
    image = Column(String(250))

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship(Categories)
    user_id = Column(Integer, ForeignKey('logged_user.id'))
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship(User)

    @property
    def serialize(self):
        """ This function is used to serialize the table objects """
        return {
            'id': self.id,
            'category_id': self.category_id,
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'created_on': self.created_on,
        }

db = create_engine('postgresql://catalog:catalog@localhost:5432/catalog')
Base.metadata.create_all(db)

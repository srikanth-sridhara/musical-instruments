""" This module has all the database helper functions for CRUD """
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Categories, CategoryItems

db = create_engine('postgresql://catalog:catalog@localhost:5432/catalog')
Base.metadata.bind = db

DBSession = sessionmaker(bind=db)
session = DBSession()

### User db functions ###
def create_user(login_session):
    new_user = User(
        name=login_session['name'],
        email=login_session['email'],
        picture=login_session['picture'],
        provider=login_session['provider'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user

def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

def get_user_by_email(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user
    except:
        return None

def set_user_info(email, login_session):
    try:
        user = session.query(User).filter_by(email=email).one()
        user.name=login_session['name']
        user.picture=login_session['picture']
        user.provider=login_session['provider']
        session.add(user)
        session.commit()
        return user
    except:
        return None


### Categories db functions ###
def get_categories():
    return session.query(Categories).all()

def get_category(category_id):
    return session.query(Categories).filter_by(id=category_id).one()

def new_category(category_obj):
    category_to_add = Categories(
        name=category_obj['name'],
        description=category_obj['description'],
        image=category_obj['image'],
        user_id=category_obj['user_id'])
    session.add(category_to_add)
    session.commit()

def delete_category(category_id):
    category_to_delete = get_category(category_id)
    session.delete(category_to_delete)
    session.commit()

def edit_category(category_id, category_name=None, category_description=None, category_image=None):
    category_to_edit = get_category(category_id)
    if category_name != None:
        category_to_edit.name = category_name
    if category_description != None:
        category_to_edit.description = category_description
    if category_image != None:
        category_to_edit.image = category_image
    session.add(category_to_edit)
    session.commit()


### Category Items db functions ###
def get_category_items(category_id):
    return session.query(CategoryItems).filter_by(category_id=category_id).all()

def get_category_item(category_item_id):
    return session.query(CategoryItems).filter_by(id=category_item_id).one()

def new_category_item(category_id, category_item_obj=None):
    new_item = CategoryItems(
        title=str(category_item_obj['title']),
        description=str(category_item_obj['description']),
        image=str(category_item_obj['image']),
        category_id=category_id,
        user_id=category_item_obj['user_id'])
    session.add(new_item)
    session.commit()

def delete_category_item(category_item_id):
    item_to_delete = get_category_item(category_item_id)
    session.delete(item_to_delete)
    session.commit()

def edit_category_item(category_item_id, category_item_obj=None):
    item_to_edit = get_category_item(category_item_id)
    if category_item_obj['title'] != None:
        item_to_edit.title = category_item_obj['title']
    if category_item_obj['description'] != None:
        item_to_edit.description = category_item_obj['description']
    if category_item_obj['image'] != None:
        item_to_edit.image = category_item_obj['image']
    session.add(item_to_edit)
    session.commit()

def get_latest_category_items(num_items=10):
    return session.query(CategoryItems).order_by(desc(CategoryItems.created_on)).limit(num_items).all()

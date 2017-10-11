""" Main Flask app with routes """
import json
import requests
import httplib2
import database_functions as db
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Categories, CategoryItems
from momentjs import momentjs
from flask import (
    Flask,
    render_template,
    url_for,
    request,
    redirect,
    flash,
    jsonify,
    make_response,
    g
)
from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required,
    LoginManager
)
dbase = create_engine('postgresql://catalog:catalog@localhost:5432/catalog')
Base.metadata.bind = dbase
DBSession = sessionmaker(bind=dbase)
session = DBSession()

app = Flask(__name__, static_url_path='/var/www/MusicalInstruments/MusicalInstruments/static')
login_manager = LoginManager()
login_manager.init_app(app)
app.jinja_env.globals['momentjs'] = momentjs

import os
CLIENT_ID = json.loads(open('/var/www/MusicalInstruments/MusicalInstruments/static/client_secrets.json',
    'r').read())['web']['client_id']
APPLICATION_NAME = "Musical Instruments Catalog"

# ############ Login endpoints start ############

@login_manager.user_loader
def load_user(user_id):
    return db.get_user_info(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    flash("Unauthorized. Login first")
    return redirect(url_for('index_categories'))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/oauth/<provider>/', methods=['POST'])
def login_oauth(provider):
    if provider == 'google':
        #STEP 1 - Parse the auth code
        auth_code = request.json.get('code')
        print "Step 1 Complete! Received auth code %s" % auth_code

        #STEP 2 - Exchange for a token
        try:
            # Upgrade the authorization code into a credentials object
            oauth_flow = flow_from_clientsecrets(
                '/var/www/MusicalInstruments/MusicalInstruments/static/client_secrets.json', scope='')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(auth_code)
        except FlowExchangeError:
            response_text = json.dumps(
                'Failed to upgrade the authorization code.')
            response = make_response(response_text, 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Check that the access token is valid.
        access_token = credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1])
        # If there was an error in the access token info, abort.
        if result.get('error') is not None:
            response_text = json.dumps(result.get('error'))
            response = make_response(response_text, 500)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Verify that the access token is used for the intended user.
        google_id = credentials.id_token['sub']
        if result['user_id'] != google_id:
            response_text = json.dumps(
                "Token's user ID doesn't match given user ID.")
            response = make_response(response_text, 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Verify that the access token is valid for this app.
        if result['issued_to'] != CLIENT_ID:
            response_text = json.dumps(
                "Token's client ID does not match app's.")
            response = make_response(response_text, 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        stored_credentials = login_session.get('credentials')
        stored_google_id = login_session.get('google_id')
        stored_provider = login_session.get('provider')
        if stored_credentials is not None and google_id == stored_google_id and stored_provider == 'google':
            response_text = json.dumps('Current user is already connected.')
            response = make_response(response_text, 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        print "Step 2 Complete! Access Token : %s " % credentials.access_token

        #STEP 3 - Find User or make a new one
        #Get user info
        h = httplib2.Http()
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt':'json'}
        answer = requests.get(userinfo_url, params=params)

        data = answer.json()

        name = data['name']
        picture = data['picture']
        email = data['email']
        login_session['name'] = name
        login_session['picture'] = picture
        login_session['email'] = email
        login_session['provider'] = 'google'
        print "Step 3 Complete! Login session: %s" % str(login_session)

        # see if user exists. If not, make a new one
        user = db.get_user_by_email(email=email)
        if not user:
            user = db.create_user(login_session=login_session)
            print "New User! Welcome %s" % str(user)
        if user.provider != 'google':
            user = db.set_user_info(email, login_session)
        g.user = user

        # Login user into flask-login
        login_user(user)

        #STEP 4 - Make token
        token = user.generate_auth_token(600)
        print "Step 4 Complete! User auth token generated: %s" % token

        #STEP 5 - Send back token to the client
        print "Step 5 Complete! User auth token sent back to client"
        return jsonify({'token': token.decode('ascii')})

    elif provider == 'facebook':
        h = httplib2.Http()
        #STEP 1 - Parse the auth code
        auth_code = request.json
        print "Step 1 Complete! Received auth code %s" % auth_code

        #STEP 2 - Exchange for a token
        with open('/var/www/MusicalInstruments/MusicalInstruments/static/fb_client_secrets.json') as data_file:
            data = json.load(data_file)
        client_id = data['web']['app_id']
        client_secret = data['web']['app_secret']
        url = "https://graph.facebook.com/oauth/access_token?"
        url += "grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s" % (
            client_id, client_secret, auth_code
        )
        result = json.loads(h.request(url, 'GET')[1])

        if result.get('error') is not None:
            response_text = json.dumps(result.get('error'))
            response = make_response(response_text, 500)
            response.headers['Content-Type'] = 'application/json'
            return response

        access_token = result['access_token']
        url = "https://graph.facebook.com/debug_token?"
        url += "input_token=%s&access_token=%s" % (auth_code, access_token)
        result2 = json.loads(h.request(url, 'GET')[1])

        if result2.get('error') is not None:
            response_text = json.dumps(result2.get('error'))
            response = make_response(response_text, 500)
            response.headers['Content-Type'] = 'application/json'
            return response

        app_id = result2['data']['app_id']
        user_id = result2['data']['user_id']

        # Verify that the access token is valid for this app.
        if app_id != client_id:
            response_text = json.dumps("Token's client ID does not match app's.")
            response = make_response(response_text, 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        stored_credentials = login_session.get('credentials')
        stored_fb_id = login_session.get('google_id')
        stored_provider = login_session.get('provider')
        if stored_credentials is not None and fb_id == stored_fb_id and stored_provider == 'facebook':
            response_text = json.dumps('Current user is already connected.')
            response = make_response(response_text, 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        print "Step 2 Complete! Access Token : %s " % access_token

        #STEP 3 - Find User or make a new one
        #Get user info
        userinfo_url = "https://graph.facebook.com/me"
        params = {
            'access_token': access_token,
            'fields':'name,id,email,picture',
            'alt':'json'}
        answer = requests.get(userinfo_url, params=params)
        data = answer.json()

        fb_id = data['id']
        name = data['name']
        picture = data['picture']['data']['url']
        email = data['email']
        login_session['name'] = name
        login_session['picture'] = picture
        login_session['email'] = email
        login_session['provider'] = 'facebook'
        print "Step 3 Complete! Login session: %s" % str(login_session)

        # see if user exists. If not, make a new one
        user = db.get_user_by_email(email=email)
        if not user:
            user = db.create_user(login_session=login_session)
            print "New User! Welcome %s" % str(user)
        if user.provider != 'facebook':
            user = db.set_user_info(email, login_session)
        g.user = user

        # Login user into flask-login
        login_user(user)

        #STEP 4 - Make token
        token = user.generate_auth_token(600)
        print "Step 4 Complete! User auth token generated: %s" % token

        #STEP 5 - Send back token to the client
        print "Step 5 Complete! User auth token sent back to client"
        return jsonify({'token': token.decode('ascii')})

    else:
        return 'Unrecoginized Provider'

@app.route('/logout')
def logout():
    login_session.clear()
    return redirect(url_for('index_categories'))

# ############ Login endpoints end   ############

# ############ Categories endpoints start ############
@app.route('/')
@app.route('/categories')
def index_categories():
    categories = db.get_categories()
    return render_template(
        'categories/categories.html',
        categories=categories,
        latest_items=get_latest_category_items())


@app.route('/categories/new/', methods=['GET', 'POST'])
@login_required
def add_new_category():
    if request.method == 'POST':
        name = request.form['categoryname']
        description = request.form['categorydescription']
        image = request.form['categoryimage']
        if image == None or image == "":
            image = url_for('static', filename='img/music.jpg')
        category_obj = {
            'name': name,
            'description': description,
            'image': image,
            'user_id': g.user.id}
        db.new_category(category_obj)
        flash("New category added!")
        return redirect(url_for('index_categories'))
    else:
        return render_template('categories/add_new_category.html')


@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    if request.method == 'POST':
        name = request.form['categoryname']
        description = request.form['categorydescription']
        image = request.form['categoryimage']
        if image == None or image == "":
            image = url_for('static', filename='img/music.jpg')

        db.edit_category(category_id, name, description, image)
        flash("category edited!")
        return redirect(url_for('index_categories'))
    else:
        category = db.get_category(category_id)
        if g.user.id != category.user_id:
            flash("You are not authorized to edit this category!")
            return redirect(url_for('index_categories'))
        return render_template(
            'categories/edit_category.html',
            category_id=category_id,
            category=category)


@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_category(category_id):
    if request.method == 'POST':
        db.delete_category(category_id)
        flash("category deleted!")
        return redirect(url_for('index_categories'))
    else:
        category = db.get_category(category_id)
        if g.user.id != category.user_id:
            flash("You are not authorized to delete this category!")
            return redirect(url_for('index_categories'))
        return render_template(
            'categories/delete_category.html',
            category_id=category_id,
            category=category)
# ############ Categories endpoints end  ############


# #######    Category Items endpoints start   #######
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/categoryitems/')
def index_category_items(category_id):
    category = db.get_category(category_id)
    items = db.get_category_items(category_id)
    return render_template(
        'category_items/category_items.html',
        category=category,
        items=items)


@app.route('/category/<int:category_id>/new/', methods=['GET', 'POST'])
@login_required
def add_new_category_item(category_id):
    if request.method == 'POST':
        title       = request.form['itemtitle']
        image       = request.form['itemimage']
        description = request.form['itemdescription']
        if image == None or image == "":
            image = url_for('static', filename='img/music.jpg')

        category_item_obj = {
            'title': title,
            'description': description,
            'image': image,
            'user_id': g.user.id}
        db.new_category_item(category_id, category_item_obj)
        flash("New category item created!")
        return redirect(
            url_for('index_category_items',
            category_id=category_id))
    else:
        category = db.get_category(category_id)
        return render_template(
            'category_items/add_new_category_item.html',
            category=category)


@app.route('/category/<int:category_id>/<int:category_item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category_item(category_id, category_item_id):
    if request.method == 'POST':
        title       = request.form['itemtitle']
        image       = request.form['itemimage']
        description = request.form['itemdescription']
        if image == None or image == "":
            image = url_for('static', filename='img/music.jpg')
        category_item_obj = {
            'title': title,
            'description': description,
            'image': image}
        db.edit_category_item(category_item_id, category_item_obj)
        flash("Category item edited!")
        return redirect(
            url_for('index_category_items',
            category_id=category_id))
    else:
        item = db.get_category_item(category_item_id)
        if g.user.id != item.user_id:
            flash("You are not authorized to edit this item!")
            return redirect(
                url_for('index_category_items',
                category_id=category_id))
        return render_template(
            'category_items/edit_category_item.html',
            category_id=category_id,
            item=item)


@app.route('/category/<int:category_id>/<int:category_item_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_category_item(category_id, category_item_id):
    if request.method == 'POST':
        db.delete_category_item(category_item_id)
        flash("Category item deleted!")
        return redirect(
            url_for('index_category_items',
            category_id=category_id))
    else:
        item = db.get_category_item(category_item_id)
        if g.user.id != item.user_id:
            flash("You are not authorized to delete this item!")
            return redirect(
                url_for('index_category_items',
                category_id=category_id))
        return render_template(
            'category_items/delete_category_item.html',
            item=item)

def get_latest_category_items():
    return db.get_latest_category_items(10)
# #######    Category Items endpoints end     #######


# ############ API endpoints start       ############
@app.route('/apis/categories/')
def get_all_categories():
    categories = db.get_categories()
    return jsonify(Categories=[r.serialize for r in categories])

@app.route('/apis/categories/<int:category_id>/')
def get_category(category_id):
    category = db.get_category(category_id)
    return jsonify(Categories=category.serialize)

@app.route('/apis/categories/<int:category_id>/categoryitems/')
def get_all_category_items(category_id):
    items = db.get_category_items(category_id)
    return jsonify(CategoryItems=[i.serialize for i in items])

@app.route('/apis/categories/<int:category_id>/categoryitems/<int:category_item_id>/')
def get_category_item(category_id, category_item_id):
    item = db.get_category_item(category_item_id)
    return jsonify(CategoryItems=item.serialize)
# ############ API endpoints end         ############


if __name__ == '__main__':
    app.debug = True
    app.secret_key = "my_preciousss"
    app.run()


import os
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash, send_from_directory
from flask.ext.seasurf import SeaSurf
from sqlalchemy import create_engine, asc, desc, func
from sqlalchemy.orm import sessionmaker
from database_schema import Category, Base, Item, User, Pictures
from flask import session as login_session
from werkzeug import secure_filename
import random
import string
from myforms import myNewItem

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'JPG', 'jpeg', 'gif'])

app = Flask(__name__)
csrf = SeaSurf(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog"


# Connect to Database and create database session
engine = create_engine('sqlite:///catalogwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# Google connect
@csrf.exempt
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    # print code
    # print "authorization code is %s" % code

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
        print credentials
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one.
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;\
        -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s with email %s" % (
        login_session['username'], login_session['email']))
    print "done!"
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
        'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Disconnect-- Revoke a current user's token and reset their login session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    print credentials
    if credentials is None:
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Execute HTTP GET request to revoke current token.
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(json.dumps('Failed to revoke token for given\
            user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Facebook connect:
@csrf.exempt
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]
    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly
    # logout, stripping out information before the equals sign in token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;\
        -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("You are now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Show all categories and items:
@app.route('/')
def AllCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    # items = session.query(Item).order_by(desc(Item.name))
    items = session.query(Item).join(
        Category).order_by(desc(Item.id)).limit(9).all()

    if 'username' not in login_session:
        return render_template(
            'public_categories.html',
            categories=categories,
            items=items)
    else:
        return render_template(
            'private_categories.html',
            categories=categories,
            items=items)


# Show specific items of the given category
@app.route('/catalog/<category_name>/items')
def SpecificCategory(category_name):
    categories = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id)
    numItems = session.query(
        func.count(
            Item.id)).filter_by(
        category_id=category.id).one()
    creator = getUserInfo(category.user_id)
    if 'username' not in login_session:
        return render_template(
            'public_items.html',
            category=category,
            categories=categories,
            items=items,
            numItems=numItems,
            creator=creator)
    else:
        return render_template(
            'private_items.html',
            category=category,
            categories=categories,
            items=items,
            numItems=numItems,
            creator=creator)


# Show specific item description and pictures
@app.route('/catalog/<category_name>/<item_name>')
def SpecificItem(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(
        name=item_name, category_id=category.id).one()
    pics = session.query(Pictures).join(Item).filter_by(id=item.id).all()
    creator = getUserInfo(item.user_id)
    if 'username' not in login_session:
        return render_template(
            'public_specific_item.html',
            category=category,
            item=item,
            pics=pics,
            creator=creator)
    else:
        return render_template(
            'private_specific_item.html',
            category=category,
            item=item,
            pics=pics,
            creator=creator)


# Add items on login
@app.route('/catalog/new', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect('/login')
    form = myNewItem(request.form)
    if request.method == 'POST' and form.validate():
        Mylist = []
        for picture in request.files:
            file = request.files[picture]

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = Rename(filename)
                filename_on_form = file.name
                my_filename = (filename, filename_on_form)
                Mylist.append(my_filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                flash('No file is attached or not allowed file')
                categories = session.query(Category).all()
                return render_template(
                    'newItem.html', categories=categories, form=form)
            print "This is the variable filename %s" % filename
            print "This variable has a type %s" % type(filename)

        newItem = Item(
            name=form.name.data,
            description=request.form['description'],
            category_id=request.form['category'],
            user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()

        # print "The name printed on the form is %s" % form.name.data
        # print "This is my list: %s" % Mylist
        for filename, form_name in Mylist:
            newPic = Pictures(
                item=newItem,
                picture=os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    filename),
                name=form_name)
            session.add(newPic)
            session.commit()
        flash('"%s" item was successfully created' % (newItem.name))
        return redirect(url_for('AllCategories'))

    else:
        categories = session.query(Category).all()
        return render_template(
            'newItem.html',
            categories=categories,
            form=form)


# Edit items on login
@app.route('/catalog/<item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):

    if 'username' not in login_session:
        return redirect('/login')

    editedItem = session.query(Item).filter_by(name=item_name).one()

    pics = session.query(Pictures).join(Item).filter_by(id=editedItem.id).all()

    if editedItem.user_id != login_session['user_id']:
        return render_template('not_auth_edit.html')

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            editedItem.category_id = request.form['category']
        session.add(editedItem)
        session.commit()

        for picture in request.files:
            if request.files[picture]:
                file = request.files[picture]
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(
                        os.path.join(
                            app.config['UPLOAD_FOLDER'],
                            filename))

                    for pic in pics:
                        if pic.name == file.name:
                            os.remove(pic.picture)
                            pic.picture = os.path.join(
                                app.config['UPLOAD_FOLDER'], filename)
                            session.add(pic)
                            session.commit()
                else:
                    categories = session.query(Category).all()
                    return render_template(
                        'editItem.html',
                        item=editedItem,
                        categories=categories,
                        default=editedItem.category_id)

        flash('Successfully Edited "%s"' % editedItem.name)
        return redirect(url_for('AllCategories'))
    else:
        categories = session.query(Category).all()
        return render_template(
            'editItem.html',
            item=editedItem,
            categories=categories,
            pics=pics,
            default=editedItem.category_id)


# Delete items on login
@app.route(
    '/catalog/<category_name>/<item_name>/delete',
    methods=[
        'GET',
        'POST'])
def deleteItem(category_name, item_name):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name=category_name).one()
    itemToDelete = session.query(
        Item).filter_by(name=item_name, category_id=category.id).one()
    picsToDelete = session.query(Pictures).join(
        Item).filter_by(id=itemToDelete.id).all()

    if itemToDelete.user_id != login_session['user_id']:
        return render_template('not_auth_del.html')

    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        for pic in picsToDelete:
            os.remove(pic.picture)
        flash('"%s" Successfully Deleted' % itemToDelete.name)
        return redirect(url_for('AllCategories'))
    else:
        return render_template(
            'deleteItem.html',
            item=itemToDelete,
            category=category)


# Making an API Endpoint (GET Request)
@app.route('/catalog.json')
def catalogJSON():
    # Access categories from database
    categories = session.query(Category).all()

    # Create empty dictionary and initialize it with categories
    Dict = {}
    Dict['Category'] = [i.serialize for i in categories]

    # Create empty nested dictionary, where Items would be placed
    for i in range(0, len(categories)):
        Dict['Category'][i]['Item'] = []

    # Access all items belonging to a category from a database
    for c in categories:
        cat_items = session.query(Item).filter_by(category_id=c.id).all()

        # Append serialized items to a list that is nested in a dictionary
        for i in cat_items:
            cat_items = i.serialize
            Dict['Category'][c.id - 1]['Item'].append(cat_items)

    # Use Jsonify function from Flask for security
    return jsonify(Dict)


# Helper function to check for the security of the file names
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Helper function to rename picture names
def Rename(filename):
    os.listdir('static/uploads')
    MyList = os.listdir('static/uploads')
    count = 0
    for s in MyList:
        count += s.count(filename.replace('.jpg', ''))

    return filename.replace('.jpg', '') + '_' + str(count) + '.jpg'


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You are now logged out.")
        return redirect(url_for('AllCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('AllCategories'))

if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

# Catalog website project.

Created by Srikanth Sridhara on 8th Sep 2017

This is a website about musical instruments. The initial page shows different categories of musical instruments. When a user clicks on any category, it shows different musical instruments in that category.
When any musical instrument is clicked, a popup-like Modal opens up with detailed information about the instrument. The initial page also shows a list of the latest category items added.

There is also a User authentication system using Oauth2 providers: Facebook and Google login. When a user is authenticated using Facebook or Google, he/she can add new categories, or edit/delete existing categories. When a user is not logged in, he/she will not be able to add/edit/delete any category/category item, the data can only be viewed. There is also a user Authorization system which makes sure that logged in users can only edit/delete items that they have created.

For styling and grid layout, [`bootstrap`](http://getbootstrap.com/) is used. To facebook and google icons, [`fontawesome`](http://fontawesome.io/) is used. Two custom fonts are used for text: [`Simplifica`](http://freetypography.com/2014/03/24/free-font-simplifica/) and [`Raleway`](https://fonts.google.com/specimen/Raleway).

## Important folders and files:

1. `app.py`:
    This is the main server side file. It contains all of the routes and API endpoints.

2. `database_setup.py`:
    This file creates a DB and adds all relevant tables(User, Categories, CategoryItems).

3. `database_populator.py`:
    This file is used to populate the DB with sample data for ease of use and to see the website in action.

4. `database_functions.py`:
    This file contains functions for all the CRUD operations done on the DB.

5. `client_secrets.json` and `fb_client_secrets.json`:
    They contain the client_id and client_secret for facebook and google oauth.

6. `templates\index.html`:
    This is the base html file containing all the styles and scripts used for the front end, along with the basic templating of the website.

7. `static\js\login.js`:
    This is the base javascript file for front end user authentication. This is responsible for sending back the tokens to the server using ajax.

8. `templates\`:
    This folder contains all the template html files for categories as well as category items.

9. `static\`:
    This folder contains all the static images, styling CSS files and javascript files for the front end.

10. `momentjs.py`:
    This is a utility file that uses `moment.js` to create a wrapper class to display datetime.

## Usage:

*  Go to the folder `\vagrant\catalog\`.
*  If there is a file called `inventory.db`, delete it.
*  Run the following: `python database_populator.py`. This will fill the DB with sample data.
*  Run the server thus: `python app.py`

## Modules used:

*  flask
*  flask.ext.httpauth
*  oauth2client.client (flow_from_clientsecrets and FlowExchangeError)
*  flask_login (login_user, logout_user, current_user, login_required, LoginManager)
*  sqlalchemy (create_engine, sessionmaker)
*  passlib.apps (custom_app_context)
*  itsdangerous (TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired)
*  momentjs

## Image credits:

Sample images were taken from these websites:
*  `dk1xgl0d43mu1.cloudfront.net`
*  `financesonline.com`
*  `mfas3.s3.amazonaws.com`
*  `sriveenavani.com`
*  `fmicassets.com`
*  `nps.gov`
*  `4.bp.blogspot.com`
*  `i.pinimg.com`
*  `jamunamusic.com`
*  `culturalinfusion.org.au`
*  `capitolmusic.files.wordpress.com`
*  `wonderopolis.org`
*  `korg.de`
*  `img.banggood.com`
*  `bestsaxophonewebsiteever.com`
*  `klarinetensaxofoonstage.be`
*  `instrumentoutfitters.com`
*  `trumpethub.com`
*  `wikimedia.org`

`momentjs.py` utility was taken from the Flask Mega-Tutorial by [`Miguel Grinberg`](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiii-dates-and-times)

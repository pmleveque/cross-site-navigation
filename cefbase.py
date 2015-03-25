# Ajout dans l'objet Menu d'un champ 'shared' et d'un champ 'author'
# Ajout de l'objet Administrator
import cgi
import os
import yaml
import StringIO
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

if os.environ.get('APPENGINE_RUNTIME') == 'python27':
    # internal django version is fine with python27
    from google.appengine._internal.django.utils.html import escape
else:
    # with python2.5 we load a more decent version than 0.96
    from google.appengine.dist import use_library
    use_library('django', '1.2')
    from django.utils.html import escape

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

NEW_VALUE_WHEN_DEPLOYED = os.environ['CURRENT_VERSION_ID']


class Menu(db.Model):
    name = db.StringProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    # special_kind sert a identifier les menus qui servent a composer les menus speciaux (ressources, dioceses...)
    special_kind = db.StringProperty()
    author = db.UserProperty()
    shared = db.BooleanProperty()


class Link(db.Model):
    name = db.StringProperty(required=True)
    menu = db.ReferenceProperty(Menu)
    date = db.DateTimeProperty(auto_now_add=True)
    url = db.LinkProperty()
    order = db.IntegerProperty(required=True)


class Navbar(db.Model):
    code = db.StringProperty(required=True) # should be lowercase (will be the script filename)
    name = db.StringProperty(required=True)
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    first_menu = db.ReferenceProperty(Menu, collection_name="navbar_first_set")
    second_menu = db.ReferenceProperty(Menu, collection_name="navbar_second_set")
    third_menu = db.ReferenceProperty(Menu, collection_name="navbar_third_set")
    fourth_menu = db.ReferenceProperty(Menu, collection_name="navbar_fourth_set")
    settings = db.StringListProperty()
    # cse: custom search engine
    cse_unique_id = db.StringProperty()


class Administrator(db.Model):
    user = db.UserProperty()
    admin = db.BooleanProperty(default= False)

import webapp2 as webapp

from google.appengine.ext import db
from google.appengine.ext import ndb
import os
from google.appengine.ext.webapp import template
import pickle
import logging
import yaml
import pprint


class Menu(db.Model):
    name = db.StringProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    # special_kind sert a identifier les menus qui servent
    #  a composer les menus speciaux (ressources, dioceses...)
    special_kind = db.StringProperty()
    author = db.UserProperty()
    shared = db.BooleanProperty()

    # helper to export links to the new MenuNDB
    def links_as_array(self):
        return [{'name': link.name, 'url': link.url} for link in
                sorted(self.link_set, key=lambda link: link.order)
                ]

    def to_ndb(self):
        return MenuNDB(
            name=self.name,
            date=self.date,
            special_kind=self.special_kind,
            author=self.author,
            shared=self.shared,
            links=self.links_as_array()
        )


class Link(db.Model):
    name = db.StringProperty(required=True)
    menu = db.ReferenceProperty(Menu)
    date = db.DateTimeProperty(auto_now_add=True)
    url = db.LinkProperty()
    order = db.IntegerProperty(required=True)


class Navbar(db.Model):
    # TODO: should be lowercase (will be the script filename)
    code = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    first_menu = db.ReferenceProperty(
        Menu, collection_name="navbar_first_set")
    second_menu = db.ReferenceProperty(
        Menu, collection_name="navbar_second_set")
    third_menu = db.ReferenceProperty(
        Menu, collection_name="navbar_third_set")
    fourth_menu = db.ReferenceProperty(
        Menu, collection_name="navbar_fourth_set")
    settings = db.StringListProperty()
    # cse: custom search engine
    cse_unique_id = db.StringProperty()

    def menus_as_array(self):
        return [menu.to_ndb() for menu in [self.first_menu,
                                           self.second_menu,
                                           self.third_menu,
                                           self.fourth_menu] if menu]

    def to_ndb(self):
        return NavbarNDB(
            code=self.code,
            name=self.name,
            author=self.author,
            date=self.date,
            menus=self.menus_as_array(),
            settings=self.settings,
            cse_unique_id=self.cse_unique_id
        )


class MenuNDB(ndb.Model):
    name = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    links = ndb.PickleProperty()
    # special_kind sert a identifier les menus qui servent
    # a composer les menus speciaux (ressources, dioceses...)
    special_kind = ndb.StringProperty()
    author = ndb.UserProperty()
    shared = ndb.BooleanProperty()


class MenuLinkNDB(ndb.Model):
    img_path = ndb.StringProperty(required=True)
    link = ndb.StringProperty(required=True)

    @classmethod
    def all():
        return super.query().fetch(1000)


class NavbarNDB(ndb.Model):
    # TODO: should be lowercase (will be the script filename)
    code = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    author = ndb.UserProperty()  # TODO: required
    date = ndb.DateTimeProperty(auto_now_add=True)
    menus = ndb.StructuredProperty(MenuNDB, repeated=True)
    menus_links = ndb.StructuredProperty(MenuLinkNDB, repeated=True)
    settings = ndb.PickleProperty()
    # cse: custom search engine
    cse_unique_id = ndb.StringProperty()


class Administrator(db.Model):
    user = db.UserProperty()
    admin = db.BooleanProperty(default=False)


class ImportPage(webapp.RequestHandler):
    def get(self):

        f = open(os.path.join(os.path.dirname(__file__), '../dump.yaml'))
        [navbars, menus, links, admins] = yaml.load(f)
        f.close()

        for item in links:
            item.put()

        for item in menus:
            item.put()

        for item in navbars:
            item.put()

        for item in admins:
            item.put()

        self.response.out.write('ok')


class DumpPage(webapp.RequestHandler):

    def get(self):
        self.response.headers.add_header("Content-Type", "text/x-yaml")

        navbars = Navbar.all().fetch(1000)
        menus = Menu.all().fetch(1000)
        links = Link.all().fetch(1000)
        admins = Administrator.all().fetch(1000)

        self.response.out.write(yaml.dump([navbars, menus, links, admins]))


class AdminPage(webapp.RequestHandler):

    def get(self):
        # logging.debug("value of my var is %s", str(menu1))

        path = os.path.join(
            os.path.dirname(__file__),
            'admin2.html'
        )

        self.response.out.write(
            template.render(
                path,
                {
                 'menus': Menu.all(),
                 'navbars': Navbar.all()
                 }
            )
        )

app = webapp.WSGIApplication([
    ('/admin2/dump.yaml', DumpPage),
    # ('/admin2/import', ImportPage),
    ('/admin2/', AdminPage),
], debug=True)

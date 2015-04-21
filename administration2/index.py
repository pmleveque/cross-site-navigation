import webapp2 as webapp

from google.appengine.ext import db
from models import *
from google.appengine.api.users import *
import os
from google.appengine.ext.webapp import template
import json
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

    def to_set(self):
        if self.author:
            author_email = str(self.author.email())
        else:
            author_email = None

        return {
            'name': self.name,
            'key': str(self.key()),
            'date': str(self.date),
            'special_kind': self.special_kind,
            'author': author_email,
            'shared': self.shared,
            'links': self.links_as_array(),
            }


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

    def menus_as_key_array(self):
        return [str(menu.key()) for menu in [self.first_menu,
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

    def to_set(self):
        if self.author:
            author_email = str(self.author.email())
        else:
            author_email = None

        return {
            'code': self.code,
            'name': self.name,
            'author': author_email,
            'date': str(self.date),
            'menus': self.menus_as_key_array(),
            'settings': self.settings,
            'cse_unique_id': self.cse_unique_id,
            }


class Administrator(db.Model):
    user = db.UserProperty()
    admin = db.BooleanProperty(default=False)

    def to_set(self):
        return {
            'user': self.user.email(),
            'admin': self.admin
        }


class ImportPage(webapp.RequestHandler):
    def get(self):
        self.response.headers.add_header("Content-Type", "text/text")

        f = open(os.path.join(os.path.dirname(__file__), 'dump.json'))
        [navbars, menus, admins] = json.load(f)
        f.close()

        for a in admins:
            admin = AdministratorNDB(
                user=User(a['user']),
                admin=a['admin']
            )
            admin.put()
            self.response.out.write(pprint.pformat(admin))

        new_menus = {}

        for m in menus:
            menu = MenuNDB(
                name=m['name'],
                # key=m['key'],
                # date=m['date'],
                special_kind=m['special_kind'],
                author=User(m['author']),
                shared=m['shared'],
                links=m['links'],
                )
            menu.put()
            new_menus[m['key']] = menu
            self.response.out.write(pprint.pformat(menu))

        for n in navbars:
            navbar = NavbarNDB(
                code=n['code'],
                name=n['name'],
                author=User(n['author']),
                # date=n['date'],
                # menus=n['menus'],
                settings=n['settings'],
                cse_unique_id=n['cse_unique_id'],
                )

            for key in n['menus']:
                navbar.menus.append(new_menus[key])

            navbar.put()
            self.response.out.write(pprint.pformat(navbar))


class DumpPage(webapp.RequestHandler):

    def get(self):
        self.response.headers.add_header("Content-Type", "application/json")

        navbars = map(lambda n: n.to_set(), Navbar.all().fetch(1000))
        menus = map(lambda n: n.to_set(), Menu.all().fetch(1000))
        admins = map(lambda n: n.to_set(), Administrator.all().fetch(1000))

        self.response.out.write(json.dumps([
            navbars, menus, admins
            ]))


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
    ('/admin2/dump.json', DumpPage),
    ('/admin2/import', ImportPage),
    ('/admin2/', AdminPage),
], debug=True)

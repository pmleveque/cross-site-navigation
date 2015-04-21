from google.appengine.ext import ndb


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

    # @classmethod
    # def all():
    #     return super.query().fetch(1000)


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


class AdministratorNDB(ndb.Model):
    user = ndb.UserProperty()
    admin = ndb.BooleanProperty(default=False)

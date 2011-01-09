from gae import db

class Currency(db.Model):
    UNIQUE      = ("name", "symbol")
    name        = db.StringProperty(max_length=50, required=True)
    symbol      = db.StringProperty(max_length=10, required=True)

    def __unicode__(self):
        return self.name

class Country(db.Model):
    '''Country'''
    KEY_NAME = "%(slug)s"
    slug     = db.SlugProperty("Short country form (us, uk, fr)", required=True, max_length=50)
    name     = db.StringProperty(required=True, max_length=100)
    # main currency used in this country
    currency = db.ReferenceProperty(Currency)

    def __unicode__(self):
        return self.name

class Region(db.Model):
    '''Region (state)'''
    KEY_NAME = "%(slug)s"
    slug     = db.SlugProperty("Short state form (kiev.ua, msk.ru, nw.us)", required=True, max_length=50)
    name     = db.StringProperty(required=True, max_length=100)
    country  = db.ReferenceProperty(reference_class=Country, required=True)

    def __unicode__(self):
        return "%s, %s" % (self.name, self.country)

class City(db.Model):
    '''City'''
    KEY_NAME = "%(slug)s"
    UNIQUE   = ("phone_code", ("name", "region"))
    slug     = db.SlugProperty("Short city form (kiev.ua, msk.ru, nw.us)", required=True, max_length=50)
    name     = db.StringProperty(required=True, max_length=100)
    region   = db.ReferenceProperty(reference_class=Region, required=True)
    phone_code  = db.StringProperty(max_length=6)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.region)
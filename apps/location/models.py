from gae.db import Model, UniqueModel, fields

class Currency(Model):
    UNIQUE      = ("name", "symbol")
    name        = fields.String(max_length=50, required=True)
    symbol      = fields.String(max_length=10, required=True)

    def __unicode__(self):
        return self.name

class Country(UniqueModel, Model):
    '''Country'''
    KEY_NAME = "%(slug)s"
    slug     = fields.Slug("short country form (us, uk, fr)", required=True, max_length=50)
    name     = fields.String(required=True, max_length=100)
    # main currency used in this country
    currency = fields.Reference(Currency)

    def __unicode__(self):
        return self.name

class Region(UniqueModel, Model):
    '''Region (state)'''
    KEY_NAME = "%(slug)s"
    slug     = fields.Slug("short state form (kiev, msk, ny)", required=True, max_length=50)
    name     = fields.String(required=True, max_length=100)
    country  = fields.Reference(reference_class=Country, required=True)

    def __unicode__(self):
        return self.name

    def full_name(self):
        return "%s, %s" % (self.name, self.country)

class City(UniqueModel, Model):
    '''City'''
    KEY_NAME = "%(slug)s"
    UNIQUE   = ("phone_code", ("name", "region"))
    slug     = fields.Slug("short city form (kiev, msk, ny)", required=True, max_length=50)
    name     = fields.String(required=True, max_length=100)
    region   = fields.Reference(reference_class=Region, required=True)
    phone_code  = fields.String(max_length=6)

    def __unicode__(self):
        return self.name

    def full_name(self):
        return "%s (%s)" % (self.name, self.region)

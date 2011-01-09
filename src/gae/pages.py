import re
from gae.db import Query
from math import ceil
from gae import webapp

class PagesException(Exception):
    pass

class Pages:
    _records = None

    def __init__(self, collection, on_page, attr_name="page", url=None):
        # check collection
        if not isinstance(collection, Query):
            raise PagesException("First parameter should be instance of google.appengine.ext.db.Query")
        self.collection = collection
        self.on_page = int(on_page)
        self.page = int(webapp.instance.request.GET.get(attr_name, 1) or 1)
        # prepare url
        if url is None:
            url = webapp.instance.request.path_qs
        # add new parameter to url
        if "?" in url:
            url = re.sub("([\?&])%s=[^&]*&?" % attr_name, "\\1", url).rstrip("&?")
            url = url + "&"
        else:
            url = url + "?"
        self.url = url + attr_name

    def total_pages(self):
        return int(ceil(float(self.collection.count()) / self.on_page))

    def current_page(self):
        return self.page

    def records(self):
        '''Return list of all objects on current page'''
        if self._records is None:
            offset = (self.page - 1) * self.on_page
            self._records = self.collection.fetch(self.on_page, offset)
        return self._records

    def __iter__(self):
        self._index = -1
        return self

    def next(self):
        self._index = self._index + 1
        records = self.records()
        if self._index >= len(records):
            raise StopIteration
        return records[self._index]

    def render_pages(self):
        '''Return numbers of pages'''
        total_pages = self.total_pages()
        start_range = self.current_page() > 2 and self.current_page() - 2 or 1
        end_range   = self.current_page() < total_pages - 2 and self.current_page() + 2 or total_pages
        pages = []
        # add 'back' and 'first' links
        if self.current_page() > 1:
            pages.append("<a href='%(prefix)s=1' class='first'>First</a>" % {'prefix': self.url})
            pages.append("<a href='%(prefix)s=%(page)s' class='back'>Back</a>" % {'page': self.current_page() - 1, 'prefix': self.url})
        for page in range(start_range, end_range+1):
            if page == self.current_page():
                pages.append("<a href='%(prefix)s=%(page)s' class='current'>%(page)s</a>" % {'page': page, 'prefix': self.url})
            else:
                pages.append("<a href='%(prefix)s=%(page)s'>%(page)s</a>" % {'page': page, 'prefix': self.url})
        # add 'next' and 'last' links
        if self.current_page() < total_pages:
            pages.append("<a href='%(prefix)s=%(page)s' class='next'>Next</a>" % {'page': self.current_page() + 1, 'prefix': self.url})
            pages.append("<a href='%(prefix)s=%(page)s' class='last'>Last</a>" % {'page': total_pages,'prefix': self.url})
        # insert data to tag <p>
        pages.insert(0, "<p class='pages'>")
        pages.append("</p>")
        return "\n".join(pages)
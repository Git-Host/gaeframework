from gae import template, webapp
from gae.markup import Wiki
from gae.tags import node_rule, BaseNode
from blog.models import Entity

register = template.create_template_register()

@register.tag
@node_rule(BaseNode, ("", "as [varname]"))
def get_recent_entries(self, context):
    '''Get list of latest blog posts'''
    collection = Entity.all().filter("active", True).order("-changed")
    collection.fetch(10)
    if hasattr(self, "varname"):
        context[self.varname] = collection
        return ""
    # TODO: delete dependency with webapp!
    return webapp.instance.render("blog/block/entries_list", {"entries": collection})

@register.tag
@node_rule(BaseNode, ("for [entry] as [varname]",))
def get_comment_count(self, context):
    '''Get count of comments for blog post'''
    if hasattr(self, "varname"):
        context[self.varname] = 0
        return ""
    return 0

@register.filter
def wiki(raw_data):
    return Wiki().parse(raw_data)
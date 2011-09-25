import logging, types
from django.template import VariableDoesNotExist
from django.template.defaultfilters import stringfilter
from django import template as django_template
from gae import template, db
from gae.tools.translation import translate as _
from gae.tools.urls import reverce_url
from gae.template.tag_elif import do_if


def node_rule(base_obj, rules):
    '''
    Decorator for logged users only.

    Args:
      rules - list of rules for users who have access (supported: admin)
    '''
    def wrap(handler_method):
        cls = type("NewNode", (base_obj,), {'render': handler_method, 'rules': rules})
        def tag_func(parser, token):
            return cls.handle_token(parser, token)
        tag_func.__name__ = handler_method.__name__
        return tag_func
    return wrap


class BaseNode(django_template.Node):
    """Base class for simplify creation of template tags"""
    rules = []

    def __init__(self, **kvargs):
        # set alla passed values to current class
        for name, value in kvargs.items():
            setattr(self, name, value)

    @classmethod
    def handle_token(cls, parser, token):
        """
        Class method to parse template tag and return a Node.
        Syntax defined into 'rules' class property.

        Syntex:
            {% get_xxx %}
            {% get_xxx as [varname] %}
            {% get_xxx for [object] as [varname] %}
            {% get_xxx for [model] [object_id] as [varname] %}
        """
        tokens = token.split_contents()[1:]
        # call tag without parameters
        if len(tokens) == 0:
            return cls()
        # convert one rule to tuple of rules
        if (type(cls.rules) == types.StringType):
            cls.rules = (cls.rules, )
        rules = [rule.strip().split(" ") for rule in cls.rules]
        # find rules for current tag by number of arguments
        rules = [rule for rule in rules if len(rule) == len(tokens)]
        # convert rules from line to list
        # match correct syntax for tag
        rule_found = None
        for rule in rules:
            rule_found = True
            for a, b in zip(rule, tokens):
                if not (a == b or (a.startswith('[') and a.endswith(']'))):
                    rule_found = None
            if rule_found:
                rule_found = rule
                break
        # rule not found
        if not rule_found:
            raise django_template.TemplateSyntaxError("Incorrect arguments in %r template tag" % token.split_contents()[0])
        # get params for class
        params = dict([(a[1:-1], b) for a, b in zip(rule_found, tokens) if a.startswith('[') and a.endswith(']')])
        # create object instance
        return cls(**params)

    def get_object(self, context):
        '''Return object based on parameter: object_instance or object_type and object_id'''
        try:
            # restore object by variable name
            if self.object_instance:
                obj = django_template.resolve_variable(self.object_instance, context)
            # get object by id
            elif self.object_type is not None and self.object_id is not None:
                # TODO: need import module before using
                obj = getattr(self.object_type, 'get_by_id')(int(self.object_id))
            else:
                obj = None
        except (AttributeError, VariableDoesNotExist), err:
            obj = None
        return obj

    @staticmethod
    def get_var(context, var_name):
        '''Return object based on parameter: object_instance or object_type and object_id'''
        try:
            # restore object by variable name
            obj = django_template.resolve_variable(var_name, context)
        except (AttributeError, VariableDoesNotExist), err:
            logging.warn("Template variable '%s' does not exists" % var_name)
            obj = None
        return obj


class UrlNode(django_template.Node):
    args = []
    kwargs = {}
    
    def __init__(self, tag_name, params):
        self.full_tag = "{%% %s %s %%}" % (tag_name, " ".join(params))
        self.url_short_name = params[0]
        for param in params[1:]:
            try:
                name, value = param.split("=")
                self.kwargs[name] = value
            except:
                self.args.append(param)

    def render(self, context):
        '''Resolve variables and return complete url address'''
        args = []
        for value in self.args:
            args.append(self._resolve_variable(context, value))

        kwargs = {}
        for name, value in self.kwargs.items():
            kwargs[name] = self._resolve_variable(context, value)
        
        return reverce_url(self.url_short_name, *args, **kwargs)

    def _resolve_variable(self, context, name):
        '''Return value for variable name'''
        value = BaseNode.get_var(context, name)
        # use key name or id if passed models instance
        if isinstance(value, db.Model):
            key = value.key()
            value = key.name() or key.id() or key
        return value


register = template.create_template_register()


@register.tag
@node_rule(BaseNode, ('[text]', '[text] [app_name]'))
def translate(self, context):
    '''Return translated text'''
    text = self.get_var(context, self.text)
    if hasattr(self, "app_name"):
        return _(text, self.app_name)
    return _(text)

@register.tag
def url(parser, token):
    tag_name = token.split_contents()[0]
    try:
        params = token.split_contents()[1:]
        return UrlNode(tag_name, params)
    except ValueError:
        raise django_template.TemplateSyntaxError, "%r tag requires an arguments" % tag_name

@register.filter(name='translate')
@stringfilter
def filter_translate(text):
    '''Return translated text'''
    return _(text)

@register.filter
def debug(content):
    return "Type: %s. Properties: %s" % (type(content), dir(content))

@register.tag
@node_rule(BaseNode, ('[paginator]',))
def pagination(self, context):
    '''Return pagination links'''
    paginator = self.get_var(context, self.paginator)
    return template.render('common/pagination.html', {"paginator": paginator})

register.tag("if", do_if)
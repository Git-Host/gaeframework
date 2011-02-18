from gae import webapp

def get_object_or_404(model, key_name):
    '''Return object with given key or show "page not found"'''
    obj = model.get_by_key_name(key_name) or model.get_by_id(int(key_name)) or model.get(key_name)
    if not obj:
        webapp.instance.error(404)
        raise Exception("Object '%s' with key '%s' not found" %
                        (model.__name__, key_name))
    return obj

def get_objects_or_404(model, **kwargs):
    '''Return object with given criteria or show "page not found"'''
    collection = model.all()
    for filed_name, value in kwargs.items():
        collection = collection.filter(filed_name, value)
    return collection

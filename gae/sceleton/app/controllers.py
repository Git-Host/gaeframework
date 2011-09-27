
def index(request):
    '''
    Render main page.

    Template located in "apps/[app_name]/templates/index.html"
    
    You can also do:
      * show plain text with
        return request.text("Hello World!")

      * show data representation in XML
        return request.xml({'city': 'California', 'ccountry': 'USA'})

      * show data representation in JSON
        return request.json({'city': 'California', 'ccountry': 'USA'})
    '''
    return request.render("[app_name]/index")
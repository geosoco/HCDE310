from django.conf import settings # import the settings file

def base_url(context):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'BASE_URL': settings.BASE_URL}

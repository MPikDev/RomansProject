from django.contrib import admin
# from .models import *
import web_part.models
acceptable_bases = ['Model', 'AbstractBaseUser', 'UpdateableModel']



for name in dir(web_part.models):
    klass = getattr(web_part.models, name)

    if hasattr(klass, '__bases__'):
        bases = [k.__name__ for k in klass.__bases__]
        if any(x in acceptable_bases for x in bases):
            if hasattr(klass, '_meta'):
                if klass._meta.abstract:
                    continue

            if hasattr(klass, '__module__'):
                if klass.__module__ == 'django.contrib.auth.models':
                    continue

            admin_klass = globals().get(klass.__name__ + 'Admin', None)
            admin.site.register(klass, admin_klass)

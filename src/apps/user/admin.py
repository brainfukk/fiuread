from django.contrib import admin

from .models import Event, UserPurse, UserUnitRelation

admin.site.register(Event)
admin.site.register(UserPurse)
admin.site.register(UserUnitRelation)

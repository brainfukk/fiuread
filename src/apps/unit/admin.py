from django.contrib import admin

from .models import Unit, UnitExerciseElement, UnitTheoryElement, Topic


admin.site.register(Topic)
admin.site.register(Unit)
admin.site.register(UnitTheoryElement)
admin.site.register(UnitExerciseElement)

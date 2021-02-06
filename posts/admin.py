from django.contrib import admin

from .models import Character

class CharacterModelAdmin(admin.ModelAdmin):
    class Meta:
        model = Character


admin.site.register(Character, CharacterModelAdmin)

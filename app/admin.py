from django.contrib import admin

from app.models import *


class ThemeAdmin(admin.ModelAdmin):
    list_display = ['title']

class UrlAdmin(admin.ModelAdmin):
    list_display = ['title','url']


admin.site.register(Operator)
admin.site.register(Theme,ThemeAdmin)
admin.site.register(RequestLog)
admin.site.register(Urls,UrlAdmin)

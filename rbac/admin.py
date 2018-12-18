from django.contrib import admin
from . import models


class User2RoleInline(admin.TabularInline):
    model = models.User2Role
    
    
class Permission2Action2RoleInline(admin.TabularInline):
    model =models.Permission2Action2Role
    
    
class Permission2ActionInline(admin.TabularInline):
    model = models.Permission2Action
    

class ActionInline(admin.TabularInline):
    model = models.Action


class PermissionInline(admin.TabularInline):
    model = models.Permission


class RoleAdmin(admin.ModelAdmin):

    inlines = [
        User2RoleInline,
        Permission2Action2RoleInline,

    ]


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('url', 'caption', 'menu')
    inlines = [
        Permission2ActionInline,
    ]


class MenuInline(admin.TabularInline):
    model = models.Menu


class MenuAdmin(admin.ModelAdmin):
    list_display = ('caption', 'parent')
    inlines = [
        MenuInline,
    ]
# admin.site.empty_value_display = 'No Value'
admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.Role, RoleAdmin)
# admin.site.register(models.Action)
# admin.site.register(models.Permission2Action)
# admin.site.register(models.Permission2Action2Role)
admin.site.register(models.Menu, MenuAdmin)
# admin.site.register(models.User2Role)

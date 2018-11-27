from django.contrib import admin
from repository import models

# Register your models here.
admin.site.register(models.Article)
admin.site.register(models.Category)
admin.site.register(models.Blog)
admin.site.register(models.UserInfo)
admin.site.register(models.UserFans)

from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Company)
admin.site.register(Project)
admin.site.register(Task)
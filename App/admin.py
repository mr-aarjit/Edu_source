from django.contrib import admin
from .models import Sub_group, Group,  index_file

admin.site.site_title = "<Edu Source>"
admin.site.site_header = "Edu Source"

admin.site.register(Sub_group)
admin.site.register(Group)
admin.site.register(index_file)

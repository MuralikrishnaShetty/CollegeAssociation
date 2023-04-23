from django.contrib import admin
from .models import Post, Finance
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# class AccountInline(admin.StackedInline):
#     model =  StaffStatus
#     can_delete = False
#     verbose_name_plural=' StaffStatus'

# class CustomizeUserAdmin(UserAdmin):
#     inlines = (AccountInline,)

# admin.site.unregister(User) 
# admin.site.register(User,CustomizeUserAdmin)

admin.site.register(Post)
admin.site.register(Finance)
from django.contrib import admin
from .models import ChatModel, UserProfileModel

# Register your models here.


admin.site.register(ChatModel)
admin.site.register(UserProfileModel)
from django.contrib import admin
from .models import  TelegramUser, TelegramState, TelegramChat

admin.site.register( TelegramUser)
admin.site.register( TelegramState )
admin.site.register( TelegramChat )
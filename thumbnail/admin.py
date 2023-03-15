from django.contrib import admin
from .models import User, AccountTier, ThumbnailSize

admin.site.register(User)
admin.site.register(AccountTier)
admin.site.register(ThumbnailSize)

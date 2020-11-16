from django.contrib import admin
from django_otp.plugins.otp_totp.models import TOTPDevice


# Register your models here.

from.models import MyUsers
# Register your models here.

admin.site.register(MyUsers)
admin.site.register(TOTPDevice)


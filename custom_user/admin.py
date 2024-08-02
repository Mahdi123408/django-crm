from django.contrib import admin
from . import models


class TimeWorkUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'start_time', 'end_time', 'time_work')


admin.site.register(models.TimeWorkUser, TimeWorkUserAdmin)


class UserExportsAdmin(admin.ModelAdmin):
    list_display = ('user', 'price_count', 'date', 'description')


admin.site.register(models.UserExports, UserExportsAdmin)


class UserWorksHourRequestsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'start_time')


admin.site.register(models.UserWorksHourRequests, UserWorksHourRequestsAdmin)

from django.contrib import admin
import core.models

admin.site.register(core.models.Account)
admin.site.register(core.models.AccountHolder)
admin.site.register(core.models.AnchorEvent)

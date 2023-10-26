from django.contrib import admin
import core.models

admin.site.register(core.models.Account)
admin.site.register(core.models.AnchorEvent)
admin.site.register(core.models.Customer)
admin.site.register(core.models.ReceiptPrinter)
from django.contrib import admin

import core.models
# Register your models here.
admin.site.register(core.models.Customer)
admin.site.register(core.models.ReceiptPrinter)
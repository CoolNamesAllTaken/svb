from django.contrib import admin
import core.models

# Register all the models you want to be able to see with the admin interface!
admin.site.register(core.models.Account)
admin.site.register(core.models.AnchorEvent)
admin.site.register(core.models.Customer)
admin.site.register(core.models.ReceiptPrinter)
admin.site.register(core.models.NewsArticle)
admin.site.register(core.models.NewsAuthor)
admin.site.register(core.models.BankState)
admin.site.register(core.models.DebitCardPrintJob)
from django.contrib import admin

from Apps.Catalogos.Met_Payment.models import metPayment

@admin.register(metPayment)
class metPaymentAdmin(admin.ModelAdmin):
    list_display = ['idPayment','namePayment','DescriptionPayment']
    search_fields = ['namePayment']
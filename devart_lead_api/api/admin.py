from django.contrib import admin
from api.models import Source, Key, Lead, Request, Offer
from django.utils.translation import gettext as _


# Register your models here.


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("name",)
    verbose_name = _("Source")
    verbose_name_plural = _("Sources")


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ("name", "api_key")
    verbose_name = _("Key")
    verbose_name_plural = _("Keys")


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("rodne_cislo", "source", "is_owner")
    verbose_name = _("Lead")
    verbose_name_plural = _("Leads")


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("rodne_cislo", "source", "checked",
                    "accepted", "created_at")
    readonly_fields = ("created_at", "source")
    verbose_name = _("Offer")
    verbose_name_plural = _("Offers")


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("recieved_at", "ip")
    readonly_fields = ('recieved_at', "ip", "headers", "data")
    verbose_name = _("Request")
    verbose_name_plural = _("Requests")

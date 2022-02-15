from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone


class Source(models.Model):
    name = models.CharField(_("Name"), max_length=255, blank=False, null=False)
    active = models.BooleanField(_("Active"), default=True)
    # TODO: add more fields

    def __str__(self):
        return self.name


class Key(models.Model):
    name = models.CharField(_("Key Identifier"),
                            max_length=255, null=False, blank=False)
    api_key = models.CharField(
        _("API Key"), max_length=511, unique=True, null=False, blank=False)
    active = models.BooleanField(_("Active"), blank=False, null=False)
    source = models.ForeignKey(_("Source"), Source)

    def __str__(self):
        # Dont change for now, or edit sleep in views
        return self.name + " pro zdroj " + str(self.source)


class Lead(models.Model):
    rodne_cislo = models.CharField(_("Rodne Cislo"),
                                   max_length=20, null=False, blank=False, unique=True)
    is_owner = models.BooleanField(_("Owner"), default=False)
    price = models.DecimalField(
        _("Price"), max_digits=15, decimal_places=2, default=0.00)

    bought = models.BooleanField(
        _("Bought"), blank=False, null=False, default=False)
    source = models.ForeignKey(_("Source"), Source)
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()

    first_name = models.CharField(_("First name"),
                                  max_length=255, null=True, blank=True, default=None)
    last_name = models.CharField(_("Last name"),
                                 max_length=255, null=True, blank=True, default=None)
    phone_number = models.CharField(_("Phone number"),
                                    max_length=255, null=True, blank=True, default=None)
    requested_amount = models.CharField(_("Requested amount"),
                                        max_length=255, null=True, blank=True, default=None)
    email = models.EmailField(_("Email"), null=True, blank=True, default=None)
    income = models.CharField(_("Income"),
                              max_length=255, null=True, blank=True, default=None)
    addr_street = models.CharField(_("Street"),
                                   max_length=255, null=True, blank=True, default=None)
    addr_city = models.CharField(_("City"),
                                 max_length=255, null=True, blank=True, default=None)
    addr_zip = models.CharField(_("ZIP"),
                                max_length=255, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Lead, self).save(*args, **kwargs)

    def __str__(self):
        return self.rodne_cislo + " od zdroje " + str(self.source)


class Offer(models.Model):
    rodne_cislo = models.CharField(_("Rodne Cislo"),
                                   max_length=20, null=False, blank=False)
    price = models.DecimalField(
        _("Price"), max_digits=15, decimal_places=2, default=0.00)

    checked = models.BooleanField(
        _("Checked"), blank=False, null=False, default=False)
    lead = models.ForeignKey(Lead, blank=True, null=True,
                             default=None, on_delete=models.SET_NULL)  # add unique=True ?
    accepted = models.BooleanField(
        _("Accepted"), blank=False, null=False, default=False)
    source = models.ForeignKey(_("Source"), Source)
    created_at = models.DateTimeField(_("Created at"), editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(Offer, self).save(*args, **kwargs)

    def __str__(self):
        return self.rodne_cislo + " od zdroje " + str(self.source)


class Request(models.Model):
    recieved_at = models.DateTimeField(
        _("Recieved at"), auto_created=True, auto_now=True)
    url = models.CharField(_("URL"), max_length=255)
    ip = models.CharField(_("IP address"), max_length=255)
    headers = models.TextField(_("Headers"))
    data = models.TextField(_("Data"))


class AcceptData(models.Model):
    rodne_cislo = models.CharField(_("Rodne Cislo"),
                                   max_length=20, null=False, blank=False, unique=True)

    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()

    first_name = models.CharField(_("First name"),
                                  max_length=255, null=True, blank=True, default=None)
    last_name = models.CharField(_("Last name"),
                                 max_length=255, null=True, blank=True, default=None)
    phone_number = models.CharField(_("Phone number"),
                                    max_length=255, null=True, blank=True, default=None)
    requested_amount = models.CharField(_("Requested amount"),
                                        max_length=255, null=True, blank=True, default=None)
    email = models.EmailField(_("Email"), null=True, blank=True, default=None)
    income = models.CharField(_("Income"),
                              max_length=255, null=True, blank=True, default=None)
    addr_street = models.CharField(_("Street"),
                                   max_length=255, null=True, blank=True, default=None)
    addr_city = models.CharField(_("City"),
                                 max_length=255, null=True, blank=True, default=None)
    addr_zip = models.CharField(_("ZIP"),
                                max_length=255, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Lead, self).save(*args, **kwargs)

    def __str__(self):
        return self.rodne_cislo + " od zdroje " + str(self.source)

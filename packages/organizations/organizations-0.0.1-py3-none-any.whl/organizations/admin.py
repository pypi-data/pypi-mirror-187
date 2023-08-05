from django.contrib import admin
from .models import Intermediary, Organization, OrganizationDID, OrganizationKeys, Issuer, UserProxy


class IntermediaryAdmin(admin.ModelAdmin):
    model = Intermediary


class OrganizationAdmin(admin.ModelAdmin):
    model = Organization


class OrganizationDIDAdmin(admin.ModelAdmin):
    model = OrganizationDID


class OrganizationKeysAdmin(admin.ModelAdmin):
    model = OrganizationKeys


class IssuerAdmin(admin.ModelAdmin):
    model = Issuer


class UserProxyAdmin(admin.ModelAdmin):
    model = UserProxy
    fields = ("username", "first_name", "last_name", "email")


admin.site.register(Intermediary, IntermediaryAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationDID, OrganizationDIDAdmin)
admin.site.register(OrganizationKeys, OrganizationKeysAdmin)
admin.site.register(Issuer, IssuerAdmin)
admin.site.register(UserProxy, UserProxyAdmin)

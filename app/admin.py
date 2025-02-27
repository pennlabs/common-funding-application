from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from .models import (
    CCEmail,
    CFAUser,
    CommonFollowupQuestion,
    CommonFreeResponseQuestion,
    EligibilityQuestion,
    Event,
    FollowupQuestion,
    FreeResponseQuestion,
    FunderConstraint,
)


class CFAUserAdmin(admin.ModelAdmin):
    filter_horizontal = ("cc_emails",)
    search_fields = ("user__username",)
    list_display = ("user", "user_type", "osa_email")
    list_filter = ("user_type",)


class EventAdmin(admin.ModelAdmin):
    search_fields = ("name", "requester__user__username")
    list_filter = ("status", "created_at")


admin.site.unregister(Group)
admin.site.unregister(Site)

admin.site.register(CFAUser, CFAUserAdmin)
admin.site.register(EligibilityQuestion)
admin.site.register(CommonFreeResponseQuestion)
admin.site.register(FreeResponseQuestion)
admin.site.register(CommonFollowupQuestion)
admin.site.register(FollowupQuestion)
admin.site.register(FunderConstraint)
admin.site.register(Event, EventAdmin)
admin.site.register(CCEmail)

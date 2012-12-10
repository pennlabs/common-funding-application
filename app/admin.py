from django.contrib import admin

from models import (CFAUser, CommonFreeResponseQuestion, EligibilityQuestion,
                    FreeResponseQuestion, FunderConstraint, Event,
                    CommonFollowupQuestion, FollowupQuestion, CCEmail)

from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Group

class CFAUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'osa_email')

admin.site.unregister(Group)
admin.site.unregister(Site)

admin.site.register(CFAUser, CFAUserAdmin)
admin.site.register(EligibilityQuestion)
admin.site.register(CommonFreeResponseQuestion)
admin.site.register(FreeResponseQuestion)
admin.site.register(CommonFollowupQuestion)
admin.site.register(FollowupQuestion)
admin.site.register(FunderConstraint)
admin.site.register(Event)
admin.site.register(CCEmail)

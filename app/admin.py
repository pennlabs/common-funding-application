from django.contrib import admin

from models import (CFAUser, CommonFreeResponseQuestion, EligibilityQuestion,
                    FreeResponseQuestion, FunderConstraint)


class CFAUserAdmin(admin.ModelAdmin):
    list_display = ('user_type', 'osa_email')


admin.site.register(CFAUser, CFAUserAdmin)
admin.site.register(EligibilityQuestion)
admin.site.register(CommonFreeResponseQuestion)
admin.site.register(FreeResponseQuestion)
admin.site.register(FunderConstraint)

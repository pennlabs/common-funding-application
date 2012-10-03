from django.contrib import admin
from models import (CFAUser, CommonFreeResponseQuestion, EligibilityQuestion,
                    FreeResponseQuestion, FunderConstraint)


admin.site.register(CFAUser)
admin.site.register(EligibilityQuestion)
admin.site.register(CommonFreeResponseQuestion)
admin.site.register(FreeResponseQuestion)
admin.site.register(FunderConstraint)

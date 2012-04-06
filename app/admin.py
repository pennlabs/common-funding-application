from django.contrib import admin
from models import FreeResponseQuestion, CFAUser, Event, \
    EligibilityQuestion, CommonFreeResponseAnswer, FunderConstraint


admin.site.register(FreeResponseQuestion)
admin.site.register(CFAUser)
admin.site.register(Event)
admin.site.register(EligibilityQuestion)
admin.site.register(CommonFreeResponseAnswer)
admin.site.register(FunderConstraint)


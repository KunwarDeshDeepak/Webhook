from django.contrib import admin
from handler.models import Webhook, SasSActions,SasSSheetMap,JiraSetup, User, AccessToken

# Register your models here.
admin.site.register(Webhook)
admin.site.register(SasSSheetMap)
admin.site.register(SasSActions)
admin.site.register(AccessToken)
admin.site.register(JiraSetup)



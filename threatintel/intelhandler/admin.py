from django.contrib import admin
from threatintel.intelhandler.models import Feed, Indicator, Tag

admin.site.register(Indicator)
admin.site.register(Feed)
admin.site.register(Tag)

from django.contrib import admin
from .models import Welfare

# Register your models here.
class WelfareAdmin(admin.ModelAdmin):
    list_display=('domain','title','description','link')

admin.site.register(Welfare,WelfareAdmin)
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Illness)
admin.site.register(IllnessType)
admin.site.register(Treatment)
admin.site.register(MedicalHistoryRecord)

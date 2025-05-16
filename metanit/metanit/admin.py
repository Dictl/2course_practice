from django.contrib import admin
from .models import *

@admin.register(ComponentCategory)
class ComponentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')

admin.site.register(Component)
admin.site.register(CPU)
admin.site.register(GPU)
admin.site.register(RAM)
admin.site.register(Motherboard)
admin.site.register(SSD)
admin.site.register(HDD)
admin.site.register(PSU)
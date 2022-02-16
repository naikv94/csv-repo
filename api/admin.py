from django.contrib import admin
from .models import File, Data

# Register your models here.
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id','csv_file','uploaded']

@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = ['id','image_name','objects_detected','timestamp']

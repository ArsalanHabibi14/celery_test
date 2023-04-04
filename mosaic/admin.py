from django.contrib import admin
from .models import *


# Mosaic Admin Model
class MasterImageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "show_size", "thumbnail_image"]


# Album Admin Model
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["__str__", "show_thumbnail_image"]


admin.site.register(MasterImage, MasterImageAdmin)  # Register The Master Model
admin.site.register(Album, AlbumAdmin)  # Register The Album Model


# ZipFile Admin Model
class ZipFileAdmin(admin.ModelAdmin):
    list_display = ["__str__", "expired_time"]


admin.site.register(ZipAlbumFiles, ZipFileAdmin)  # Register ZipAlbumFile Model


# Mosaic Admin Model
class MosaicAdmin(admin.ModelAdmin):
    list_display = ["__str__", "master_image_thumbnail", "show_mosaic_thumbnail"]


admin.site.register(Mosaic, MosaicAdmin)  # Register The Mosaic Model

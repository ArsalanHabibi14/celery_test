from django.db.models.signals import pre_save, post_delete
from .models import *
import shutil
from .utils import MASTER_PATH


def set_size(sender, instance, **kwargs):
    """Set The Size When The Master Image Upload"""
    data_mb, data_kb = convert_size(instance.master_image.size)
    instance.size = data_kb


pre_save.connect(set_size, MasterImage)  # Connect to Master Image Signals


def album_delete(sender, instance, **kwargs):
    """Delete The Album File Or Zipfile when an Album Delete"""
    # Check If The Album Extracted Delete The All Images
    if instance.image_folder_path:
        if os.path.exists(instance.image_folder_path):
            shutil.rmtree(instance.image_folder_path)

    # Check If The Album is Zip Delete The Zipfile
    elif instance.image_zip:
        if os.path.exists(instance.image_zip.path):
            os.remove(instance.image_zip.path)


post_delete.connect(album_delete, Album)  # Connect The Album Delete Signal


#


def zipfile_delete(sender, instance, **kwargs):
    """Delete A Zipfile when the ZipFile Model Deleted"""

    # Check This Zipfile Model Have a zip file
    if instance.zipfile:
        # Check The Zipfile exists to delete
        if os.path.exists(instance.zipfile.path):
            os.remove(instance.zipfile.path)  # Remove The file


# Connect to the zipfile
post_delete.connect(zipfile_delete, ZipAlbumFiles)


#


def delete_mosaic(sender, instance, **kwargs):
    """Delete The Mosaic Signals when the mosaic delete the mosaic result should delete"""
    # Check The Mosaic Result Exists
    if instance.mosaic_result_path:
        # Check The Mosaic Result Image Path Exists
        if os.path.exists(instance.mosaic_result_path):
            os.remove(instance.mosaic_result_path)  # Delete the mosaic photo


post_delete.connect(delete_mosaic, Mosaic)  # Just Connect To The Signals


def delete_master(sender, instance, **kwargs):
    """Delete The Master Image Signals when the Master delete the mosaic result should delete"""
    # Check The Mosaic Result Exists
    if instance.master_image:
        # Check The Mosaic Result Image Path Exists
        if os.path.exists(instance.master_image.path):
            file_path = os.path.join(settings.MEDIA_ROOT, MASTER_PATH, instance.user.id)
            shutil.rmtree(file_path)  # Delete the mosaic photo


post_delete.connect(delete_master, MasterImage)  # Just Connect To The Signals

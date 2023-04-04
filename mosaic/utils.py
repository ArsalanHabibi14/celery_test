import os
import uuid
from django import forms
from rest_framework import status
from rest_framework.response import Response
from datetime import timedelta
from users.models import *

ALBUM_FILE = "album/"
MASTER_PATH = "master/"

# =====================================================


def validate_file_extension(value):
    """
    This Function checks if the file extension is valid
    """
    format_types = [".jpg", ".png", ".jpeg"]
    ext = os.path.splitext(value.name)[1]

    # Check That The Image format is valid
    if not ext in format_types:
        raise forms.ValidationError(f"The image file type must be PNG or JPG")


# =====================================================


def validate_file_size(value):
    """
    Validate the file size value!
    """
    size = value.size  # Get The File Sizes

    # Convert The Byte size to Kilo Byte Size
    data_kb = size / 1024

    # Convert The Byte Size to the Mega Byte Size
    data_mb = size / (1024 * 1024)

    # Validate The Maximum Size That Should not be greater than 20 MB
    if int(data_mb) > 20:
        raise forms.ValidationError("The Image Size Should not be greater than 20 MB")

    # Validate The Minimum Size That Should not be greater than 10 KB
    elif int(data_kb) < 10:
        raise forms.ValidationError("The Image Size Should not be smaller than 10 KB")


# =====================================================


def get_file_name(file_name):
    """
    This function is used to get the name and extension of an image and return them
    """
    basename = os.path.basename(file_name)
    name, ext = os.path.splitext(basename)

    return name, ext


# =====================================================


def set_final_name(instance, file_path):
    """Set The Final Path and name Of The Master Image"""

    name, ext = get_file_name(file_path)
    final_name = (
        f"{MASTER_PATH}{instance.user.id}/{instance.id}-{instance.user.email}{ext}"
    )
    return final_name


# =====================================================


def set_final_album_name(instance, file_path):
    """Set The Final Path and name Of The Album Images"""
    name, ext = get_file_name(file_path)
    final_name = f"{ALBUM_FILE}/{instance.id}/{str(uuid.uuid4())[:13]}{ext}"
    return final_name


# =====================================================


def convert_size(size):
    """
    This function converts the size of the file!
    """
    # Convert The Byte size to Mega Byte Size
    data_mb = size / (1024 * 1024)

    # Convert The Byte Size to Kilo Byte Size
    data_kb = size / 1024

    return int(data_mb), int(data_kb)  # Return The Converted Size


# =====================================================


def get_file_size(file_path):
    """
    This Function is used to get the size of a file!
    """
    file_stats = os.stat(file_path)
    data_mb = file_stats.st_size / (1024 * 1024)
    data_kb = file_stats.st_size / 1024
    return int(data_mb), int(data_kb)


# ======================================================


def check_the_image(master_image):
    """
    Validate the image Type and Size For The Models!
    """
    name, ext = get_file_name(master_image.path)

    format_types = [".jpg", ".png"]
    # Check The Images Path
    if str(ext).lower() in format_types:

        # Get The Master Image Size
        size = master_image.size

        # Convert The Byte size to Kilo Byte Size
        data_kb = size / 1024

        # Convert The Byte Size To Mega byte Size
        data_mb = size / (1024 * 1024)

        # Validate The Maximum Size That Should not be greater than 20 MB
        if int(data_mb) > 20:
            raise forms.ValidationError(
                "The Image Size Should not be greater than 20 MB"
            )

        # Validate The Minimum Size That Should not be greater than 10 KB
        elif int(data_kb) < 10:
            raise forms.ValidationError(
                "The Image Size Should not be smaller than 10 KB"
            )

    # Raise an Error because the file extension is valid or not
    else:
        raise forms.ValidationError(
            f"The Image type must be PNG or JPG but you uploaded a file with the {ext} format"
        )


# =====================================
def check_image(get_image, format_types, name, max_size, min_size):
    """Check the all images for API"""
    # Check Master Image
    if get_image is None:
        return False, Response({"detail": f"{name} Should upload!"})

    # Call The Convertor Size function
    data_mb, data_kb = convert_size(get_image.size)

    # Get The Name and Extension Of Image
    name, ext = get_file_name(get_image.name)

    # Check The Image Extension Valid Or not
    if not str(ext).lower() in format_types:
        return False, Response(
            {"detail": f"{name} Should not be {ext} Image Should be {format_types}"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Validate The Maximum Size That Should not be greater than 20 MB
    elif data_mb > max_size:
        return False, Response(
            {"detail": f"{name} Should not be greater than {max_size} MB!"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Validate The Maximum Size That Should not be greater than 10 KB
    elif data_kb < min_size:
        return False, Response(
            {"detail": f"{name} Should not be greater than {min_size} KB!"},
            status=status.HTTP_403_FORBIDDEN,
        )
    # Check The Image Type

    else:
        return True, True


# ============================================================


def expire_time():
    """
    Set The Expire Time Of an image
    """
    now = timezone.now()
    later = now + timedelta(minutes=1)
    return later


# ==================================================
def random_set_name(filename):
    """Generate the Random Name for images"""
    basename = os.path.basename(filename)  # Get The Base Name of file
    name, ext = os.path.splitext(basename)  # Get The Name and Extension of file
    final_name = f"{str(uuid.uuid4())[:5]}{ext}"  # Set The The Name Of File
    return final_name  # Return The final name


# ===========================================


def processed_dir_file(instance, file_path):
    """Set The Rendered Album Path"""

    name, ext = get_file_name(file_path)
    file_name = f"{instance.image_folder_path}/{instance.id}{ext}"
    return file_name

# Import Required Modules
import shutil
from .models import *
import zipfile
from .utils import *
import json
from django.core.files.base import ContentFile
from io import BytesIO
from datetime import timedelta
from django.utils import timezone
from celery import shared_task

# from .mosaic_code.render import create_mosaic
# from .mosaic_code.GalleryProcessing import GalleryProcessing


@shared_task
def upload_photo(zip_file_path, extract_to, album_id, title):
    """
    This function is used to extract the images and upload them in database
    """
    # try:
    # Some Configuration
    count = 0
    count_all_files = 0
    album = Album.objects.filter(id=album_id).first()
    format_types = [".jpg", ".png", ".jpeg"]

    # Create The file
    report_files = {}
    main_data = {}

    # Check The Zip Album file Exists
    if album.image_zip is None:
        album = ZipAlbumFiles.objects.filter(album=album).first()

    # Open The zipfile
    with zipfile.ZipFile(zip_file_path) as zip_file:
        # Get The Path
        path = f"{extract_to}/"
        counter = 1
        # Check The File exists if not exists create the directory
        if not os.path.exists(path):
            os.makedirs(path)
        # ============================================

        # iterate the zipfiles
        for zip_info in zip_file.infolist():
            count_all_files += 1
            another_path = f"{path}/"

            # Check the main path exists or not if not exists create the directory
            if not os.path.exists(another_path):
                os.makedirs(another_path)

            # Get The Name of images
            if zip_info.filename[-1] == "/":
                continue

            # Process The Images
            name, ext = get_file_name(zip_info.filename)

            # Report to the user
            if str(ext).lower() not in report_files:
                report_files[str(ext).lower()] = 0
            else:
                report_files[str(ext).lower()] += 1

            # Check the images format is valid or not
            if ext in format_types:
                zip_info.filename = f"{str(uuid.uuid4())[:5]}.png"
                count += 1
                # Extract The Photos
                zip_file.extract(zip_info, another_path)

        # Pass the number of all folder in report section
        report_files["total_files"] = count
        report_files["receive_file"] = count_all_files
        # Iterate directory
        # ==============================================

        album_images_path = f"{path}/"

        # Get all files from the directory
        for file_path in os.listdir(album_images_path):
            joining = os.path.join(album_images_path, file_path)

            name, ext = get_file_name(file_path)
            # Check The Format of images
            if ext in format_types:
                main_data[name] = joining

        # Set the images path to the album
        album.images_path = json.dumps(main_data)

        # Set The All Album Images Path
        album.image_folder_path = str(path)
        album.save()  # And Save The Album Model

    # Delete the the album zip file
    album.image_zip.delete()
    return report_files  # Return The Report for user about the files


# ==============================================================


@shared_task
def zip_album_files(album_id, zip_id):
    """
    This Task is used to zip the all album's images
    """
    # Get The all required things
    get_album = Album.objects.filter(id=album_id).first()
    # Load The All images path
    get_files = json.loads(get_album.images_path)

    # Create ZipFile
    zip_file = BytesIO()

    # create a zipfile
    with zipfile.ZipFile(zip_file, "w") as zip:
        # Get The Path from the album model
        for image in get_files.values():
            # split the images with / to get the name of file
            image_name = image.split("/")[-1]

            # Write
            zip.write(image, arcname=image_name)

    # Get The Value
    zip_content = zip_file.getvalue()

    # Upload zip to model
    model_instance = ZipAlbumFiles.objects.get(pk=zip_id)
    model_instance.zipfile.save(
        f"{get_album.user.id}___{get_album.id}.zip", ContentFile(zip_content)
    )

    # Delete All Images Folder
    shutil.rmtree(get_album.image_folder_path)

    get_album.images_path = None  # Set The Images Path to Null
    get_album.image_folder_path = None  # Set The folder Path to Null
    get_album.save()  # Just Save The Album

    return "Done!"


# =======================================================================


@shared_task
def delete_zipfile():
    """This Task is used to delete the zipfiles after 7 day from the database"""
    ZipAlbumFiles.objects.filter(
        created_time__lte=timezone.now() - timezone.timedelta(days=7)
    ).delete()  # Delete The all zipfile that should delete today


# =========================================================================
# @shared_task
# def render_album(album_id):
#     """ Render The Album File It Have an Error"""
#     # Get The Album Model
#     get_album = Album.objects.filter(id=album_id).first()
#
#     # Processs The Album
#     gProcess = GalleryProcessing(galleryDir=get_album.image_folder_path)
#     path_file = gProcess.featureExtraction(file_dir=get_album.image_folder_path, imageType="png",
#                                            file_name=album_id)
#
#     # Set The CSV Processed File
#     get_album.album_processed_file = path_file
#     get_album.save()
#     return "Done"

# ==================================================
# @shared_task
# def create_mosaic_photo(mosaic_id):
#     # Get The Mosaic
#     get_mosaic = Mosaic.objects.filter(id=mosaic_id).first()
#     master_image = get_mosaic.master_image.master_image.path  # Master Image
#     get_album = get_mosaic.album  # Album Model
#
#     # Check The Mosaic image exists or not
#     if get_mosaic.mosaic_result_path:
#         if os.path.exists(get_mosaic.mosaic_result_path):
#             os.remove(get_mosaic.mosaic_result_path)
#
#     # Call The Mosaic Creator Function
#     mosaic_create_task = create_mosaic(master=master_image,
#                                        album_processed_file_path=get_album.album_processed_file,
#                                        album=get_album.image_folder_path,
#                                        cellsize=get_mosaic.cell_size,
#                                        cutsize=get_mosaic.cut_size, enhance=get_mosaic.color_enhance,
#                                        blend=get_mosaic.blend, repeat=get_mosaic.repeat,
#                                        candidates=get_mosaic.candidates, radius=get_mosaic.radius)
#     # Set The Mosaic Photo Result Path to the mosaic Path
#     get_mosaic.mosaic_result_path = mosaic_create_task
#     get_mosaic.save()
#     return "Done"

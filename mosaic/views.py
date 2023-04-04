from PIL import Image

from users.mixins import *

from picartia.app import app

# Django Rest Framework Modules
from rest_framework import views, generics
from rest_framework.decorators import api_view
from django.http import FileResponse

# Custom Apps Import
from users.utils import check_token_exist
from .mixins import *
from .serializers import *
from .tasks import *
from .models import *
from .utils import *

"""     Master Image Section        """


# ============================================


class UploadMasterImage(CheckCompanyTokenExist, views.APIView):
    """
    Upload The Master Image
    """

    def get(self, request, *args, **kwargs):
        # =======================
        return Response({"detail": "Upload your master image With POST Request"})

    def post(self, request, *args, **kwargs):
        # =======================
        """Handle The POST Method"""
        # Get Some Required
        get_master_image = request.FILES.get("master_image")

        # Check The Uploaded Image
        boolean, data = check_image(
            get_master_image,
            format_types=[".jpg", ".png", ".jpeg"],
            name="master_image",
            max_size=20,
            min_size=10,
        )

        # return the checked data
        if boolean != True:
            return data

        else:
            # Create a Master Image
            main_data = MasterImage.objects.create(
                master_image=get_master_image, user=self.profile, company=self.company
            )

            # Create A Mosaic Record
            mosaic_create = Mosaic.objects.create(
                user=self.profile, company=self.company, master_image=main_data
            )

            # Serializer the Mosaic Created
            serialize_mosaic_data = MosaicSerializer(mosaic_create, many=False)
            serialize_data = MasterImageSerializer(
                main_data, many=False
            )  # Serializer The Master Image

            # Return The Response
            return Response(
                {"Master": serialize_data.data, "Mosaic": serialize_mosaic_data.data}
            )


# =========================================


class MasterImageDelete(CheckCompanyTokenExist, views.APIView):
    """
    This Class is used to Delete a master image
    """

    def get(self, request, pk=None, *args, **kwargs):
        # Check Company

        # =======================
        return Response(
            {
                "detail": "Just Send A Request With DELETE Method To Delete The Master Image!"
            }
        )

    def delete(self, request, pk=None, *args, **kwargs):
        # Check Company

        # =======================
        """Handle The DELETE Method"""
        # Get The Master Image With PK
        data = MasterImage.objects.filter(
            id=pk, user=self.profile, company=self.company
        ).first()

        # Check The Master Image exists
        if data is None:
            return Response(
                {"detail": "Master Image not found!"},
                status=status.HTTP_404_NOT_FOUND,
            )  # Return A Response When The Master Image Not Found!

        # Delete the Master Image
        data.delete()
        return Response(
            {"detail": "Successfully Master Image Deleted!"},
            status=status.HTTP_204_NO_CONTENT,
        )  # Return The Response When Deleted


# ======================================================


class DownloadMasterImage(CheckCompanyTokenExist, views.APIView):
    """
    This view is used to download the master image
    """

    def get(self, request, pk=None, *args, **kwargs):
        # Check Company

        # =======================
        """Handle the Get Request"""
        # Get The Master Image With PK
        get_master_image = MasterImage.objects.filter(
            id=pk, user=self.profile, company=self.company
        ).first()

        # Check The Master Image exists
        if get_master_image is None:
            return Response(
                {"detail": "The Master Image Not Found!"},
                status=status.HTTP_404_NOT_FOUND,
            )  # Return A Response When The Master Image Does Not Exists!

        # Return The File Response To Download
        return FileResponse(
            get_master_image.master_image.open(), as_attachment=True
        )  # Return The File Path


# ================================================
"""     Album Section        """


# ===================================


class UploadAlbum(CheckCompanyTokenExist, views.APIView):
    """
    Upload the Album File
    """

    def get(self, request, pk=None, *args, **kwargs):

        # Check Company

        # =======================
        return Response(
            {
                "detail": "Upload Your album_file Just With POST Method!Note: Your Album Images Should be a ZIP file"
            }
        )  # Return A Response Just For Info

    def post(self, request, pk=None, *args, **kwargs):

        # =======================
        """Handle The POST Method"""
        # Check The Mosaic Exists
        is_exists, get_mosaic = get_mosaic_model(pk, self.profile, self.company)
        # Check Mosaic Exists
        if not is_exists:
            return get_mosaic
        # Get Some Required Things
        get_file = request.FILES.get("album_file")
        get_title = request.POST.get("title")
        # Check The Mosaic Have A Master Image
        if get_mosaic.master_image is None:
            return Response({"detail": "This Mosaic Don't have any master image"})

        # Check the file uploaded
        if get_file is None:
            return Response({"detail": "You Should Upload your album_file!"})

        # Check The title set!
        if get_title is None:
            return Response({"detail": "You Should Set the title for your album"})

        # Validate The Album ZIP File
        boolean, data = check_image(
            get_file,
            format_types=[".zip"],
            name="album_file",
            max_size=200,
            min_size=100,
        )

        # Return Data if is False
        if not boolean:
            return data

        # Process images if data is True
        else:
            # Get Company And Profile

            # if album not exists
            if get_mosaic.album is None:
                # Create The Album
                album = Album.objects.create(
                    title=get_title,
                    image_zip=get_file,
                    user=self.profile,
                    company=self.company,
                )

                # Set The Mosaic Album And Save
                get_mosaic.album = album
                get_mosaic.save()

            # Serialize Data and return
            serialize_data = AlbumSerializer(get_mosaic.album, many=False)
            serialize_mosaic_data = MosaicSerializer(get_mosaic, many=False)
            return Response(
                {"Album": serialize_data.data, "Mosaic": serialize_mosaic_data.data},
                status=status.HTTP_201_CREATED,
            )


# =====================================================


class AlbumDelete(CheckCompanyTokenExist, views.APIView):
    """
    This View is use to Delete an Album
    """

    def delete(self, request, pk=None, *args, **kwargs):
        # Check Company

        # =======================
        """Handle DELETE Method"""
        # Check The Album Exists
        is_exists, get_album = get_album_model(pk, self.profile, self.company)
        if not is_exists:
            return get_album
        get_album.delete()

        return Response({"detail": "Successfully Your Album Deleted!"})


# =============================================================


class DownloadAlbumImage(CheckCompanyTokenExist, views.APIView):
    """
    This Class is used to Download the zip version of album
    """

    def get(self, request, pk=None, *args, **kwargs):

        # Check Company

        # =======================
        """Handle The Get Method"""
        # Check The Album Exists
        is_exists, get_album = get_album_model(pk, self.profile, self.company)
        if not is_exists:
            return get_album

        # Get The Album Zip File in database
        get_zipfiles = ZipAlbumFiles.objects.filter(album=get_album).first()
        zipfiles = None
        # Check this album is exists in zip file database
        if get_zipfiles is not None:
            zipfiles = get_zipfiles.zipfile.path
        elif get_album.image_zip:
            zipfiles = get_album.image_zip.path

        else:
            return Response(
                {
                    "detail": "The Zipfile extracted Or At the first you should request to the zip url to zip the file!"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return FileResponse(zipfiles, as_attachment=True)


# =============================================================


class ZipAlbumImages(CheckCompanyTokenExist, views.APIView):
    """
    This Class is used to Zip the all album images
    """

    def get(self, request, pk=None, *args, **kwargs):
        """Handle the Get Request"""
        return Response({"detail": "Just Send the request with POST method!"})

    def post(self, request, pk=None, *args, **kwargs):
        """Handle The Post Request"""
        # Check The Album Exists
        is_exists, get_album = get_album_model(pk, self.profile, self.company)
        if not is_exists:
            return get_album

        # Check The Album main directory path exists
        if get_album.images_path is None:
            return Response(
                {"detail": "This File has not extracted!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Proccess
        create_zip_file = ZipAlbumFiles.objects.create(
            album=get_album
        )  # Create The Zip file
        zip_file_task = zip_album_files.delay(
            get_album.id, create_zip_file.id
        )  # Just Call The Celery Task
        response_data = {
            "data": "Your Request is being processed.Please Wait...!You Can See Your Request Status in this url task/status/<task_id>/",
            "Task ID": zip_file_task.id,
        }
        return Response(response_data)


# ==================================================


class UnZipAlumImages(CheckCompanyTokenExist, views.APIView):
    """
    Unzip the all images
    """

    def post(self, request, pk=None, *args, **kwargs):

        # Check Company

        # =======================
        """
        Handle the POST Request
        """
        # Check The Album Image
        # Check The Album Exists
        is_exists, get_album = get_album_model(pk, self.profile, self.company)
        if not is_exists:
            return get_album

        # Check That the zip file of images exists or Not
        try:
            data = get_album.image_zip.url
        except:
            return Response({"detail": "This Album Extracted Or Zipped Again!"})

        # Assign the all Unziped Files
        main_file_path = ""
        data = get_album.image_zip.path.split("\\")
        data.pop(len(data) - 1)

        for s in data:
            main_file_path += f"{s}\\"

        # Use Celery Task to unzip all images
        upload_file = upload_photo.delay(
            zip_file_path=get_album.image_zip.path,
            extract_to=main_file_path,
            album_id=get_album.id,
            title=get_album.title,
        )

        # Check the task is Running or Not

        # Return Back a wait message and the celery task id for user
        response_data = {
            "data": "Your Request is being processed.Please Wait...!You Can See Your Request Status in this url task/status/<task_id>/",
            "Task ID": upload_file.id,
        }
        return Response(response_data)


# =========================================================================
class ViewAlbumImages(CheckCompanyTokenExist, views.APIView):
    """This Class is used to View all album images"""

    def get(self, request, pk=None, *args, **kwargs):

        # Check Company

        # =======================
        """Handle The Get Method"""
        # Check The Album Exists
        is_exists, get_album = get_album_model(pk, self.profile, self.company)
        if not is_exists:
            return get_album

        # Check The images path is None
        elif get_album.images_path is None:
            return Response(
                {
                    "detail": "Album don't have the list of photo! Just go to the unzip url"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Return The all path of images
        images = json.loads(get_album.images_path)
        return Response(images, status=status.HTTP_200_OK)


# ========================================================
class RenameAlbum(CheckCompanyTokenExist, generics.UpdateAPIView):
    """
    This View is use for Rename an album
    """

    queryset = Album.objects.all()
    serializer_class = RenameAlbumSerializer


# ========================================================
class AddSinglePhoto(CheckCompanyTokenExist, views.APIView):
    """Add a signle photo to the album images"""

    def get(self, request, pk=None, *args, **kwargs):
        """Handle The GET Method"""
        return Response({"detail": "Just Send a POST Request with image!"})

    def post(self, request, pk=None, *args, **kwargs):
        """Handle The POST Method"""
        # Check The Album Exists
        is_exists, get_album = get_album_model(pk, self.profile, self.company)
        if not is_exists:
            return get_album

        # Check The Images Path Exists Or Not
        if get_album.images_path is None:
            return Response({"detail": "The Album Image deleted or zipped!"})

        # Check That The Album File Unziped or Not
        if get_album.image_zip:
            return Response({"detail": "Your Should Unzip your file"})
        # Check the image uploaded or not
        get_image = request.FILES.get("image")
        if get_image is None:
            return Response(
                {"detail": "Upload the image file!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Send the data to the Celery Task
        boolean, data = check_image(
            get_image=get_image,
            format_types=[".jpg", ".png", ".jpeg"],
            name="image",
            max_size=10,
            min_size=100,
        )

        # Return The Data
        if not boolean:
            return data

        # ==================================
        name, ext = get_file_name(get_image.name)

        name = f"{str(uuid.uuid4())[:5]}"
        # Just Save The Image
        get_image = Image.open(get_image)
        get_image.save(f"{get_album.image_folder_path}/{name}{ext}")
        # Load The Json Data From The Album Model
        load_data = json.loads(get_album.images_path)

        # Just Add The New Name for image
        load_data[name] = f"{get_album.image_folder_path}/{name}{ext}"

        # Set The Album Images Path
        get_album.images_path = json.dumps(load_data)

        get_album.save()  # Save The Album

        return Response({"detail": "Successfully Added!"}, status=status.HTTP_200_OK)


# ===============================================================
class DeleteListOfImages(CheckCompanyTokenExist, views.APIView):
    """
    This View is use to delete the list of images
    """

    def get(self, request, pk=None, *args, **kwargs):

        # Check Company

        # =======================
        """Handle The Get Method"""
        return Response(
            {"detail": "Just Send The DELETE request with the list of image's id"}
        )

    def delete(self, request, pk=None, *args, **kwargs):

        # Check Company

        # =======================
        """Handle The POST Method"""
        images = request.POST.get("images_id")
        # Check The Album Exists
        is_exists, album = get_album_model(pk, self.profile, self.company)
        if not is_exists:
            return album

        images_ids = list(json.loads(album.images_path).keys())
        # Check exists or not
        if album is None:
            return Response({"detail": "Album Not Found!"})

        # Check the images uploaded or not
        if images is None:
            return Response(
                {
                    "detail": "Set images_id and to delete multiple images seperate with ,!",
                    "images_id": images_ids,
                }
            )
        # Check Image Path
        split_files = str(images).split(",")
        load_data = json.loads(album.images_path)
        deleted_count = 0
        undeleted_count = 0

        # Get Images
        for s in split_files:
            if s in list(load_data.keys()):
                os.remove(load_data[s])
                load_data.pop(s)
                deleted_count += 1
            else:
                undeleted_count += 1

        # Pass the images path to the album

        album.images_path = json.dumps(load_data)
        album.save()
        return Response(
            {"detail": f"{deleted_count} Deleted! {undeleted_count} Not Found!"}
        )


# Album Render Status View


# =======================================================
class AlbumThumbImage(CheckCompanyTokenExist, views.APIView):
    """This Class is used to assign the Thumbnail image for album"""

    def get(self, request, pk=None, *args, **kwargs):
        """
        Handle The Get Request
        """
        return Response(
            {
                "detail": "Just Send a POST Request and Set Id Of Image to set as default thumnail image!"
            }
        )

    def post(self, request, pk=None, *args, **kwargs):

        # Check Company

        # =======================
        """Handle The Post Request"""
        # Get The Image_id and Album
        image_id = request.POST.get("image_id")

        # Check The Album Exists
        is_exists, album = get_album_model(pk, self.profile, self.company)
        if not is_exists:
            return album
        # Check The Image_id exists or not
        if album.images_path is None:
            return Response({"detail": "The Album File Zipped!"})

        images_ids = list(json.loads(album.images_path).keys())

        # Just Return A Response To Select A Image id
        if image_id is None:
            return Response(
                {
                    "detail": "Set the image_id from this list",
                    "images_id": images_ids,
                }
            )

        # Check The Image id Exists in images id
        if image_id not in images_ids:
            return Response(
                {
                    "detail": "Image Not Found! Selected Another Image",
                    "images_id": images_ids,
                }
            )
        # Set as default Thumbnail
        load_data = json.loads(album.images_path)
        for s in list(load_data.keys()):

            if image_id == s:
                album.default_thumnail_image = str(load_data[s])

        # Save The Album And Assign The thumbnail image
        album.save()
        return Response({"detail": "Your Image Successfully Assigned!"})


# =========================================
class AlbumRender(CheckCompanyTokenExist, views.APIView):
    def get(self, request, pk, format=None):
        return Response({"detail": "Just Send The POST Request!"})

    def post(self, request, pk, format=None):
        """Handle The POST Request"""
        # Check The Album Exists
        is_exists, get_album = get_album_model(pk, self.profile, self.company)
        if not is_exists:
            return get_album

        # Call The Celery Task
        elif get_album.images_path is None or get_album.image_zip:
            return Response(
                {"detail": "Your Album Don't have any photo or your album Zipped!"}
            )
        # album_ren = render_album.delay(get_album.id)
        response_data = {
            "data": f"Your Request is being processed.Please Wait...! You Can See Your Request Status in this url task/status/<task_id>/",
            # "Task ID": album_ren.id,
        }
        return Response(response_data)


"""         Mosaic Section           """


class MosaicRender(CheckCompanyTokenExist, SetMosaicParameter, views.APIView):
    """This View"""

    serializer_class = MosaicSerializer

    def get(self, request, pk, format=None):
        """Handle The GET Request"""
        return Response({"detail": "Just Send The POST Request!"})

    def post(self, request, pk, format=None):
        """Handle The POST Request"""
        set_mosaic_parameter(pk, self.parameter)  # Set The Mosaic Parameters
        # mosaic_create = create_mosaic_photo.delay(pk)  # Call The Celery Task to create the mosaic
        response_data = {
            "data": f"Your Request is being processed.Please Wait...! You Can See Your Request Status in this url task/status/<task_id>/",
            # "Task ID": mosaic_create.id,
        }
        return Response(response_data)


# ======================================================

# Download the Mosaic


class MosaicDownload(CheckCompanyTokenExist, views.APIView):
    """Download The Mosaic Photo"""

    def get(self, request, pk, format=None):
        """Handle The GET Request"""
        # Get The Mosaic Model
        # Check The Mosaic Exists
        is_exists, get_mosaic = get_mosaic_model(pk, self.profile, self.company)
        if not is_exists:
            return get_mosaic

        # Check The Mosaic Image Exists
        elif get_mosaic.mosaic_result_path:
            if not os.path.exists(get_mosaic.mosaic_result_path):
                return Response({"detail": "Your Mosaic photo Does Not Exists"})
        else:
            return Response({"detail": "Mosaic Was Not Created!"})
        return FileResponse(get_mosaic.mosaic_result_path, as_attachment=True)


# ===============================================
# Delete Mosaic View
class MosaicDelete(CheckCompanyTokenExist, views.APIView):
    """Delete The Mosaic Photo"""

    def delete(self, request, pk, format=None):
        """Handle The DELETE Request"""
        # Check The Mosaic Exists
        is_exists, get_mosaic = get_mosaic_model(pk, self.profile, self.company)
        if not is_exists:
            return get_mosaic

        # Delete The Mosaic
        get_mosaic.delete()
        return Response({"detail": "Successfully Mosaic Deleted!"})  # Return A Response


@api_view(["GET"])
def task_status(request, task_id):
    """Check The Status of celery tasks"""

    try:
        token = request.headers["company-auth"]
        company = CompanyToken.objects.filter(token=token).first()
        # Check the company with the header exists or not
        if company is not None:
            # Proccess Them
            try:

                task_result = app.AsyncResult(task_id)

                # Check if successful
                if task_result.successful():
                    return Response(
                        {
                            "Message": "Task Completed Successfully!",
                            "Result": task_result.result,
                        }
                    )

                # Check if failed
                elif task_result.failed():
                    return Response(
                        {
                            "Message": "Task Failed!",
                            "Result": task_result.result,
                        }
                    )

                # Check if still Running
                else:
                    return Response(
                        {
                            "Message": "Task is Still Running!",
                            "Result": task_result.result,
                        }
                    )
            # If Task Not Found!
            except:
                return Response({"Message": "Task Not Found!"})

        # If the company not found!
        else:
            return Response({"detail": "Company Not Found!"})
    except:
        return Response({"detail": "An Error Occured!"})

from django.urls import path
from . import views

# Create your tests here
app_name = "mosaic"

urlpatterns = [
    # Master Image URLS
    path(
        "master/upload/", views.UploadMasterImage.as_view(), name="upload_master_image"
    ),
    path(
        # To Delete a Master Image
        "master/delete/<str:pk>/",
        views.MasterImageDelete.as_view(),
        name="delete_master_image",
    ),
    path(
        # Download The Master Image
        "master/download/<str:pk>/",
        views.DownloadMasterImage.as_view(),
        name="download_master_image",
    ),
    # Album URLS
    path(
        # This URL is for upload the album image
        "album/upload/<str:pk>/",
        views.UploadAlbum.as_view(),
        name="upload_album_files",
    ),
    path(
        # This URL is for delete the album image
        "album/delete/<str:pk>/",
        views.AlbumDelete.as_view(),
        name="delete_album_files",
    ),
    path(
        # This URL is for zip the album images
        "album/zip/<str:pk>/",
        views.ZipAlbumImages.as_view(),
        name="zip_album_files",
    ),
    path(
        # This URL is for unzip the album images
        "album/unzip/<str:pk>/",
        views.UnZipAlumImages.as_view(),
        name="unzip_album_files",
    ),
    path(
        # To Download the zip file of album
        "album/download/<str:pk>/",
        views.DownloadAlbumImage.as_view(),
        name="download_album_zip_file",
    ),
    path(
        # To View the all images
        "album/view/<str:pk>/",
        views.ViewAlbumImages.as_view(),
        name="view_album_files",
    ),
    path(
        # Rename an album
        "album/rename/<str:pk>/",
        views.RenameAlbum.as_view(),
        name="rename_album",
    ),
    path(
        # Add Single Image for album
        "album/item/add/<str:pk>/",
        views.AddSinglePhoto.as_view(),
        name="upload_single_image",
    ),
    path(
        # Delete The List of Items
        "album/item/delete/<str:pk>/",
        views.DeleteListOfImages.as_view(),
        name="delete_a_list_of_images",
    ),
    path(
        # Set The Thumbnail image for album images
        "album/thumb/<str:pk>/",
        views.AlbumThumbImage.as_view(),
        name="set_default_thumbnail",
    ),
    path("task/status/<str:task_id>/", views.task_status, name="task_status"),
    # Render Album
    path(
        "album/render/<str:pk>/", views.AlbumRender.as_view(), name="album_render_view"
    ),
    # Mosaic Section
    path("mosaic/render/<str:pk>/", views.MosaicRender.as_view(), name="mosaic_render"),
    # Mosaic Download
    path(
        "mosaic/download/<str:pk>/",
        views.MosaicDownload.as_view(),
        name="mosaic_download",
    ),
    # Mosaic Delete
    path("mosaic/delete/<str:pk>/", views.MosaicDelete.as_view(), name="mosaic_delete"),
]

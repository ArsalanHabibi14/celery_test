from users.models import Profile, Company
from .utils import *
from django.conf import settings
from django.utils.timezone import now


def generate_id():
    letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "".join(random.choices(letters, k=7))


class MasterImage(models.Model):
    """
    The Master Images with different versions
    """

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    master_image = models.ImageField(
        upload_to=set_final_name,
        validators=[validate_file_extension, validate_file_size],
    )
    size = models.IntegerField(null=True, blank=True)
    created_time = models.DateTimeField(default=now, null=True, blank=True)
    id = models.CharField(
        max_length=7, default=generate_id, editable=False, primary_key=True, unique=True
    )

    def __str__(self):
        return f"{self.id} Master Image"

    def thumbnail_image(self):
        return format_html(
            f"<a href='{self.master_image.url}'><img src='{self.master_image.url}' alt='{self.id}' style='width:100px;height:70px;border-radius:10px;'></a>"
        )

    def show_size(self):
        if self.size > 1024:
            return f"{round(self.size / 1024, 2)} MB"
        return f"{self.size} KB"


class Album(models.Model):
    """
    This Class is for upload an Album
    """

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    created_time = models.DateTimeField(default=now, null=True, blank=True)
    images_path = models.JSONField(null=True, blank=True)
    image_folder_path = models.CharField(
        max_length=5000, null=True, editable=False, unique=True
    )
    image_zip = models.FileField(upload_to=set_final_album_name, null=True, blank=True)
    default_thumnail_image = models.CharField(max_length=2000, null=True, blank=True)
    status = models.BooleanField(default=False)
    album_processed_file = models.CharField(max_length=2000, null=True, blank=True)
    id = models.CharField(
        max_length=7, default=generate_id, editable=False, primary_key=True, unique=True
    )

    def __str__(self):
        return self.title

    def show_thumbnail_image(self):
        """Just The The Thumbnail for user"""
        if not self.default_thumnail_image:
            return "No Thumbnail"

        get_main_file = self.default_thumnail_image.replace("\\", "/")
        split_files = get_main_file.split("/")
        path = ""
        get_index = split_files.index(settings.MEDIA_PATH_FILE)

        for s in range(len(split_files) - 1):
            if s > get_index:
                path += f"{split_files[s]}/"

        basename = os.path.basename(self.default_thumnail_image)
        name, ext = os.path.splitext(basename)

        main_path = f"{settings.MEDIA_URL}{path}{name}{ext}"

        return format_html(
            f"<a href='{main_path}'><img src='{main_path}' style='width:130px;height:80px;border-radius:10px;'></a>"
        )


class Mosaic(models.Model):
    """
    The Mosaic Info Model
    """

    SECURITY_CHOICES = (
        ("public", "Public"),
        ("private", "Private"),
    )

    FILL_TYPE_CHOICES = (("seq", "Sequance"), ("random", "Random"))

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    master_image = models.ForeignKey(
        MasterImage, on_delete=models.SET_NULL, null=True, blank=True
    )
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True)
    mosaic_name = models.CharField(max_length=200, default="Untitled", unique=False)
    description = models.TextField(null=True, blank=True)
    security_choices = models.CharField(
        max_length=200, choices=SECURITY_CHOICES, default="public"
    )
    # The Mosaic Parameter
    cell_size = models.IntegerField(default=250, null=True, blank=True)
    cut_size = models.IntegerField(default=40, null=True, blank=True)
    color_enhance = models.FloatField(default=0)
    blend = models.FloatField(default=0.5)
    repeat = models.IntegerField(default=50)
    fill = models.CharField(max_length=100, default="seq", choices=FILL_TYPE_CHOICES)
    candidates = models.IntegerField(default=20)
    radius = models.IntegerField(default=2)
    # ==================================
    mosaic_result_path = models.CharField(max_length=2000, null=True, blank=True)
    # ==================================
    is_buy = models.BooleanField(default=False)
    created_time = models.DateTimeField(default=now, null=True, blank=True)
    id = models.CharField(
        max_length=7, default=generate_id, editable=False, primary_key=True, unique=True
    )

    def __str__(self):
        return f"The {self.user.username} Mosaic Photo"

    def show_mosaic_thumbnail(self):
        if not self.mosaic_result_path:
            return "No Thumbnail"

        get_main_file = self.mosaic_result_path.replace("\\", "/")
        split_files = get_main_file.split("/")

        path = ""
        get_index = split_files.index(settings.MEDIA_PATH_FILE)

        for s in range(len(split_files) - 1):
            if s > get_index:
                path += f"{split_files[s]}/"

        basename = os.path.basename(self.mosaic_result_path)
        name, ext = os.path.splitext(basename)

        main_path = f"{settings.MEDIA_URL}{path}{name}{ext}"

        return format_html(
            f"<a href='{main_path}'><img src='{main_path}' style='width:130px;height:80px;border-radius:10px;'></a>"
        )

    def master_image_thumbnail(self):
        if not self.master_image:
            return "No Master Image!"
        return self.master_image.thumbnail_image()


# ===========================================
class ZipAlbumFiles(models.Model):
    """
    This Class is for the zipfiles and after 7 day the all will delete
    """

    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    zipfile = models.FileField(upload_to="zip_albums/", null=True, blank=True)
    created_time = models.DateTimeField(default=now, null=True, blank=True)
    expired_time = models.DateTimeField(
        default=expire_time, editable=False, null=True, blank=True
    )
    id = models.CharField(
        max_length=7, default=generate_id, editable=False, primary_key=True, unique=True
    )

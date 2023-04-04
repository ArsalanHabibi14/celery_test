from rest_framework import serializers

from .models import Mosaic, MasterImage, Album

import zipfile as zf


class MasterImageSerializer(serializers.ModelSerializer):
    """
    This Serializer Is use for the Master Image
    """

    user = serializers.SerializerMethodField("get_username")
    company = serializers.SerializerMethodField("get_company")

    class Meta:
        model = MasterImage
        fields = "__all__"
        read_only_fields = ["show_size"]

    def get_username(self, obj):
        """ Just Get The Username from the model """
        return obj.user.username

    def get_company(self, obj):
        """ Just Get The Company from the Master Model """
        return obj.company.company_name


class AlbumSerializer(serializers.ModelSerializer):
    """This Serializer is for the album"""

    class Meta:
        model = Album
        fields = "__all__"


class RenameAlbumSerializer(serializers.ModelSerializer):
    """This Serializer is used to Rename the album"""

    class Meta:
        model = Album
        fields = "__all__"
        read_only_fields = [
            "mosaic",
            "created_time",
            "images_path",
            "image_folder_path",
            "image_zip",
        ]


class AlbumImagesSerializer(serializers.Serializer):
    """It Just to give the Album Image Serializer"""

    image = serializers.ImageField()


class MosaicSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Mosaic
        fields = "__all__"

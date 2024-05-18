from io import BytesIO
import os

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_image_file_extension

from PIL import Image
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings

PROFILE_IMAGE_FOLDER = "profile_images"

class OverwriteFileStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        """File Storage that removes the old file
        so that we can make a new one (overwrite it)."""
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
    
def get_file_path(instance, filename):
    """Get a file path where the filename is a User's username,
    and give it the correct file extension."""
    ext = filename.split('.')[-1]
    username = instance.user.username
    filename = f"{username}.{ext}"
    
    return os.path.join("profile_images", filename)

def strip_exif_data(image: models.ImageField, username: str) -> None:
    """Strip exif data from an image file."""  
    # https://bhch.github.io/posts/2018/12/django-how-to-editmanipulate-uploaded-images-on-the-fly-before-saving/
      
    im = Image.open(image)
    
    thumb_io = BytesIO() # create a BytesIO object
    
    pixel_data = list(im.getdata())
    im_without_exif = Image.new(im.mode, im.size)
    im_without_exif.putdata(pixel_data)
    
    # save new image to BytesIO object
    # PNG supports alpha, which is why we use it
    im_without_exif.save(thumb_io, 'PNG', quality=85)
    
    # as a good practice, close the file handler after saving the image.
    im_without_exif.close()

    # WARNING:
    # Dunno what the use of name arg is here, as it's a representation
    #   of file data.
    new_image = File(thumb_io, name=image.name) # create a django friendly File object

    return new_image

class UserProfile(models.Model):
    """A social profile for a user."""
    user = models.OneToOneField(to=User,
                                on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to=get_file_path,
        default='profile_images/default_profile_image.jpg',
        storage=OverwriteFileStorage(),
    )
    bio_text = models.CharField(max_length=500,
                                blank=True)
    is_public = models.BooleanField(default=True)
    friends = models.ManyToManyField(to="self",
                                     blank=True)
    
    class Meta:
        ordering = ["user__username"]
        
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def save(self, *args, **kwargs):
        if self.profile_image.name != 'profile_images/default_profile_image.jpg':
            self.image = strip_exif_data(self.profile_image, self.user.username)

        super().save(*args, **kwargs)
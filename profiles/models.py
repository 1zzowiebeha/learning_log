from io import BytesIO
import os
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_image_file_extension

from PIL import Image
from PIL import ImageSequence
from django.core.files import File
from django.core.files.storage import FileSystemStorage

PROFILE_IMAGE_FOLDER = "profile_images"
DEFAULT_IMAGE_PATH = PROFILE_IMAGE_FOLDER + "/default/default_profile_image.jpg"


class ProfileImageFileStorage(FileSystemStorage):
    """If a file with the same name exists, delete it.
    Then, convert the file contents into PNG format.
    If it's a GIF, save the first frame as a PNG."""
    
    def get_available_name(self, name, max_length=None):
        """Remove the old file so that we can
        make a new one. (overwrite it)"""

        if self.exists(name):
            self.delete(name)

        return name
    
    def save(self, name, content, max_length=None):
        """If the file contents are not a sequence of
        images, convert to PNG format.
        
        If GIF contents are passed, extract the first frame,
        and convert the frame to PNG format.
        
<<<<<<< Updated upstream
        In both cases, EXIF data is not included in the final image.
        
        After all of this, pass the converted file
        off to FileSystemStorage to do the actual file system save."""
    
=======
        # Todo: if the image uploaded is a GIF,
        # store a frame from that GIF as a PNG instead of
        # corrupting the image via PNG conversion.
        
>>>>>>> Stashed changes
        with Image.open(content) as initial_image:
            final_image_io = BytesIO()
        
            if initial_image.format == "GIF":
                    # A context manager closes the file pointer for us,
                    #   and gives us clean code.
                    with ImageSequence.Iterator(initial_image)[0] as frame1:
                        frame1 = frame1.convert("RGBA")
                        frame1.save(final_image_io, format="PNG", quality=85)
            else:
                # Use RGBA channels to support PNG conversion
                if initial_image.mode != 'RGBA':
                    # convert() returns a pillow Image
                    with initial_image.convert('RGBA') as converted_temp_image:
                        converted_temp_image.save(final_image_io, format="PNG", quality=85)
                else:
                    initial_image.save(final_image_io, format="PNG", quality=85)
     
                
            
            new_file = File(final_image_io)
            
            new_name = super().save(name=name, content=new_file, max_length=max_length)
            
            return new_name
                        
    
def create_name(instance, filename):
    """Create a name for a profile picture ImageField,
    where the path is /profile_images/,
    and the filename is a User's username followed by the
    .png extension."""
    username = instance.user.username
    filename = f"{username}.png"
    
    return os.path.join(PROFILE_IMAGE_FOLDER, filename)


class UserProfile(models.Model):
    """A social profile for a user."""
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False)
    user = models.OneToOneField(to=User,
                                on_delete=models.CASCADE)
    # If profile_image doesn't update on the client's side,
    #   the browser may be caching an old version.
    # The user should clear their cookies until we find a better
    #   solution.
    profile_image = models.ImageField(
        upload_to=create_name,
        default=DEFAULT_IMAGE_PATH,
        storage=ProfileImageFileStorage(),
    )
    bio_text = models.CharField(max_length=500,
                                blank=True)
    is_public = models.BooleanField(default=True)
    friends = models.ManyToManyField(to="self",
                                     blank=True)
    pending_friends = models.ManyToManyField(to="self",
                                            blank=True)
    
    class Meta:
        ordering = ["user__username"]
        
    def __str__(self):
        return f"{self.user.username}'s profile"
    

class Notification(models.Model):
    """A notification for a user."""
    notify_profile = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    bootstrap_icon = models.TextField(blank=False)
    notification_text = models.TextField(blank=False)
    hyperlink = models.TextField(blank=True)
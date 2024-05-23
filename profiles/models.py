from io import BytesIO
import os
import uuid

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
            self.delete(name)

        return name
    
    def save(self, name, content, max_length=None):
        """Strip exif data from the file,
        and convert the contents to PNG format.
        
        If a GIF is passed, extract the first frame,
        strip the exif data, and convert the frame to PNG
        format.
        
        Then, pass it off to FileSystemStorage to do the
        actual file system save."""
        
        with Image.open(content) as initial_image:
            final_image_io = BytesIO()
            
            # Create a singular image from the initial image, and put its data in the image.
            with (
                Image.new(initial_image.mode, initial_image.size)
                as image_without_exif
            ):   
                if initial_image.format == "GIF":
                        try:
                            initial_image.seek(0)

                            image_pixel_data = list(initial_image.getdata())
                            first_frame_pixel_data = []
                            
                            # Store first frame of gif from its pixel data
                            current_line = 0
                            for index, pixel in enumerate(image_pixel_data):
                                # We've reached the end of the line. Begin a new one.
                                if index % initial_image.width == 0:
                                    current_line += 1
                                # We've reached the end of frame1.
                                if current_line == initial_image.height:
                                    break
                                
                                first_frame_pixel_data.append(image_pixel_data[index])
                             
                            image_without_exif.putdata(first_frame_pixel_data)
                            
                            # Use RGBA channels to support PNG conversion
                            if image_without_exif.mode != 'RGBA':
                                image_without_exif = image_without_exif.convert('RGBA')
                        
                            image_without_exif.save(fp=final_image_io, format='PNG', quality=85)
                        except EOFError:
                            print("EOF occured. Check the code and spot the bug >:)")
                else:
                    image_pixel_data = list(initial_image.getdata())
                    image_without_exif.putdata(image_pixel_data)
                    
                    # Use RGBA channels to support PNG conversion
                    if image_without_exif.mode != 'RGBA':
                        image_without_exif = image_without_exif.convert('RGBA')
                    
                    # Save new image to final_image_io BytesIO object
                    # PNG supports alpha, which is why we use it
                    image_without_exif.save(fp=final_image_io, format='PNG', quality=85)
                
                # Instantiate im_without_exif with the new image data
                # and to let the context manager handle closing the file.
                #with Image.open(final_image_io) as im_without_exif: 
                new_file = File(final_image_io, name=name)
                    
                new_name = super().save(name=name, content=new_file, max_length=max_length)
                    
                # As a good practice, close the file handler after we are do.
                image_without_exif.close()
                    
                return new_name

    
def create_name(instance, filename):
    """Create a name for a profile picture ImageField,
    where the path is /profile_images/,
    and the filename is a User's username followed by the
    .png extension."""
    username = instance.user.username
    filename = f"{username}.png"
    
    return os.path.join("profile_images", filename)

def process_image(image: models.ImageField, username: str) -> None:
    """Convert image to PNG and strip exif data from an image file."""  
    # https://bhch.github.io/posts/2018/12/django-how-to-editmanipulate-uploaded-images-on-the-fly-before-saving/
      
    im = Image.open(image)
    
    final_image_io = BytesIO() # create a BytesIO object
    
    pixel_data = list(im.getdata())
    im_without_exif = Image.new(im.mode, im.size)
    im_without_exif.putdata(pixel_data)
    
    if im_without_exif.mode != 'RGBA':
        im_without_exif = im_without_exif.convert('RGBA')
        
        
    # save new image to BytesIO object
    # PNG supports alpha, which is why we use it
    im_without_exif.save(fp=final_image_io, format='PNG', quality=85)
    
    im_without_exif = Image.open(final_image_io)
    
    print(im_without_exif.format, im_without_exif.mode)
    
    # as a good practice, close the file handler after saving the image.
    im_without_exif.close()

    
    media_relative_path = os.path.split(image.path)[-2:]
    dirname = media_relative_path[0]
    filename = media_relative_path[1]
    #filename_without_ext = '.'.join(filename.split('.')[:-1])
    #new_name = f"{dirname}/{filename_without_ext}.png"
    
    #print(f"New_name: {new_name}")
    
    # WARNING:
    # Dunno what the use of name arg is here, as it's a representation
    #   of file data.
    new_image = File(final_image_io) # create a django friendly File object

    # Delete the old image (may be a diff type)
    filepath = settings.MEDIA_ROOT / dirname / filename
    if os.path.exists(filepath):
        os.remove(filepath)
            
    return new_image

class UserProfile(models.Model):
    """A social profile for a user."""
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False)
    user = models.OneToOneField(to=User,
                                on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to=create_name,
        default='profile_images/default/default_profile_image.jpg',
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
    
    #def save(self, *args, **kwargs):
    #    if self.profile_image.name != 'profile_images/default_profile_image.jpg':
    #        self.image = process_image(self.profile_image, self.user.username)
    #
    #    super().save(*args, **kwargs)
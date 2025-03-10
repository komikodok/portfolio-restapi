from django.db import models
from django.utils.text import slugify
from django.conf import settings
from cloudinary.models import CloudinaryField


class Project(models.Model):
    title = models.CharField(max_length=250, unique=True)
    description = models.TextField()
    prefix = models.TextField()
    suffix = models.TextField()
    slug = models.SlugField(unique=True, blank=True, editable=False)
    github = models.CharField(max_length=250, unique=True, null=True)
    view_count = models.IntegerField(default=0)
    if settings.DEBUG:
        image = models.ImageField(upload_to="image/")
    else:
        image = CloudinaryField(
            "image", 
            folder="projects/", 
            resource_type="image",
        )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


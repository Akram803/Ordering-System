from django.db import models 
from django.urls import reverse

# Create your models here.
def upload_location(instance, filename):
    return '%s/%s'%(instance.id, filename)
    
class Post(models.Model):
    title = models.CharField(max_length=120)
    # slug = models.SlugField(unique=True)
    # image = models.FileField(blank=True, null=True )
    image = models.ImageField(
        # upload_to=upload_location,
        height_field='height_field',
        width_field='width_field',
        null=True,
        blank=True)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.pk})
    
    class Meta:
        ordering = [ "-timestamp", "-updated" ]
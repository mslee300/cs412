from django.db import models
from django.utils import timezone
from django.urls import reverse

class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    email = models.EmailField()
    profile_image_url = models.URLField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)

    def get_status_messages(self):
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StatusMessage(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def get_images(self):
        return Image.objects.filter(status_message=self).order_by('timestamp')

    def __str__(self):
        return f"{self.profile.first_name}: {self.message[:50]}"    
    

class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    status_message = models.ForeignKey('StatusMessage', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Image for StatusMessage: {self.status_message.id} uploaded on {self.timestamp}"
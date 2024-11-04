from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
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

    def get_friends(self):
        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        friends_profiles = [friend.profile2 if friend.profile1 == self else friend.profile1 for friend in friends]
        return friends_profiles
    
    def add_friend(self, other):
        if self == other:
            return
        
        if not Friend.objects.filter(
            models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)
        ).exists():
            Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        friends_ids = [friend.id for friend in self.get_friends()]
        return Profile.objects.exclude(id__in=friends_ids + [self.id])
    
    def get_news_feed(self):
        profiles = [self] + self.get_friends()
        return StatusMessage.objects.filter(profile__in=profiles).order_by('-timestamp')
    
    def is_owner(self, user):
        return self.user == user


class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profile1} & {self.profile2}"


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

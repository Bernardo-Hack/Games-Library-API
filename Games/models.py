from django.db import models

# Create your models here.

class Publisher(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    website = models.URLField(unique=True)

    def __str__(self):
        return self.name
    

class Game(models.Model):
    title = models.CharField(max_length=100, unique=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    description = models.TextField()
    release_date = models.DateField()
    genre = models.CharField(max_length=100)

    onWindows = models.BooleanField()
    onMac = models.BooleanField()
    onLinux = models.BooleanField()
    

    def __str__(self):
        return self.title
    
    def get_platforms(self):
        platforms = []
        if self.onWindows:
            platforms.append('Windows')
        if self.onMac:
            platforms.append('Mac')
        if self.onLinux:
            platforms.append('Linux')
        return platforms
    
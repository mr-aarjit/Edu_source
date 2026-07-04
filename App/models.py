from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    heading = models.CharField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return self.heading


class index_file(models.Model):

    heading = models.CharField()
    image = models.ImageField(upload_to='images/', null=True, blank=False)


    def __str__(self):
        return self.heading
    

class Sub_group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    heading = models.CharField()
    description = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    file = models.FileField(upload_to="files/", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
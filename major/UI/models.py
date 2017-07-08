from datetime import datetime, timedelta
from django.contrib.auth.models import Permission , User
from django.db import models


# Create your models here.


class Job(models.Model):
    title = models.CharField(max_length=30)
    company = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    post = models.CharField(max_length=30)
    no_of_vacancies = models.IntegerField()
    degree = models.CharField(max_length=30)
    skills = models.CharField(max_length=100)
    work_exp = models.CharField(max_length=100)
    deadline = models.DateField(default=datetime.now()+timedelta(days=7))
    appliers = models.ManyToManyField(User)

    def __str__(self):
        return self.title


def user_directory_path(instance, filename):
    #file will be uploaded to MEDIA_ROOT/username/<filename>
    return '{0}/{1}'.format(instance.applicant.username,filename)


class Cv(models.Model):
    applicant = models.ForeignKey(User, default=1)
    resume = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return self.applicant.username+"'s CV"
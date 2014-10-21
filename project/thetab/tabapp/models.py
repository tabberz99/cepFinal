from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Variable(models.Model):
    title = models.CharField(max_length=50)
    maxMarks = models.IntegerField()
    minMarks = models.IntegerField()
    
    def __unicode__(self):
      return self.title

class teamName(models.Model):
    name = models.CharField(max_length=30)
    
    def __unicode__(self):
      return self.name
    
class ScoreForm(models.Model):
    formname = models.CharField(max_length=50)
    groupNames = models.ManyToManyField(teamName,related_name="groupNames")
    components = models.ManyToManyField(Variable, related_name="components")
    timer = models.BooleanField(default=False)
    
    def __unicode__(self):
      return self.formname
    
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
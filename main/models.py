from django.db import models

# Create your models here.
class Squawk(models.Model):
	message = models.CharField(max_length=140)
	created = models.DateTimeField(auto_now_add=True)


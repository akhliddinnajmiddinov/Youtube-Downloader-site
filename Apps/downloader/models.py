import os
import uuid
from django.db import models


class Query(models.Model):
	url = models.CharField(max_length=300)
	quality = models.CharField(max_length=10)
	downloaded_file = models.FileField(upload_to='media/', null=True, blank=True)
	downloaded_percentage = models.IntegerField(default=0)


	def __str__(self):
		return self.url + ":" + self.quality
from django.db import models

class DataResource(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    source = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
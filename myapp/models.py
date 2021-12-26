from django.db import models

# Create your models here.
class FilesModel(models.Model):
    title = models.CharField(max_length=100,null=True)
    path=models.CharField(max_length=100,null=True)
    key_word=models.CharField(max_length=100,null=True)
    file_type=models.CharField(max_length=50,choices=[('text','text'),('video','video')],default=('text','text'))
    def __str__(self):
        return self.title

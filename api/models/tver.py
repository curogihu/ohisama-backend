from django.db import models
from .member import Member

class TVer(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    delete_flg = models.BooleanField(default=False)
    members = models.ManyToManyField(Member, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "TVer"
        verbose_name_plural = "TVers"
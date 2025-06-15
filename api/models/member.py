from django.db import models
from .agency import Agency

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    generation = models.IntegerField()
    birthplace = models.CharField(max_length=100, blank=True, null=True)
    joined_at = models.DateField()
    graduated_at = models.DateField(blank=True, null=True)
    fan_name = models.CharField(max_length=100, blank=True, null=True)
    penlight_color_1 = models.CharField(max_length=50)
    penlight_color_2 = models.CharField(max_length=50)
    image_url = models.URLField(blank=True, null=True)
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delete_flg = models.BooleanField(default=False)

    def __str__(self):
        return self.name

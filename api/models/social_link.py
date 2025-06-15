from django.db import models
from .member import Member

class SocialLink(models.Model):
    PLATFORM_CHOICES = (
        ("blog", "Blog"),
        ("instagram", "Instagram"),
        ("message", "Message App"),
    )

    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="social_links")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    hashtag = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delete_flg = models.BooleanField(default=False)

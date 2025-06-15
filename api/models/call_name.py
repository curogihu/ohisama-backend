from django.db import models
from .member import Member

class CallName(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="call_names")
    call_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    delete_flg = models.BooleanField(default=False)

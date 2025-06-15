from django.db import models

class Agency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    start_date = models.DateField(null=True)
    end_date = models.DateField(blank=True, null=True)
    delete_flg = models.BooleanField(default=False)

    def __str__(self):
        return self.name

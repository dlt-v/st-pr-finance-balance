from django.db import models
from django.contrib.auth.models import User


class Entry(models.Model):
    title = models.CharField(max_length=80, )
    created_at = models.DateField(auto_now_add=True)
    value = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'({self.created_at}) "{self.title}" {self.value}'

    class Meta:
        verbose_name_plural = "entries"

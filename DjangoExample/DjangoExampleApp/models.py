from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role, blank=True)

    @property
    def name(self):
        return self.user.get_full_name()
    
    @property
    def email(self):
        return self.user.email
    
    def __str__(self) -> str:
        return f'{self.name} ({self.email})'


class News(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.title} ({self.get_date()} by {self.author.name}){"[hidden]" if self.hidden else ""}'
    
    def get_date(self) -> str:
        return self.created_at.strftime("%d.%m.%Y, %H:%M")
    
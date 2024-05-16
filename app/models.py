from django.db import models

class ExerciseRecord(models.Model):
    date = models.DateField()
    description = models.TextField(blank=True)  # description 필드를 blank=True로 수정하여 선택 사항으로 만듭니다.

    def __str__(self):
        return f"Exercise on {self.date}"

"""
from django.contrib.auth.models import AbstractUser

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    # 사용자 지정 필드 추가

    # groups와 user_permissions 필드의 역참조 이름 변경
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # 관계 필드에 대한 역참조 이름 변경
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # 관계 필드에 대한 역참조 이름 변경
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )
"""
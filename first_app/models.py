from django.contrib.auth.models import User
from django.db import models

class CommentHistory(models.Model):
    text = models.TextField(max_length=100, verbose_name='Комментарий')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1, verbose_name='Автор')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-id']

    def __str__(self):
        return self.author.username

class ExpHistory(models.Model):
    res = models.CharField(max_length=100, verbose_name='Выражение')
    solution = models.IntegerField(default=0, verbose_name='Решение')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1, verbose_name='Автор')

    class Meta:
        verbose_name = 'Выражение'
        verbose_name_plural = 'Выражения'
        ordering = ['-id']

    def __str__(self):
        return self.author.username

class studentHistory(models.Model):
    hp = models.IntegerField(default=0, verbose_name="HP")
    iq = models.IntegerField(default=0, verbose_name="IQ")
    happi_index = models.IntegerField(default=0, verbose_name="HAPPI_INDEX")
    ##create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1, verbose_name='Автор')

    class Meta:
        verbose_name = 'О студенте'
        verbose_name_plural = 'О студенте'
        ordering = ['-id']

    def __str__(self):
        return self.author.username
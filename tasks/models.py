from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.utils.text import slugify


class Tasks(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField('Описание')
    added = models.DateTimeField(auto_now=True, verbose_name='Добавлено')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='Обновлено')
    date = models.DateField('Cрок', blank=True)
    finished = models.BooleanField(default=False, verbose_name='Завершено')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task', kwargs={'tasks_id': self.pk})

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Profile(models.Model):
    image = models.ImageField(upload_to='users/%Y/%m/%d/', default='img/cat.jpg')
    slug = models.SlugField(unique=True, max_length=155)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name='friends')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='added_profiles')

    def save(self, **kwargs):
        super().save(**kwargs)
        img = Image.open(self.image.path)
        if img.width > 300 or img.height > 300:
            new_size = (300, 300)
            img.thumbnail(new_size)
            img.save(self.image.path)
        if not self.slug:
            self.slug = slugify(self.user.username)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})

    def __str__(self):
        return self.user.username


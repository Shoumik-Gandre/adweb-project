from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from PIL import Image
import hashlib
import string
import secrets
from .custom_mixin import ModelDiffMixin
from django.contrib import messages

class Advertisement(models.Model, ModelDiffMixin):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/')
    url_link = models.URLField(default="")
    clicks = models.IntegerField(default=0)
    category = models.IntegerField(
        choices=(
            (0, 'science'),
            (1, 'math'),
            (2, 'anime'),
            (3, 'computers'),
            (4, 'nature'),
            (5, 'news'),
            (6, 'music'),
            (7, 'politics'),
            (8, 'anthology'),
            (9, 'medical'),
            (10, 'sports'),
            (11, 'fashion'),
            (12, 'others')
        ),
        default="others"
    )
    size = models.CharField(
            max_length=16, choices=(
            ('medium rectangle', '300x250 pixels'),
            ('large rectangle', '336x280 pixels'),
            ('leaderboard', '728x90 pixels'),
            ('half page', '320x600 pixels'),
            ('free size', 'free size')
        ), 
        default='free size'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateTimeField('date published', default=timezone.now)
    is_enabled = models.BooleanField(default=True)
    identification_key = models.CharField(max_length=32, default='0')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.identification_key == '0':
            key = ''.join(secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(32))
            self.identification_key = key
        super(Advertisement, self).save(*args, **kwargs)
        if self.get_field_diff('size'):
            img = Image.open(self.image.path)
            width, height = img.size
            left = 0
            top = 0
            if self.size == 'medium rectangle':
                right = 300
                bottom = 250
                
            elif self.size == 'large rectangle':
                right = 336
                bottom = 280
                
            elif self.size == 'leaderboard':
                right = 728
                bottom = 90
                
            elif self.size == 'half page':
                right = 320
                bottom = 600
                
            elif self.size == 'free size':
                pass

            img = img.crop((left, top, right, bottom))
            img.save(self.image.path, img.format)

class Website(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    userkey = models.CharField(max_length=32, default='0')

    def __str__(self):
        return str(self.url)

    def save(self, *args, **kwargs):
        notfound = True
        while notfound:
            key = ''.join(secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(32))
            if not Website.objects.filter(userkey=key).exists():
                notfound = False
                self.userkey = key
        super(Website, self).save(*args, **kwargs)


class AdvertisementLog(models.Model):
    """
    unique_key is only valid till we get a click, otherwise we set the value to '1'.
    """
    ad = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    site = models.ForeignKey(Website, on_delete=models.PROTECT)
    click_date = models.DateTimeField('date clicked', default=timezone.now)
    view_date = models.DateTimeField('date viewed', default=timezone.now)
    unique_key = models.CharField(max_length=32, default='0')
    is_clicked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_clicked:
            self.click_date = timezone.now()
            self.unique_key = '1'
        notfound = True
        if not self.is_clicked:
            while notfound:
                key = ''.join(secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(32))
                if not AdvertisementLog.objects.filter(unique_key=key, is_clicked=False).exists():
                    notfound = False
                    self.unique_key = key
        super(AdvertisementLog, self).save(*args, **kwargs)


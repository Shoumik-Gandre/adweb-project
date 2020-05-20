from django.conf import settings
from random import randint
import base64
from .models import Website
from PIL import Image
import secrets
import string
from adtool.models import Advertisement, AdvertisementLog

class AdvertisementAPI:

    def __init__(self, request, advertisement_model, size):
        super().__init__()
        self.model = advertisement_model
        self.request = request
        self.size = size
        self.website = None
        self.alog = None

    def get_advertisement(self, user_key):
        # Gives back an html string of the advertisement or error
        try:
            if self.key_confirmation(user_key):
                advertisement = self.advertisement_selection()
                # Retrieve advertisement image from Database here and send it as json
                advertisement_html = self.advertisement_html_maker_base64(advertisement)
                return advertisement_html
            else:
                # If key_confirmation is false we raise an exception
                print("Key Confirmation False")
                raise Exception()
        except ValueError as e:
            print("Something else", e)
            raise e

    def advertisement_selection(self):
        # Decides how are advertisements retrieved from database
        # it is in random mode
        model_objects = self.model.objects.filter(size=self.size, is_enabled=True)
        count = model_objects.count()
        random_index = randint(0, count-1)
        advertisement = model_objects[random_index]
        self.alog = AdvertisementLog(ad=advertisement, site=self.website)
        self.alog.save()
        return advertisement

    def advertisement_html_maker_base64(self, advertisement):
        img_path = advertisement.image.path
        image = Image.open(img_path)
        img_format = image.format.lower()
        with open(img_path, 'rb') as f:
            img = base64.b64encode(f.read()).decode('utf-8')
        advertisement_site = f'http://{self.request.get_host()}/api/advertisement/{advertisement.pk}/{self.website.pk}/{self.alog.unique_key}/'
        advertisement_image = f'<img src="data:images/{img_format};base64,{img}">'
        advertisement_html = f'<a target="_blank" href="{advertisement_site}"><img src="data:images/{img_format};base64,{img}"></a>'
        return advertisement_html

    def key_confirmation(self, user_key):
        try:
            website = Website.objects.get(userkey=user_key)
            if website:
                self.website = website
                return True
            else:
                return False
        except :
            return False





'''
temporary_keys = {}
class AdvanceKeyAPI:


    def __init__(self, user_key):
        super().__init__()
        self.user_key = user_key
        self.website_pk = None

    def user_key_confirmation(self):
        try:
            website = Website.objects.get(userkey=self.user_key)
            if website:
                self.website_pk = website.pk
                return True
            else:
                return False
        except :
            return False

    def get_temporary_key(self):
        try:
            if self.user_key_confirmation():
                key = ''.join(secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(10))
                temporary_keys[key] = self.website_pk
                print(temporary_keys)
                return key
        except Exception as e:
            print(e)
            raise Exception('Tempory key could not be generated')

class AdvanceAdvertAPI:
    def __init__(self, request, temp_key, size):
        self.request = request
        self.temp_key = temp_key
        self.size = size
        self.website_pk = None
        try:
            self.website_pk = temporary_keys[temp_key]
        except Exception as e:
            print(e)

    def get_advertisement(self):
        if self.website_pk:
            return self.advertisement_html_maker_base64(self.advertisement_selection())
        else:
            raise Exception('temporary key not valid')
        
    def advertisement_selection(self):
        # Decides how are advertisements retrieved from database
        # it is in random mode
        model_objects = Advertisement.objects.filter(size=self.size, is_enabled=True)
        count=model_objects.count()
        random_index=randint(0, count-1)
        return model_objects[random_index]

    def advertisement_html_maker_base64(self, advertisement):
        img_path = advertisement.image.path
        image = Image.open(img_path)
        img_format = image.format.lower()
        with open(img_path, 'rb') as f:
            img = base64.b64encode(f.read()).decode('utf-8')
        advertisement_site = f'http://{self.request.get_host()}/api/advertisement/{advertisement.pk}/{self.website_pk}'
        advertisement_image = f'<img src="data:images/{img_format};base64,{img}">'
        advertisement_html = f'<a target="_blank" href="{advertisement_site}"><img src="data:images/{img_format};base64,{img}"></a>'
        return advertisement_html

'''
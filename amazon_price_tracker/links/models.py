from django.db import models
from .utils import get_link_data
from django.core.mail import send_mail
# Create your models here.
class Link(models.Model):
    name = models.CharField(max_length=200 , blank=True)
    url = models.URLField()
    current_price = models.FloatField(blank=True)
    old_price = models.FloatField(default=0)
    price_diff = models.FloatField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('price_diff' , '-created')

    def save(self , *args , **kwargs):
        try:
            name , price = get_link_data(self.url)
        except:
            return 
        old_price = self.current_price
        if self.current_price:
            if(price>old_price):
                send_mail(
                'Hurry! Rates are Increasing',
                'Hey , Your Products rate has increased. Check out your account to Know More',
                'ssamarth1201@gmail.com',
                ['2018219@iiitdmj.ac.in'],
                fail_silently=False,
            )
            if(price<old_price):
                send_mail(
                'Hurry! Rates are Decreasing',
                'Hey , Your Products rate has decreased. Check out your account to Know More',
                'ssamarth1201@gmail.com',
                ['2018219@iiitdmj.ac.in'],
                fail_silently=False,
            )
            if price!=old_price:
                diff = price-old_price
                self.price_diff = round(diff , 2)
                self.old_price = old_price
        else:
            self.old_price=0
            self.price_diff=0
        self.name = name
        self.current_price = price
        super().save(*args , **kwargs)

        



